<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/dmedina559/bedrock-server-manager/main/src/bedrock_server_manager/web/static/image/icon/favicon.svg" alt="BSM Logo" width="150">
</div>

# bsm-api-client Changelog

# 1.2.1
1. Removed cleanup

# 1.2.0
1. Added support for BSM 3.5.0
2. Added CLI client
	- Use `pip install bsm-api-client[cli]`
	- Run commands with `bsm-api-client`
3. Refactored client to use pydantic models
4. Removed various methods that no longer exist in the current version of BSM (3.5.7)

# 1.1.0
1. Added BSM 3.4.0 support
2. Added methogs for plugin endpoints 

# 1.0.1

1. Changed allowlist remove to use updated route from BSM 3.3.0.
   - Corresponds to `DELETE /api/server/{server_name}/allowlist/remove`.
	- Allows removing multiple players from the allowlist at once.
2. Updated restore methods to use the new BSM 3.3.0 types for `restore_type`:
   - `world` -> `world`
   - `config` -> `permissions`
   - `config` -> `properties`
   - `config` -> `allowlist`

# 1.0.0

> [!IMPORTANT]
> BREAKING CHANGES:
>  - Renamed pybedrock-server-manager to bsm-api-client
>     * Point your imports from `pybedrock_server_manager` to `bsm_api_client`
>  - The variables `async_list_server_backups` accepts for `backup_type` has been changed to `allowlist`, `permissions`,`properties`,`world`, `all`
>     * You should lock your curently installed version to 0.5.1 or lower if you want to keep using the old values until you update to BSM 3.3.0+

1. Added support for Bedrock Server Manager (BSM) 3.3.0
2. Added `async_reset_server_world`
   - Corresponds to `DELETE /api/server/{server_name}/world/reset`. 

# 0.5.1

1. Logger changes for when using ssl

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