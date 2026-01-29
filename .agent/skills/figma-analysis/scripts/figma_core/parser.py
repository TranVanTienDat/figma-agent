
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
