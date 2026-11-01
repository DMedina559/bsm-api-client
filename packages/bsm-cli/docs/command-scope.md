# CLI command scope

The CLI prioritizes operational workflows. Every command in the reviewed tree is inventoried below, including the removed paths for migration. Commands marked Removed have been deleted; use the listed replacement instead. All HTTP operations remain available in `api explore` and `api call`; the SDK remains complete.

Examples:

```sh
bsm-cli auth whoami
bsm-cli auth verify
bsm-cli api call list_passkeys
bsm-cli api call get_account_server_access --param user_id=2
bsm-cli api explore
```

Authentication prompts for an OTP only after a server MFA challenge and only in an interactive terminal. JSON/noninteractive commands return actionable errors without prompting. Browser WebAuthn registration/sign-in stays in the frontend. Passkey-only accounts cannot fall back to password-only CLI login.

| Command | Decision | Reason / replacement |
| --- | --- | --- |
| `access passkeys` | Removed; use replacement | api explore for account grants and administrator security operations |
| `access reset-mfa` | Removed; use replacement | api explore for account grants and administrator security operations |
| `access servers` | Removed; use replacement | api explore for account grants and administrator security operations |
| `access sessions` | Removed; use replacement | api explore for account grants and administrator security operations |
| `access set` | Removed; use replacement | api explore for account grants and administrator security operations |
| `access show` | Removed; use replacement | api explore for account grants and administrator security operations |
| `access signout` | Removed; use replacement | api explore for account grants and administrator security operations |
| `account change-password` | Removed; use replacement | auth whoami / auth change-password, or api call for profile/theme edits |
| `account details` | Removed; use replacement | auth whoami / auth change-password, or api call for profile/theme edits |
| `account update-profile` | Removed; use replacement | auth whoami / auth change-password, or api call for profile/theme edits |
| `account update-theme` | Removed; use replacement | auth whoami / auth change-password, or api call for profile/theme edits |
| `addon install` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `addon manage` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `allowlist add` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `allowlist list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `allowlist remove` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `api call` | Keep | HTTP discovery and request tooling |
| `api diff` | Keep | HTTP discovery and request tooling |
| `api download` | Keep | HTTP discovery and request tooling |
| `api explore` | Keep | HTTP discovery and request tooling |
| `api export` | Keep | HTTP discovery and request tooling |
| `api info` | Keep | HTTP discovery and request tooling |
| `api model` | Keep | HTTP discovery and request tooling |
| `api models` | Keep | HTTP discovery and request tooling |
| `api operation` | Keep | HTTP discovery and request tooling |
| `api operations` | Keep | HTTP discovery and request tooling |
| `api refresh` | Keep | HTTP discovery and request tooling |
| `api schema` | Keep | HTTP discovery and request tooling |
| `appearance set` | Keep | Terminal preferences |
| `appearance show` | Keep | Terminal preferences |
| `audit` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth activity` | Removed; use replacement | api call list_security_activity |
| `auth change-password` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth devices forget` | Removed; use replacement | api call list_trusted_devices / revoke_trusted_device / revoke_trusted_devices |
| `auth devices list` | Removed; use replacement | api call list_trusted_devices / revoke_trusted_device / revoke_trusted_devices |
| `auth login` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth logout` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth mfa confirm` | Removed; use replacement | web UI for enrollment and recovery; api explore for scripted management |
| `auth mfa disable` | Removed; use replacement | web UI for enrollment and recovery; api explore for scripted management |
| `auth mfa enroll` | Removed; use replacement | web UI for enrollment and recovery; api explore for scripted management |
| `auth mfa recovery-codes` | Removed; use replacement | web UI for enrollment and recovery; api explore for scripted management |
| `auth mfa status` | Removed; use replacement | web UI for enrollment and recovery; api explore for scripted management |
| `auth passkeys list` | Removed; use replacement | web UI for WebAuthn; api explore for credential metadata |
| `auth passkeys rename` | Removed; use replacement | web UI for WebAuthn; api explore for credential metadata |
| `auth passkeys revoke` | Removed; use replacement | web UI for WebAuthn; api explore for credential metadata |
| `auth sessions list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth sessions rename` | Removed; use replacement | api call rename_login_session |
| `auth sessions revoke` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth sessions revoke-all` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth setup` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth tokens create` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth tokens list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth tokens revoke` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth tokens rotate` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth verify` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `auth whoami` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup annotate` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup cleanup-destination` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup create` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup download` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup dry-run` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup health` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup import` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup inspect` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup manage` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup prepare-copy` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup prune` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup report` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup restore` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `backup schedule` | Removed; use replacement | scheduler save |
| `backup upload` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `bans add` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `bans list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `bans remove` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `content upload` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `diagnostics activity` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `diagnostics compare` | Removed; use replacement | api call compare_diagnostic_snapshots |
| `diagnostics history` | Removed; use replacement | api call get_diagnostic_history |
| `diagnostics report` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `diagnostics runs` | Removed; use replacement | api explore for diagnostic runs |
| `diagnostics snapshot` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `diagnostics trace` | Removed; use replacement | api explore for diagnostic traces |
| `events activity` | Removed; use replacement | api explore for event catalogs and activity |
| `events catalog` | Removed; use replacement | api explore for event catalogs and activity |
| `health` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `logs` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `monitor` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `operations list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `operations show` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `overview` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `permissions list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `permissions set` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `player add` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `player scan` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin call` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin disable` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin enable` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin operations` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin reload` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin settings edit` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin settings set` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin settings show` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `plugin trigger-event` | Removed; use replacement | api call trigger_plugin_event |
| `properties get` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `properties raw` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `properties set` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `runtime` | Removed; use replacement | api call get_web_runtime |
| `scheduler control` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `scheduler list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `scheduler remove` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `scheduler save` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server delete` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server install` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server list` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server monitor` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server restart` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server send-command` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server settings` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server start` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server stop` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `server update` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `settings` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `shutdown` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `users delete` | Removed; use replacement | api explore for user administration |
| `users disable` | Removed; use replacement | api explore for user administration |
| `users enable` | Removed; use replacement | api explore for user administration |
| `users invite` | Removed; use replacement | api explore for user administration |
| `users list` | Removed; use replacement | api explore for user administration |
| `users set-role` | Removed; use replacement | api explore for user administration |
| `world export` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `world install` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |
| `world reset` | Keep | Operational workflow, formatted inspection, file transfer, validation or confirmation |

## Removal impact

38 redundant leaf commands were removed, together with their orphaned groups and menu entries. They are not hidden aliases. The HTTP operation catalog and SDK remain complete. `auth whoami` and `auth change-password` replace the retained account workflows; `scheduler save` replaces the duplicate backup schedule command.
