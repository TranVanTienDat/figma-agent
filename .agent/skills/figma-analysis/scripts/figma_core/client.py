
import requests
import json
import os
import sys

class FigmaClient:
    """
    A robust client for interacting with the Figma REST API.
    Documentation: https://developers.figma.com/docs/rest-api/
    """
    BASE_URL = "https://api.figma.com/v1"

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "X-Figma-Token": access_token
        }

    def _request(self, method, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Handle specific 403 error for Variables (Enterprise only) gracefully
            if response.status_code == 403 and "variables" in endpoint:
                print(f"[!] Warning: Variables API access denied (requires Enterprise plan). Skipping.")
                return None
            print(f"[!] HTTP Error ({response.status_code}) for {url}: {e}")
            raise e

    def get_file_nodes(self, file_key, node_ids, depth=None):
        """
        GET /v1/files/:key/nodes
        """
        if isinstance(node_ids, list):
            node_ids = ",".join(node_ids)
            
        params = {
            'ids': node_ids,
            'geometry': 'paths', # Get vector paths
            'plugin_data': 'shared' # Get plugin data
        }
        if depth is not None: params['depth'] = depth

        return self._request("GET", f"/files/{file_key}/nodes", params=params)

    def get_local_variables(self, file_key):
        """
        GET /v1/files/:key/variables/local
        Fetches local variables (Design Tokens). Enterprise only.
        """
        return self._request("GET", f"/files/{file_key}/variables/local")

    def get_file_styles(self, file_key):
        """
        GET /v1/files/:key/styles
        """
        return self._request("GET", f"/files/{file_key}/styles")

    def get_file_components(self, file_key):
        """
        GET /v1/files/:key/components
        """
        return self._request("GET", f"/files/{file_key}/components")

    def get_images(self, file_key, node_ids, format='svg', scale=1):
        """
        GET /v1/images/:key
        """
        if isinstance(node_ids, list):
            node_ids = ",".join(node_ids)
            
        params = {
            'ids': node_ids,
            'format': format,
            'scale': scale
        }
        return self._request("GET", f"/images/{file_key}", params=params)

    # Legacy method support
    def get_file(self, file_key, depth=None):
        params = {}
        if depth: params['depth'] = depth
        return self._request("GET", f"/files/{file_key}", params=params)

    def get_image_fills(self, file_key):
        return self._request("GET", f"/files/{file_key}/images")

    def get_published_components(self, file_key):
         return self.get_file_components(file_key)

    def get_published_styles(self, file_key):
         return self.get_file_styles(file_key)
