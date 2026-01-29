
import json
import argparse
import os
import sys
from figma_core.client import FigmaClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Advanced Figma Data Extraction Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Subcommand: file
    parser_file = subparsers.add_parser("file", help="Get full file data (use with caution on large files)")
    parser_file.add_argument("file_key", help="Figma File Key")
    parser_file.add_argument("--depth", type=int, help="Depth of the tree to traverse")
    parser_file.add_argument("--summary", action="store_true", help="Analyze and print a summary of node types")
    
    # Subcommand: nodes
    parser_nodes = subparsers.add_parser("nodes", help="Get specific nodes")
    parser_nodes.add_argument("file_key", help="Figma File Key")
    parser_nodes.add_argument("node_ids", help="Comma-separated list of Node IDs (e.g., 1:2,3:4)")
    
    # Subcommand: images
    parser_images = subparsers.add_parser("images", help="Get image fill URLs")
    parser_images.add_argument("file_key", help="Figma File Key")

    # Subcommand: components
    parser_components = subparsers.add_parser("components", help="Get published components")
    parser_components.add_argument("file_key", help="Figma File Key")

    # Subcommand: styles
    parser_styles = subparsers.add_parser("styles", help="Get published styles")
    parser_styles.add_argument("file_key", help="Figma File Key")

    # Global arguments
    parser.add_argument("--token", help="Figma Personal Access Token")
    parser.add_argument("--output", help="Output JSON file path")

    args = parser.parse_args()

    # 1. Auth Setup
    token = args.token or os.environ.get("FIGMA_ACCESS_TOKEN")
    if not token:
        print("❌ Error: FIGMA_ACCESS_TOKEN is missing.")
        sys.exit(1)
        
    client = FigmaClient(token)
    
    # 2. Command Execution
    try:
        data = None
        if args.command == "file":
            print(f"📡 Fetching file: {args.file_key} (Depth: {args.depth})...")
            data = client.get_file(args.file_key, depth=args.depth)
            
            if args.summary:
                from figma_core.parser import FigmaParser
                p = FigmaParser(data)
                all_nodes = p.flatten_tree()
                # Count types
                counts = {}
                for n in all_nodes:
                    t = n.get("type", "UNKNOWN")
                    counts[t] = counts.get(t, 0) + 1
                
                print("\n📊 File Summary:")
                for t, count in counts.items():
                    print(f"  - {t}: {count}")
            
        elif args.command == "nodes":
            nodes_list = args.node_ids.split(",")
            print(f"📡 Fetching nodes: {nodes_list} from {args.file_key}...")
            
            # Fetch raw data
            raw_data = client.get_file_nodes(args.file_key, nodes_list)
            
            # Try to fetch variables for enrichment (Best effort)
            variables_map = {}
            try:
                print("   🎨 Fetching variables for enrichment...")
                vars_resp = client.get_local_variables(args.file_key)
                if vars_resp and "meta" in vars_resp:
                    # Improved variable resolution Logic
                    meta = vars_resp["meta"]
                    variables = meta.get("variables", {})
                    collections = meta.get("variableCollections", {})
                    
                    for vid, vdata in variables.items():
                        # Get default mode from collection
                        collection_id = vdata.get("variableCollectionId")
                        collection = collections.get(collection_id, {})
                        default_mode = collection.get("defaultModeId")
                        
                        # Resolve value
                        raw_value = vdata.get("valuesByMode", {}).get(default_mode)
                        
                        # Handle alias or direct value
                        # Note: Deep extraction might need recursive alias resolution, 
                        # but for now we capture the immediate value/alias.
                        
                        # syntax priority: WEB -> name
                        syntax = vdata.get("codeSyntax", {}).get("WEB")
                        clean_name = syntax if syntax else vdata["name"]

                        variables_map[vid] = {
                            "name": clean_name,
                            "original_name": vdata["name"],
                            "value": raw_value,
                            "type": vdata.get("resolvedType")
                        }
            except Exception as e:
                print(f"   ⚠️ Warning fetching variables: {e}")
                pass

            # Enrich
            from figma_core.parser import NodeEnricher
            enricher = NodeEnricher(variables_map=variables_map)
            
            # Map through roots
            data = {"nodes": {}}
            for nid, node_wrapper in raw_data.get("nodes", {}).items():
                if "document" in node_wrapper:
                    data["nodes"][nid] = enricher.enrich_node(node_wrapper["document"])

        elif args.command == "images":
            print(f"📡 Fetching image fills for: {args.file_key}...")
            data = client.get_image_fills(args.file_key)

        elif args.command == "components":
            print(f"📡 Fetching published components for: {args.file_key}...")
            data = client.get_published_components(args.file_key)

        elif args.command == "styles":
            print(f"📡 Fetching published styles for: {args.file_key}...")
            data = client.get_published_styles(args.file_key)
            
        else:
            parser.print_help()
            sys.exit(1)

        # 3. Output
        if args.output:
            # Ensure folder exists
            out_dir = os.path.dirname(args.output)
            if out_dir and not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)
                
            with open(args.output, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✅ Data saved to {args.output}")
        else:
            # Print first 500 chars to avoid spamming terminal
            print(json.dumps(data, indent=2)[:2000] + "...")

    except Exception as e:
        print(f"❌ Execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
