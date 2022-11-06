from typing import List
import hashlib

#url to view function mappers.
def map_urls(app_inst, urls: List[List]):
	for maps in urls:
		if len(maps) >= 3:
			url, view_func, methods = maps
			app_inst.route(url, methods=methods)(view_func)
		else:
			url, view = maps
			app_inst.route(url)(view)
			
def slugify(link_str):
	s = "-".join(link_str.lower().split(" ")[:8])+"..."
	return s

def get_hash_string_SHA256(string):
	'''Function for encoding a string using SHA-256'''
	hashed = hashlib.sha256(string.encode())
	result = hashed.hexdigest()
	return result