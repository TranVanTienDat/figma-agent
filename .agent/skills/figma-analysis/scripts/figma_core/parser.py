
class NodeEnricher:
    """
    Enriches raw Figma nodes with resolved Design Tokens and Component names.
    Inspired by 'Deep Extract v3.0'.
    """
    def __init__(self, variables_map=None, components_map=None):
        self.variables_map = variables_map or {}
        self.components_map = components_map or {}

    def rgba_to_hex(self, color):
        if not color: return None
        r = int(color.get('r', 0) * 255)
        g = int(color.get('g', 0) * 255)
        b = int(color.get('b', 0) * 255)
        a = color.get('a', 1)
        
        if a >= 1:
            return f"#{r:02x}{g:02x}{b:02x}"
        else:
            return f"rgba({r}, {g}, {b}, {a:.2f})"

    def enrich_node(self, node):
        """
        Recursively processes a node to creating a Simplified, Enriched version.
        """
        result = {
            "id": node.get("id"),
            "name": node.get("name"),
            "type": node.get("type"),
            "layout": {
                "width": node.get("absoluteBoundingBox", {}).get("width"),
                "height": node.get("absoluteBoundingBox", {}).get("height"),
                "x": node.get("absoluteBoundingBox", {}).get("x"),
                "y": node.get("absoluteBoundingBox", {}).get("y"),
            },
            "styles": {},
            "boundVariables": {},
            "children": []
        }

        # 1. Resolve Bound Variables (Tokens)
        bound_vars = node.get("boundVariables", {})
        for prop, binding in bound_vars.items():
            # Handle array bindings or single objects
            # Warning: Python dict keys for bindings might vary
            if isinstance(binding, dict):
                 var_id = binding.get("id")
                 if var_id and var_id in self.variables_map:
                     result["boundVariables"][prop] = {
                         "tokenName": self.variables_map[var_id]["name"],
                         "value": self.variables_map[var_id]["value"]
                     }

        # 2. Enrich Fills (Backgrounds)
        fills = node.get("fills", [])
        if fills:
            result["styles"]["fills"] = []
            for fill in fills:
                if fill.get("visible", True) is False: continue
                
                fill_data = {
                    "type": fill.get("type"),
                    "opacity": fill.get("opacity", 1)
                }
                if "color" in fill:
                    fill_data["color"] = self.rgba_to_hex(fill["color"])
                    
                result["styles"]["fills"].append(fill_data)

        # 3. Enrich Text
        if node.get("type") == "TEXT":
            style = node.get("style", {})
            result["styles"]["text"] = {
                "characters": node.get("characters"),
                "fontFamily": style.get("fontFamily"),
                "fontWeight": style.get("fontWeight"),
                "fontSize": style.get("fontSize"),
                "textAlign": style.get("textAlignHorizontal"),
                "lineHeight": style.get("lineHeightPx")
            }

        # 4. Enrich Component Info
        comp_id = node.get("componentId")
        if comp_id and comp_id in self.components_map:
            result["componentName"] = self.components_map[comp_id]["name"]
            result["componentDescription"] = self.components_map[comp_id].get("description")

        # Recursion
        if "children" in node:
            for child in node["children"]:
                result["children"].append(self.enrich_node(child))

        return result


class FigmaParser:
    """
    Utility for parsing the full Figma document tree.
    """
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def flatten_tree(self, node=None):
        """
        Flattens the Figma document tree into a list of nodes.
        """
        if node is None:
            # Handle both full file response and subset node response
            node = self.raw_data.get("document", self.raw_data)
            if not node: return []

        nodes = [node]
        if "children" in node:
            for child in node["children"]:
                nodes.extend(self.flatten_tree(child))
        return nodes

class DesignTokenExtractor:
    """
    Extracts 'Local Styles' by analyzing the raw usage of properties on nodes.
    Useful when 'Get File Styles' API returns empty (no published library).
    """
    def __init__(self, nodes):
        self.nodes = nodes
        self.colors = {}     # Hex -> {count, usage_examples}
        self.typography = {} # key -> {fontFamily, fontSize, ...}
        
    def extract(self):
        for node in self.nodes:
            self._scan_colors(node)
            self._scan_typography(node)
            
        return {
            "colors": self._format_most_used(self.colors, "color"),
            "typography": self._format_most_used(self.typography, "text"),
        }
    
    def _scan_colors(self, node):
        # Scan fills
        for fill in node.get("fills", []):
            if fill.get("type") == "SOLID" and fill.get("visible", True):
                color = self._rgba_to_hex(fill.get("color"))
                if color:
                    if color not in self.colors:
                        self.colors[color] = {"value": color, "count": 0}
                    self.colors[color]["count"] += 1
                    
        # Scan strokes
        for stroke in node.get("strokes", []):
            if stroke.get("type") == "SOLID" and stroke.get("visible", True):
                color = self._rgba_to_hex(stroke.get("color"))
                if color:
                    if color not in self.colors:
                        self.colors[color] = {"value": color, "count": 0}
                    self.colors[color]["count"] += 1

    def _scan_typography(self, node):
        if node.get("type") == "TEXT":
            style = node.get("style", {})
            # Create a unique key for this font style
            key = f"{style.get('fontFamily')}-{style.get('fontSize')}-{style.get('fontWeight')}"
            
            if key not in self.typography:
                self.typography[key] = {
                    "fontFamily": style.get("fontFamily"),
                    "fontSize": style.get("fontSize"),
                    "fontWeight": style.get("fontWeight"),
                    "lineHeight": style.get("lineHeightPx"),
                    "letterSpacing": style.get("letterSpacing"),
                    "count": 0
                }
            self.typography[key]["count"] += 1

    def _format_most_used(self, source_dict, type_name):
        # Sort by usage count
        sorted_items = sorted(source_dict.values(), key=lambda x: x["count"], reverse=True)
        return sorted_items

    def _rgba_to_hex(self, color):
        if not color: return None
        r = int(color.get('r', 0) * 255)
        g = int(color.get('g', 0) * 255)
        b = int(color.get('b', 0) * 255)
        # We ignore alpha for simple hex tokens, or could handle alpha separately
        return f"#{r:02x}{g:02x}{b:02x}"
