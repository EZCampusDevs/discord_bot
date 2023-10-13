# Copyright (C) 2022-2023 EZCampus 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os
import datetime
import logging
import asyncio

import dotenv

from aiohttp import ClientSession 

import discord
from discord.ext import commands

from . import logging_util
from . import constants
from . import data_util
from . import bot_util
from . import bot_cogs
from . import ezcampus_api


def get_and_prase_args(args):
    import argparse

    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]...",
        add_help=False,
    )

    general = parser.add_argument_group("General Options")
    general.add_argument(
        "-h",
        "--help",
        action="help",
        help="Print this help message and exit",
    )

    general.add_argument("-L", "--loglevel", dest="log_level", help=f"Set the log level, {logging_util.get_level_map_pretty()}")
    general.add_argument("-f", "--logfile", dest="log_file", help="Set the NAME of the logfile, will be put in the log directory")
    general.add_argument("-D", "--logdir", dest="log_dir", help="Set the log directroy")

    return parser.parse_args(args)


async def _main(token: str, prefix: str, testing_guild_id:int|None=None):

    async with ClientSession() as our_client:
        
        ezcampus_api.Search.instance(our_client)

        exts = bot_cogs.ALL_COGS

        intents = discord.Intents.default()
        
        intents.message_content = True

        async with bot_util.BotClient(
            web_client=our_client,
            cogs_to_load=exts,
            intents=intents,
            testing_guild_id=testing_guild_id,
            command_prefix=prefix
        ) as bot:
            await bot.start(token)

def main():
    
    dotenv.load_dotenv()

    parsed_args = get_and_prase_args(sys.argv[1:])
    
    time = datetime.datetime.strftime( datetime.datetime.now(), "%Y-%m-%d_%H-%M-%S")
    
    log_dir = parsed_args.log_dir or os.getenv("LOG_DIR", "./logs")
    log_file = parsed_args.log_file or os.getenv("LOG_FILE", f"{constants.BRAND}{time}.log")
    log_path = os.path.join(log_dir, log_file)
    
    log_level = parsed_args.log_level or os.getenv("LOG_LEVEL", str(logging.INFO))
    log_level = data_util.parse_int(log_level, -1)
    
    assert log_level in logging_util.LOG_LEVEL_MAP, f"Unknown log level {log_level}"

    logging_util.setup_logging(log_file=log_path, log_level=log_level)
    logging_util.add_unhandled_exception_hook()
    
    logging.info("Starting...")
    logging.info(f"--- {constants.BRAND} ---")
    logging.info(f"--- {len(constants.BRAND) * ' '} ---")
    logging.info(f"Date Time: {time}")
    logging.info(f"Logging to {log_path}")

    token = os.getenv("BOT_TOKEN")
    test_guild_id = os.getenv("TESTING_GUILD_ID", None)
    prefix = ".."

    try:

        asyncio.run(_main(token, prefix, testing_guild_id=test_guild_id))
        
    except KeyboardInterrupt:
        logging.error("Keyboard interrupt. Exiting...")
        
    finally:
        pass
