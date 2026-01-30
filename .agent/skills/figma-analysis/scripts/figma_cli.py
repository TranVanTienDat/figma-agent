
import json
import argparse
import os
import sys
from figma_core.client import FigmaClient
from dotenv import load_dotenv

# Load environment variables
# Try searching for .env in current directory or script's root
dotenv_path = os.path.join(os.getcwd(), '.env')
if not os.path.exists(dotenv_path):
    # Fallback to script directory's parent (assuming .agent/skills/...)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(script_dir, '../../../../', '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv() # Default search

def main():
    parser = argparse.ArgumentParser(description="Advanced Figma Data Extraction Tool")
    
    # ... [rest of the function]
    # (I'll just add the debug print inside main)
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Subcommand: file
    parser_file = subparsers.add_parser("file", help="Get full file data (use with caution on large files)")
    parser_file.add_argument("file_key", help="Figma File Key")
    # Depth removed to enforce recursive full fetch
    parser_file.add_argument("--summary", action="store_true", help="Analyze and print a summary of node types")
    
    # Subcommand: nodes
    parser_nodes = subparsers.add_parser("nodes", help="Get specific nodes")
    parser_nodes.add_argument("file_key", help="Figma File Key")
    parser_nodes.add_argument("node_ids", help="Comma-separated list of Node IDs (e.g., 1:2,3:4)")
    

    # Subcommand: components
    parser_components = subparsers.add_parser("components", help="Get published components")
    parser_components.add_argument("file_key", help="Figma File Key")

    # Subcommand: styles
    parser_styles = subparsers.add_parser("styles", help="Get published styles")
    parser_styles.add_argument("file_key", help="Figma File Key")

    # Subcommand: local-variables (Enterprise)
    parser_vars = subparsers.add_parser("local-variables", help="Get local variables (Enterprise)")
    parser_vars.add_argument("file_key", help="Figma File Key")

    # Subcommand: images
    parser_images = subparsers.add_parser("images", help="Get image URLs for nodes")
    parser_images.add_argument("file_key", help="Figma File Key")
    parser_images.add_argument("node_ids", help="Comma-separated Node IDs")
    parser_images.add_argument("--format", default="svg", help="Image format (svg, png, jpg, pdf)")
    parser_images.add_argument("--scale", type=float, default=1, help="Image scale")

    # Subcommand: extract-tokens (Local)
    parser_extract = subparsers.add_parser("extract-tokens", help="Extract tokens from local JSON file (X-Ray Scan)")
    parser_extract.add_argument("input_file", help="Path to input JSON file")

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
    print(f"🔓 Login success. Token loaded from {dotenv_path if os.path.exists(dotenv_path) else 'environment'}.")
    
    # 2. Command Execution
    try:
        data = None
        if args.command == "file":
            print(f"📡 Fetching file: {args.file_key} (Full Tree)...")
            data = client.get_file(args.file_key)
            
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


        elif args.command == "components":
            print(f"📡 Fetching published components for: {args.file_key}...")
            data = client.get_published_components(args.file_key)

        elif args.command == "styles":
            print(f"📡 Fetching published styles for: {args.file_key}...")
            data = client.get_published_styles(args.file_key)

        if args.command == "local-variables":
            print(f"📡 Fetching local variables for: {args.file_key}...")
            data = client.get_local_variables(args.file_key)
            if not data:
                print("⚠️  No local variables found or access denied (Enterprise feature).")
                data = {}

        elif args.command == "images":
            nodes_list = args.node_ids.split(",")
            print(f"📡 Fetching images for nodes: {nodes_list} ({args.format})...")
            data = client.get_images(args.file_key, nodes_list, format=args.format, scale=args.scale)

        elif args.command == "extract-tokens":
            print(f"🔍 Extracting tokens from: {args.input_file} (X-Ray Mode)...")
            
            if not os.path.exists(args.input_file):
                print(f"❌ Error: Input file not found: {args.input_file}")
                sys.exit(1)
                
            with open(args.input_file, 'r') as f:
                raw_json = json.load(f)
                
            # Normalize input to list of root nodes
            root_nodes = []
            if isinstance(raw_json, dict):
                if "nodes" in raw_json:
                    # Output from 'nodes' command
                    for nid, val in raw_json["nodes"].items():
                        # Check if it is raw (has "document") or enriched (is the node itself)
                        if "document" in val:
                            root_nodes.append(val["document"])
                        else:
                            root_nodes.append(val)
                elif "document" in raw_json:
                    # Output from 'file' command
                    root_nodes.append(raw_json["document"])
                else:
                    # Just a single node object?
                    root_nodes.append(raw_json)
            elif isinstance(raw_json, list):
                root_nodes = raw_json
                
            # Flatten recursively
            from figma_core.parser import FigmaParser, DesignTokenExtractor
            all_nodes = []
            
            # Helper parser to flatten tree
            # We construct a fake document wrapper to leverage existing flatten_tree
            p = FigmaParser({"document": {"children": root_nodes}})
            all_nodes = p.flatten_tree()
            
            print(f"   📊 Analyzing {len(all_nodes)} nodes...")
            
            extractor = DesignTokenExtractor(all_nodes)
            data = extractor.extract()
            print(f"   ✨ Found {len(data['colors'])} unique colors and {len(data['typography'])} font styles.")
            
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
