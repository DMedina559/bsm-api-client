import os

import click
import questionary
from questionary import Separator

from bsm_api_client.models import (
    AddonActionPayload,
    AddonReorderPayload,
    AddonSubpackPayload,
    FileNamePayload,
)

from .decorators import monitor_task, pass_async_context


@click.group()
def addon():
    """Manages server addons."""
    pass


@addon.command("install")
@click.option(
    "-s", "--server", "server_name", required=True, help="Name of the target server."
)
@click.option(
    "-f",
    "--file",
    "addon_file_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="Path to the addon file (.mcpack, .mcaddon); skips interactive menu.",
)
@pass_async_context
async def install_addon(ctx, server_name: str, addon_file_path: str):
    """Installs a behavior or resource pack addon to a specified server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        selected_addon_path = addon_file_path

        if not selected_addon_path:
            click.secho(
                f"Entering interactive addon installation for server: {server_name}",
                fg="yellow",
            )
            response = await client.async_get_content_addons()
            available_files = response.files

            if not available_files:
                click.secho(
                    "No addon files found in the content/addons directory. Nothing to install.",
                    fg="yellow",
                )
                return

            file_map = {os.path.basename(f): f for f in available_files}
            choices = sorted(list(file_map.keys())) + ["Cancel"]
            selection = await questionary.select(
                "Select an addon to install:", choices=choices
            ).ask_async()

            if not selection or selection == "Cancel":
                raise click.Abort()
            selected_addon_path = file_map[selection]

        addon_filename = os.path.basename(selected_addon_path)
        click.echo(f"Installing addon '{addon_filename}' to server '{server_name}'...")

        payload = FileNamePayload(filename=addon_filename)
        response = await client.async_install_server_addon(server_name, payload)
        if response.task_id:
            await monitor_task(
                client,
                response.task_id,
                f"Addon '{addon_filename}' installed successfully",
                "Failed to install addon",
            )
        elif response.status == "success":
            click.secho(f"Addon '{addon_filename}' installed successfully.", fg="green")
        else:
            click.secho(f"Failed to install addon: {response.message}", fg="red")

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@addon.command("manage")
@click.option(
    "-s", "--server", "server_name", required=True, help="Name of the target server."
)
@pass_async_context
async def manage_addons(ctx, server_name: str):  # noqa: C901
    """Interactively manages installed addons on a specified server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    while True:
        try:
            response = await client.async_get_server_addons(server_name)
            addons = response.addons
            if not addons:
                click.secho(
                    "Failed to fetch installed addons or no addons returned.", fg="red"
                )
                return

            bp = addons.behavior_packs or []
            rp = addons.resource_packs or []

            click.clear()
            click.secho(
                f"--- Manage Addons for {server_name} ---", fg="magenta", bold=True
            )

            from questionary import Choice

            menu_choices: list[Choice | Separator | str] = [
                Separator("--- Behavior Packs ---")
            ]

            for idx, pack in enumerate(bp, 1):
                status = "🟢" if pack.status == "ACTIVE" else "⚪"
                menu_choices.append(
                    Choice(
                        f"{idx}. {status} [BP] {pack.name} (v{'.'.join(map(str, pack.version))})",
                        value=f"{idx}. {status} [BP] {pack.name} (v{'.'.join(map(str, pack.version))})",
                    )
                )

            menu_choices.append(Separator("--- Resource Packs ---"))
            for idx, pack in enumerate(rp, 1):
                status = "🟢" if pack.status == "ACTIVE" else "⚪"
                menu_choices.append(
                    Choice(
                        f"{idx}. {status} [RP] {pack.name} (v{'.'.join(map(str, pack.version))})",
                        value=f"{idx}. {status} [RP] {pack.name} (v{'.'.join(map(str, pack.version))})",
                    )
                )

            menu_choices.extend(
                [
                    Separator("--- Actions ---"),
                    Choice("Reorder Behavior Packs", value="Reorder Behavior Packs"),
                    Choice("Reorder Resource Packs", value="Reorder Resource Packs"),
                    Choice("Back", value="Back"),
                ]
            )

            choice = await questionary.select(
                "Select an addon to manage or an action:", choices=menu_choices
            ).ask_async()

            if not choice or choice == "Back":
                return

            if choice == "Reorder Behavior Packs":
                active_bp = [p for p in bp if p.status == "ACTIVE"]
                if not active_bp:
                    click.secho("No active behavior packs to reorder.", fg="yellow")
                    await questionary.press_any_key_to_continue().ask_async()
                    continue

                from typing import List

                ordered_uuids: List[str] = []
                remaining_bp = list(active_bp)

                while remaining_bp:
                    choices = [f"{p.name} ({p.uuid})" for p in remaining_bp]
                    selected_str = await questionary.select(
                        f"Select pack for position {len(ordered_uuids) + 1}:",
                        choices=choices,
                    ).ask_async()
                    if not selected_str:
                        break

                    uuid = selected_str.split("(")[-1].replace(")", "")
                    ordered_uuids.append(uuid)
                    remaining_bp = [p for p in remaining_bp if p.uuid != uuid]

                if len(ordered_uuids) == len(active_bp):
                    payload = AddonReorderPayload(
                        pack_type="behavior", uuids=ordered_uuids
                    )
                    res = await client.async_reorder_server_addon(server_name, payload)
                    if res.task_id:
                        await monitor_task(
                            client,
                            res.task_id,
                            "Reorder successful",
                            "Failed to reorder",
                        )
                    else:
                        click.secho("Reordered successfully.", fg="green")
                else:
                    click.secho("Reorder cancelled.", fg="yellow")

                await questionary.press_any_key_to_continue().ask_async()
                continue

            if choice == "Reorder Resource Packs":
                active_rp = [p for p in rp if p.status == "ACTIVE"]
                if not active_rp:
                    click.secho("No active resource packs to reorder.", fg="yellow")
                    await questionary.press_any_key_to_continue().ask_async()
                    continue

                ordered_uuids = []
                remaining_rp = list(active_rp)

                while remaining_rp:
                    choices = [f"{p.name} ({p.uuid})" for p in remaining_rp]
                    selected_str = await questionary.select(
                        f"Select pack for position {len(ordered_uuids) + 1}:",
                        choices=choices,
                    ).ask_async()
                    if not selected_str:
                        break

                    uuid = selected_str.split("(")[-1].replace(")", "")
                    ordered_uuids.append(uuid)
                    remaining_rp = [p for p in remaining_rp if p.uuid != uuid]

                if len(ordered_uuids) == len(active_rp):
                    payload = AddonReorderPayload(
                        pack_type="resource", uuids=ordered_uuids
                    )
                    res = await client.async_reorder_server_addon(server_name, payload)
                    if res.task_id:
                        await monitor_task(
                            client,
                            res.task_id,
                            "Reorder successful",
                            "Failed to reorder",
                        )
                    else:
                        click.secho("Reordered successfully.", fg="green")
                else:
                    click.secho("Reorder cancelled.", fg="yellow")

                await questionary.press_any_key_to_continue().ask_async()
                continue

            # Handle specific pack
            is_bp = "[BP]" in choice
            pack_type = "behavior" if is_bp else "resource"
            pack_name = choice.split("] ")[1].split(" (v")[0]

            pack = next((p for p in (bp if is_bp else rp) if p.name == pack_name), None)

            if not pack:
                continue

            pack_menu = []
            if pack.status == "ACTIVE":
                pack_menu.append("Disable")
                if pack.subpacks:
                    pack_menu.append("Change Subpack")
            else:
                pack_menu.append("Enable")

            pack_menu.extend(["Uninstall", "Back"])

            action_choice = await questionary.select(
                f"Actions for {pack.name}:", choices=pack_menu
            ).ask_async()

            if not action_choice or action_choice == "Back":
                continue

            if action_choice == "Enable":
                res = await client.async_enable_server_addon(
                    server_name,
                    AddonActionPayload(pack_uuid=pack.uuid, pack_type=pack_type),
                )
                if res.task_id:
                    await monitor_task(
                        client, res.task_id, "Enabled successfully", "Failed to enable"
                    )
            elif action_choice == "Disable":
                res = await client.async_disable_server_addon(
                    server_name,
                    AddonActionPayload(pack_uuid=pack.uuid, pack_type=pack_type),
                )
                if res.task_id:
                    await monitor_task(
                        client,
                        res.task_id,
                        "Disabled successfully",
                        "Failed to disable",
                    )
            elif action_choice == "Uninstall":
                if await questionary.confirm(
                    f"Are you sure you want to uninstall {pack.name}?"
                ).ask_async():
                    res = await client.async_uninstall_server_addon(
                        server_name,
                        AddonActionPayload(pack_uuid=pack.uuid, pack_type=pack_type),
                    )
                    if res.task_id:
                        await monitor_task(
                            client,
                            res.task_id,
                            "Uninstalled successfully",
                            "Failed to uninstall",
                        )
            elif action_choice == "Change Subpack":
                subpack_choices = []
                default_sp = None
                for sp in pack.subpacks:
                    sp_name = sp.get("name") or sp.get("folder_name")
                    if pack.active_subpack == sp.get("folder_name"):
                        sp_name += " (Active)"
                        default_sp = sp_name
                    subpack_choices.append(sp_name)

                sp_choice = await questionary.select(
                    "Select new subpack:", choices=subpack_choices, default=default_sp
                ).ask_async()

                if sp_choice:
                    clean_sp_choice = sp_choice.replace(" (Active)", "")
                    selected_sp = next(
                        (
                            sp
                            for sp in pack.subpacks
                            if sp.get("name") == clean_sp_choice
                            or sp.get("folder_name") == clean_sp_choice
                        ),
                        None,
                    )
                    if selected_sp:
                        subpack_payload = AddonSubpackPayload(
                            pack_uuid=pack.uuid,
                            pack_type=pack_type,
                            subpack_name=selected_sp.get("folder_name"),
                        )
                        setattr(
                            subpack_payload,
                            f"subpack_{pack.uuid}",
                            selected_sp.get("folder_name"),
                        )

                        res = await client.async_update_server_addon_subpack(
                            server_name, subpack_payload
                        )
                        if res.task_id:
                            await monitor_task(
                                client,
                                res.task_id,
                                "Subpack updated successfully",
                                "Failed to update subpack",
                            )

        except Exception as e:
            click.secho(f"An error occurred: {e}", fg="red")
            await questionary.press_any_key_to_continue().ask_async()
