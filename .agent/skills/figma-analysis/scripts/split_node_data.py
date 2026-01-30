#!/usr/bin/env python3
"""
Split Large Figma Node Data into Logical Chunks

This script splits a large Figma node JSON file into multiple smaller files
organized by component type and hierarchy, making it easier for AI to process.

Features:
- Automatic recursive splitting to keep files at 200-300 lines
- Separate files for different concerns (structure, text, images, etc.)
- Hierarchical organization by component type
- Summary files for quick overview

Usage:
    python3 split_node_data.py <input-file.json> [--output-dir <directory>] [--max-lines <number>]
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

# Configuration
DEFAULT_MAX_LINES = 250  # Target lines per file
MIN_LINES_TO_SPLIT = 200  # Don't split if smaller than this

def extract_text_nodes(node: Dict[str, Any], parent_path: str = "") -> List[Dict[str, Any]]:
    """Extract all text nodes with their context"""
    texts = []
    current_path = f"{parent_path}/{node.get('name', 'unnamed')}"
    
    if node.get('type') == 'TEXT':
        text_data = {
            'id': node.get('id'),
            'name': node.get('name'),
            'path': current_path,
            'layout': node.get('layout'),
            'styles': node.get('styles', {}).get('text'),
            'characters': node.get('styles', {}).get('text', {}).get('characters')
        }
        texts.append(text_data)
    
    # Recurse through children
    for child in node.get('children', []):
        texts.extend(extract_text_nodes(child, current_path))
    
    return texts

def extract_instances(node: Dict[str, Any], parent_path: str = "") -> List[Dict[str, Any]]:
    """Extract all component instances"""
    instances = []
    current_path = f"{parent_path}/{node.get('name', 'unnamed')}"
    
    if node.get('type') == 'INSTANCE':
        instance_data = {
            'id': node.get('id'),
            'name': node.get('name'),
            'path': current_path,
            'layout': node.get('layout'),
            'componentId': node.get('componentId'),
            'children_count': len(node.get('children', []))
        }
        instances.append(instance_data)
    
    # Recurse through children
    for child in node.get('children', []):
        instances.extend(extract_instances(child, current_path))
    
    return instances

def extract_images(node: Dict[str, Any], parent_path: str = "") -> List[Dict[str, Any]]:
    """Extract all image/vector nodes"""
    images = []
    current_path = f"{parent_path}/{node.get('name', 'unnamed')}"
    
    node_type = node.get('type')
    if node_type in ['VECTOR', 'FRAME', 'GROUP'] and 'image' in node.get('name', '').lower():
        image_data = {
            'id': node.get('id'),
            'name': node.get('name'),
            'type': node_type,
            'path': current_path,
            'layout': node.get('layout')
        }
        images.append(image_data)
    
    # Recurse through children
    for child in node.get('children', []):
        images.extend(extract_images(child, current_path))
    
    return images

def extract_colors(node: Dict[str, Any]) -> Dict[str, int]:
    """Extract all unique colors used in the design"""
    colors = defaultdict(int)
    
    # Check fills
    fills = node.get('styles', {}).get('fills', [])
    if isinstance(fills, list):
        for fill in fills:
            if isinstance(fill, dict) and fill.get('type') == 'SOLID':
                color = fill.get('color')
                if color:
                    colors[color] += 1
    elif isinstance(fills, dict):
        # Single fill object
        if fills.get('type') == 'SOLID':
            color = fills.get('color')
            if color:
                colors[color] += 1
    
    # Recurse through children
    for child in node.get('children', []):
        child_colors = extract_colors(child)
        for color, count in child_colors.items():
            colors[color] += count
    
    return dict(colors)

def estimate_json_lines(obj: Any) -> int:
    """Estimate how many lines this object will take when serialized as JSON"""
    try:
        json_str = json.dumps(obj, indent=2, ensure_ascii=False)
        return len(json_str.split('\n'))
    except:
        # Fallback: rough estimate
        return len(str(obj)) // 50

def should_split_node(node: Dict[str, Any], max_lines: int) -> bool:
    """Check if a node should be split into smaller parts"""
    estimated_lines = estimate_json_lines(node)
    return estimated_lines > max_lines

def split_node_recursively(
    node: Dict[str, Any], 
    max_lines: int,
    parent_name: str = ""
) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Recursively split a node into smaller chunks if it's too large
    
    Returns:
        List of (name, node_data) tuples
    """
    estimated_lines = estimate_json_lines(node)
    
    # If small enough, return as-is
    if estimated_lines <= max_lines:
        node_name = node.get('name', 'unnamed')
        return [(node_name, node)]
    
    # If no children, can't split further - return as-is
    children = node.get('children', [])
    if not children:
        node_name = node.get('name', 'unnamed')
        return [(node_name, node)]
    
    # Try to split by children
    result = []
    
    # Group children into chunks that fit max_lines
    current_chunk = []
    current_chunk_lines = 0
    chunk_index = 0
    
    for child in children:
        child_lines = estimate_json_lines(child)
        
        # If single child is too large, split it recursively
        if child_lines > max_lines:
            # First, save current chunk if any
            if current_chunk:
                chunk_name = f"{node.get('name', 'unnamed')}_part{chunk_index}"
                chunk_node = {
                    'id': f"{node.get('id', '')}_part{chunk_index}",
                    'name': chunk_name,
                    'type': node.get('type'),
                    'layout': node.get('layout'),
                    'styles': node.get('styles', {}),
                    'boundVariables': node.get('boundVariables', {}),
                    'children': current_chunk
                }
                result.append((chunk_name, chunk_node))
                current_chunk = []
                current_chunk_lines = 0
                chunk_index += 1
            
            # Recursively split the large child
            child_splits = split_node_recursively(child, max_lines, node.get('name', ''))
            result.extend(child_splits)
            
        # If adding this child would exceed max_lines, start new chunk
        elif current_chunk_lines + child_lines > max_lines and current_chunk:
            chunk_name = f"{node.get('name', 'unnamed')}_part{chunk_index}"
            chunk_node = {
                'id': f"{node.get('id', '')}_part{chunk_index}",
                'name': chunk_name,
                'type': node.get('type'),
                'layout': node.get('layout'),
                'styles': node.get('styles', {}),
                'boundVariables': node.get('boundVariables', {}),
                'children': current_chunk
            }
            result.append((chunk_name, chunk_node))
            current_chunk = [child]
            current_chunk_lines = child_lines
            chunk_index += 1
        else:
            # Add to current chunk
            current_chunk.append(child)
            current_chunk_lines += child_lines
    
    # Save last chunk
    if current_chunk:
        if chunk_index == 0:
            # Only one chunk, use original name
            result.append((node.get('name', 'unnamed'), node))
        else:
            chunk_name = f"{node.get('name', 'unnamed')}_part{chunk_index}"
            chunk_node = {
                'id': f"{node.get('id', '')}_part{chunk_index}",
                'name': chunk_name,
                'type': node.get('type'),
                'layout': node.get('layout'),
                'styles': node.get('styles', {}),
                'boundVariables': node.get('boundVariables', {}),
                'children': current_chunk
            }
            result.append((chunk_name, chunk_node))
    
    return result

