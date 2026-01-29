#!/usr/bin/env python3
"""
Figma Metadata Query Tool
Allows AI to efficiently extract specific information from metadata without loading the entire file.
"""

import json
import argparse
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_metadata(metadata_path="figma-agent/common/file-metadata.json"):
    """Load metadata file"""
    if not os.path.exists(metadata_path):
        print(f"[!] Error: Metadata file not found at {metadata_path}")
        print("    Run fetch_figma_metadata.py first to generate metadata.")
        sys.exit(1)
    
    with open(metadata_path, 'r') as f:
        return json.load(f)

def query_summary(data):
    """Get high-level summary of the file"""
    file_meta = data.get('file', {})
    file_structure = data.get('file_structure', {})
    
    summary = {
        "file_name": file_meta.get('name'),
        "folder": file_meta.get('folder_name'),
        "last_modified": file_meta.get('last_touched_at'),
        "version": file_structure.get('version'),
        "total_components": len(data.get('published_components', [])),
        "total_styles": len(data.get('published_styles', []))
    }
    return summary

def query_components(data, search_term=None):
    """Get list of components, optionally filtered by search term"""
    components = data.get('published_components', [])
    
    if search_term:
        components = [
            c for c in components 
            if search_term.lower() in c.get('name', '').lower()
        ]
    
    # Return simplified version (name, node_id, description only)
    return [
        {
            "name": c.get('name'),
            "node_id": c.get('node_id'),
            "description": c.get('description', 'No description'),
            "thumbnail": c.get('thumbnail_url')
        }
        for c in components
    ]

def query_styles(data, style_type=None):
    """Get list of styles, optionally filtered by type (FILL, TEXT, EFFECT, GRID)"""
    styles = data.get('published_styles', [])
    
    if style_type:
        styles = [
            s for s in styles 
            if s.get('style_type') == style_type.upper()
        ]
    
    # Return simplified version
    return [
        {
            "name": s.get('name'),
            "type": s.get('style_type'),
            "node_id": s.get('node_id'),
            "description": s.get('description', 'No description')
        }
        for s in styles
    ]

def query_component_by_name(data, component_name):
    """Get detailed info for a specific component by name"""
    components = data.get('published_components', [])
    
    for c in components:
        if c.get('name', '').lower() == component_name.lower():
            return c
    
    return None

def fetch_style_details(style_key, token=None):
    """
    Fetch detailed style information from Figma API.
    Endpoint: GET /v1/styles/:key
    Requires: library_assets:read scope
    """
    if not token:
        token = os.environ.get("FIGMA_ACCESS_TOKEN")
    
    if not token:
        return {"error": "FIGMA_ACCESS_TOKEN not found. Set it in .env or environment."}
    
    url = f"https://api.figma.com/v1/styles/{style_key}"
    headers = {"X-Figma-Token": token}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch style details: {str(e)}"}

def query_style_by_name(data, style_name, fetch_details=False):
    """Get info for a specific style by name, optionally fetch full details from API"""
    styles = data.get('published_styles', [])
    
    for s in styles:
        if s.get('name', '').lower() == style_name.lower():
            if fetch_details and s.get('key'):
                # Fetch detailed info from API
                details = fetch_style_details(s.get('key'))
                return {**s, "api_details": details}
            return s
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Query Figma metadata efficiently")
    parser.add_argument("--metadata", default="figma-agent/common/file-metadata.json", 
                       help="Path to metadata file")
    
    subparsers = parser.add_subparsers(dest='command', help='Query commands')
    
    # Summary command
    subparsers.add_parser('summary', help='Get file summary')
    
    # Components command
    comp_parser = subparsers.add_parser('components', help='List components')
    comp_parser.add_argument('--search', help='Search components by name')
    
    # Styles command
    style_parser = subparsers.add_parser('styles', help='List styles')
    style_parser.add_argument('--type', choices=['FILL', 'TEXT', 'EFFECT', 'GRID'], 
                             help='Filter by style type')
    
    # Component detail command
    detail_parser = subparsers.add_parser('component', help='Get component details')
    detail_parser.add_argument('name', help='Component name')
    
    # Style detail command
    style_detail_parser = subparsers.add_parser('style', help='Get style details')
    style_detail_parser.add_argument('name', help='Style name')
    style_detail_parser.add_argument('--fetch-api', action='store_true', 
                                     help='Fetch full details from Figma API (requires token)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Load metadata
    data = load_metadata(args.metadata)
    
    # Execute query
    if args.command == 'summary':
        result = query_summary(data)
    elif args.command == 'components':
        result = query_components(data, args.search)
    elif args.command == 'styles':
        result = query_styles(data, args.type)
    elif args.command == 'component':
        result = query_component_by_name(data, args.name)
    elif args.command == 'style':
        result = query_style_by_name(data, args.name, args.fetch_api)
    
    # Print result as formatted JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
