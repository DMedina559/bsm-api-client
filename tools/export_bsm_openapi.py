"""Export the installed backend's canonical core contract.

Install bedrock-server-manager[contract] from the target backend checkout first.
The backend owns schema dependency versions and normalization rules.
"""

from bedrock_server_manager.web.contract import main

if __name__ == "__main__":
    main()