def create_structure_tree(node: Dict[str, Any], depth: int = 0, max_depth: int = 3) -> Dict[str, Any]:
    """Create a simplified structure tree (limited depth for overview)"""
    if depth > max_depth:
        return {
            'id': node.get('id'),
            'name': node.get('name'),
            'type': node.get('type'),
            'children_count': len(node.get('children', [])),
            'truncated': True
        }
    
    result = {
        'id': node.get('id'),
        'name': node.get('name'),
        'type': node.get('type'),
        'layout': node.get('layout'),
    }

    
    children = node.get('children', [])
    if children:
        result['children'] = [
            create_structure_tree(child, depth + 1, max_depth)
            for child in children
        ]
        result['children_count'] = len(children)
    
    return result

def split_by_sections(node: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Split top-level children into logical sections"""
    sections = {}
    
    for child in node.get('children', []):
        section_name = child.get('name', 'unnamed').lower()
        # Clean up section name
        section_name = section_name.replace(' ', '_').replace('-', '_')
        
        sections[section_name] = child
    
    return sections

def create_summary(node: Dict[str, Any], texts: List, instances: List, images: List, colors: Dict) -> Dict[str, Any]:
    """Create a comprehensive summary of the node"""
    
    def count_nodes(n):
        count = 1
        for child in n.get('children', []):
            count += count_nodes(child)
        return count
    
    def count_by_type(n, counts=None):
        if counts is None:
            counts = defaultdict(int)
        counts[n.get('type', 'UNKNOWN')] += 1
        for child in n.get('children', []):
            count_by_type(child, counts)
        return dict(counts)
    
    return {
        'name': node.get('name'),
        'id': node.get('id'),
        'type': node.get('type'),
        'layout': node.get('layout'),
        'statistics': {
            'total_nodes': count_nodes(node),
            'text_nodes': len(texts),
            'component_instances': len(instances),
            'images': len(images),
            'unique_colors': len(colors),
            'nodes_by_type': count_by_type(node)
        },
        'top_colors': sorted(colors.items(), key=lambda x: -x[1])[:10],
        'sections': [
            {
                'name': child.get('name'),
                'type': child.get('type'),
                'children_count': len(child.get('children', []))
            }
            for child in node.get('children', [])
        ]
    }

def process_file(input_path: Path, output_dir: Optional[Path] = None, max_lines: int = DEFAULT_MAX_LINES) -> None:
    """Process a Figma node JSON file and split into multiple files"""
    
    print(f"📖 Reading: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both single node and nodes object format
    if 'nodes' in data:
        nodes = data['nodes']
        root_key = list(nodes.keys())[0]
        root_node = nodes[root_key]
    else:
        root_node = data
    
    # Determine output directory
    if output_dir is None:
        output_dir = input_path.parent / f"{input_path.stem}-split"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Extract different aspects
    print(f"\n🔍 Analyzing structure...")
    
    print(f"   📝 Extracting text nodes...")
    texts = extract_text_nodes(root_node)
    
    print(f"   🧩 Extracting component instances...")
    instances = extract_instances(root_node)
    
    print(f"   🖼️  Extracting images...")
    images = extract_images(root_node)
    
    print(f"   🎨 Extracting colors...")
    colors = extract_colors(root_node)
    
    print(f"   📊 Creating structure tree...")
    structure = create_structure_tree(root_node, max_depth=3)
    
    print(f"   📋 Creating summary...")
    summary = create_summary(root_node, texts, instances, images, colors)
    
    # Save files
    print(f"\n💾 Saving files...")
    
    files_created = []
    
    # 1. Summary (most important for AI)
    summary_path = output_dir / "00-summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    files_created.append(("00-summary.json", "Quick overview with statistics"))
    print(f"   ✅ {summary_path.name}")
    
    # 2. Structure tree (limited depth)
    structure_path = output_dir / "01-structure.json"
    with open(structure_path, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    files_created.append(("01-structure.json", "Hierarchical structure (3 levels deep)"))
    print(f"   ✅ {structure_path.name}")
    
    # 3. Text content
    if texts:
        texts_path = output_dir / "02-texts.json"
        with open(texts_path, 'w', encoding='utf-8') as f:
            json.dump({'texts': texts, 'count': len(texts)}, f, indent=2, ensure_ascii=False)
        files_created.append(("02-texts.json", f"All text content ({len(texts)} items)"))
        print(f"   ✅ {texts_path.name}")
    
    # 4. Component instances
    if instances:
        instances_path = output_dir / "03-instances.json"
        with open(instances_path, 'w', encoding='utf-8') as f:
            json.dump({'instances': instances, 'count': len(instances)}, f, indent=2, ensure_ascii=False)
        files_created.append(("03-instances.json", f"Component instances ({len(instances)} items)"))
        print(f"   ✅ {instances_path.name}")
    
    # 5. Images/Icons
    if images:
        images_path = output_dir / "04-images.json"
        with open(images_path, 'w', encoding='utf-8') as f:
            json.dump({'images': images, 'count': len(images)}, f, indent=2, ensure_ascii=False)
        files_created.append(("04-images.json", f"Images and icons ({len(images)} items)"))
        print(f"   ✅ {images_path.name}")
    
    # 6. Color palette
    if colors:
        colors_sorted = sorted(colors.items(), key=lambda x: -x[1])
        colors_path = output_dir / "05-colors.json"
        with open(colors_path, 'w', encoding='utf-8') as f:
            json.dump({
                'colors': [{'color': c, 'usage_count': count} for c, count in colors_sorted],
                'total_unique': len(colors)
            }, f, indent=2, ensure_ascii=False)
        files_created.append(("05-colors.json", f"Color palette ({len(colors)} unique colors)"))
        print(f"   ✅ {colors_path.name}")
    
    # 7. Split by top-level sections with recursive splitting for large sections
    print(f"   📂 Splitting sections (max {max_lines} lines per file)...")
    sections = split_by_sections(root_node)
    
    if sections:
        sections_dir = output_dir / "sections"
        sections_dir.mkdir(exist_ok=True)
        
        total_section_files = 0
        
        for section_name, section_node in sections.items():
            # Check if section needs recursive splitting
            section_lines = estimate_json_lines(section_node)
            
            if section_lines > max_lines:
                # Recursively split large section
                print(f"      ⚠️  {section_name} is large ({section_lines} lines), splitting...")
                splits = split_node_recursively(section_node, max_lines)
                
                for split_name, split_node in splits:
                    # Clean up split name
                    clean_name = split_name.lower().replace(' ', '_').replace('-', '_')
                    section_path = sections_dir / f"{clean_name}.json"
                    
                    with open(section_path, 'w', encoding='utf-8') as f:
                        json.dump(split_node, f, indent=2, ensure_ascii=False)
                    
                    split_lines = estimate_json_lines(split_node)
                    print(f"      ✅ sections/{section_path.name} ({split_lines} lines)")
                    total_section_files += 1
            else:
                # Small enough, save as-is
                section_path = sections_dir / f"{section_name}.json"
                with open(section_path, 'w', encoding='utf-8') as f:
                    json.dump(section_node, f, indent=2, ensure_ascii=False)
                print(f"   ✅ sections/{section_path.name} ({section_lines} lines)")
                total_section_files += 1
        
        files_created.append((f"sections/*.json", f"{total_section_files} section files"))

    
    # 8. Full node tree (for reference)
    full_path = output_dir / "99-full-tree.json"
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(root_node, f, indent=2, ensure_ascii=False)
    files_created.append(("99-full-tree.json", "Complete node tree (use only if needed)"))
    print(f"   ✅ {full_path.name}")
    
    # Create README
    readme_path = output_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f"# {root_node.get('name', 'Component')} - Split Data\n\n")
        f.write(f"**Source:** `{input_path.name}`\n\n")
        f.write(f"## 📊 Statistics\n\n")
        f.write(f"- **Total nodes:** {summary['statistics']['total_nodes']}\n")
        f.write(f"- **Text nodes:** {summary['statistics']['text_nodes']}\n")
        f.write(f"- **Component instances:** {summary['statistics']['component_instances']}\n")
        f.write(f"- **Images:** {summary['statistics']['images']}\n")
        f.write(f"- **Unique colors:** {summary['statistics']['unique_colors']}\n\n")
        
        f.write(f"## 📁 Files\n\n")
        f.write(f"Files are organized by concern for easier AI processing:\n\n")
        for filename, description in files_created:
            f.write(f"- **`{filename}`**: {description}\n")
        
        f.write(f"\n## 🎯 Recommended Reading Order for AI\n\n")
        f.write(f"1. **`00-summary.json`** - Start here for quick overview\n")
        f.write(f"2. **`01-structure.json`** - Understand the hierarchy\n")
        f.write(f"3. **`02-texts.json`** - Get all text content\n")
        f.write(f"4. **`sections/*.json`** - Dive into specific sections as needed\n")
        f.write(f"5. **`99-full-tree.json`** - Only if you need complete details\n\n")
        
        f.write(f"## 🎨 Top Colors\n\n")
        for color, count in summary['top_colors'][:5]:
            f.write(f"- `{color}` - used {count} times\n")
    
    print(f"   ✅ {readme_path.name}")
    
    # Final summary
    print(f"\n✨ Done! Created {len(files_created) + 1} files in: {output_dir.name}/")
    print(f"   Max lines per file: {max_lines}")
    print(f"\n💡 For AI processing, start with: 00-summary.json")
    print(f"   Then read specific files as needed instead of the full tree.\n")

def main():
    parser = argparse.ArgumentParser(
        description='Split large Figma node JSON files into logical chunks (200-300 lines each)'
    )
    parser.add_argument('input', type=str, help='Input JSON file path')
    parser.add_argument('--output-dir', '-o', type=str, help='Output directory (optional)')
    parser.add_argument(
        '--max-lines', '-m', 
        type=int, 
        default=DEFAULT_MAX_LINES,
        help=f'Maximum lines per file (default: {DEFAULT_MAX_LINES})'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        sys.exit(1)
    
    output_dir = Path(args.output_dir) if args.output_dir else None
    
    print(f"⚙️  Configuration:")
    print(f"   Max lines per file: {args.max_lines}")
    print(f"   Input: {input_path.name}")
    print()
    
    process_file(input_path, output_dir, args.max_lines)

if __name__ == '__main__':
    main()

