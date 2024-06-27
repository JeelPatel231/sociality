from pyrogram import filters
from bot import app


def command(command: str, prefix: str = "/", case_sensitive: bool = False):
    return filters.command(
        commands=[command, f"{command}@{app.me.username}"],
        prefixes=prefix,
        case_sensitive=case_sensitive
    )
