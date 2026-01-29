import requests
import json
import argparse
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def get_figma_metadata(file_key, access_token):
    """
    Fetches comprehensive metadata for a Figma file using the REST API.
    """
    base_url = "https://api.figma.com/v1"
    headers = {
        "X-Figma-Token": access_token
    }

    print(f"[*] Fetching metadata for file: {file_key}")
    
    # 1. Get File Metadata (Detailed metadata: creator, folder, etc.)
    # Endpoint: GET /v1/files/:key/meta
    meta_url = f"{base_url}/files/{file_key}/meta"
    
    try:
        meta_response = requests.get(meta_url, headers=headers)
        meta_response.raise_for_status()
        metadata = meta_response.json()
    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching file metadata: {e}")
        if meta_response.status_code == 403:
            print("[!] Access denied. Check your FIGMA_ACCESS_TOKEN and file permissions.")
        return None

    # 2. Get File Info (Additional metadata: version, components, styles)
    # Endpoint: GET /v1/files/:key?depth=1
    # Note: We use depth=1 to avoid downloading the entire document tree
    info_url = f"{base_url}/files/{file_key}?depth=1"
    
    try:
        info_response = requests.get(info_url, headers=headers)
        info_response.raise_for_status()
        file_info = info_response.json()
        
        # Merge relevant fields into our metadata object
        metadata['file_structure'] = {
            'lastModified': file_info.get('lastModified'),
            'editorType': file_info.get('editorType'),
            'version': file_info.get('version'),
            'component_count': len(file_info.get('components', {})),
            'component_set_count': len(file_info.get('componentSets', {})),
            'style_count': len(file_info.get('styles', {}))
        }
    except requests.exceptions.RequestException as e:
        print(f"[!] Note: Could not fetch additional file info (components/styles): {e}")

    return metadata

def get_file_components(file_key, access_token):
    """
    Fetches the list of published components within a file library.
    Endpoint: GET /v1/files/:file_key/components
    """
    url = f"https://api.figma.com/v1/files/{file_key}/components"
    headers = {"X-Figma-Token": access_token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('meta', {}).get('components', [])
    except Exception as e:
        print(f"[!] Warning: Could not fetch components list: {e}")
        return []

def get_file_styles(file_key, access_token):
    """
    Fetches the list of published styles within a file library.
    Endpoint: GET /v1/files/:file_key/styles
    """
    url = f"https://api.figma.com/v1/files/{file_key}/styles"
    headers = {"X-Figma-Token": access_token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('meta', {}).get('styles', [])
    except Exception as e:
        print(f"[!] Warning: Could not fetch styles list: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Fetch all metadata of a Figma file.")
    parser.add_argument("file_key", help="The key of the Figma file (from the URL)")
    parser.add_argument("--token", help="Figma Personal Access Token (or set FIGMA_ACCESS_TOKEN env var)")
    parser.add_argument("--output", help="Save output to a JSON file", default="figma-agent/common/file-metadata.json")

    args = parser.parse_args()

    # Get token from arg or environment
    token = args.token or os.environ.get("FIGMA_ACCESS_TOKEN")
    
    if not token:
        print("[!] Error: No Figma access token provided.")
        print("    Use --token or set the FIGMA_ACCESS_TOKEN environment variable.")
        sys.exit(1)

    # Clean file key if it's a full URL
    file_key = args.file_key
    if "figma.com/design/" in file_key:
        file_key = file_key.split("/design/")[1].split("/")[0]
    elif "figma.com/file/" in file_key:
        file_key = file_key.split("/file/")[1].split("/")[0]

    result = get_figma_metadata(file_key, token)

    if result:
        # Fetch detailed components and styles
        print("[*] Fetching detailed published components...")
        result['published_components'] = get_file_components(file_key, token)
        
        print("[*] Fetching detailed published styles...")
        result['published_styles'] = get_file_styles(file_key, token)

        # Print summary
        file_meta = result.get('file', {})
        print("\n=== Figma File Metadata Summary ===")
        print(f"Name:         {file_meta.get('name')}")
        print(f"Folder:       {file_meta.get('folder_name', 'N/A')}")
        print(f"Components:   {len(result['published_components'])} published")
        print(f"Styles:       {len(result['published_styles'])} published")
        print(f"Last Modified:{file_meta.get('last_touched_at')}")
        print("===================================\n")

        # Ensure output directory exists
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"[+] Created directory: {output_dir}")

        # Save to file
        with open(args.output, "w") as f:
            json.dump(result, f, indent=4)
        print(f"[+] Full metadata saved to {args.output}")

if __name__ == "__main__":
    main()
