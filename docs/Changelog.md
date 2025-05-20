# pybedrock-server-manager Changelog

# 0.5.0
1. Made port optional

# 0.4.0
1. Added verify ssl option

# 0.3.0
1. Added missing imports

# 0.2.0
1. Added use_ssl parameter to __init__ for HTTPS connections
2. Method Renames for Clarity:
	- async_get_servers() split into:
	- async_get_servers_details() -> List[Dict[str, Any]] (returns full server objects).
	- async_get_server_names() -> List[str] (returns just a list of names).
3. Added input validation to several methods (e.g., for backup_type, restore_type, empty commands, permission levels, player data format) to raise ValueError before making an API call with invalid data.
4. Enhanced docstrings for some methods to detail parameters, return types, corresponding API endpoints, authentication requirements, and potential exceptions
5. Consistent use of json_data when calling self._request

# 0.1.0
1. Initial release