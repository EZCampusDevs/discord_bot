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

import logging
from typing import Optional

import discord
from discord.ext import commands

import aiohttp


from . import bot_cogs

class BotClient(commands.Bot):
    
    EMBED_STANDARD_COLOR = 0xBCD0F7
    
    BOT_PERMISSION_NUMBER = 1102128924672 # 2147502080
    
    """
    1102128924672 gives:

    Manage Roles
    Change Nickname
    Manage Nicknames
    Moderate Members
    Embed Links
    Attach Files
    Use Slash Commands
    Send Messages
    
    """

    
    def __init__(
        self,
        *args,
        cogs_to_load: list[bot_cogs.BaseCog],
        web_client: aiohttp.ClientSession,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.web_client: aiohttp.ClientSession = web_client

        self.testing_guild_id: int = testing_guild_id

        self.cogs_to_load: list[bot_cogs.BaseCog] = cogs_to_load

        self.loaded_cogs: list[bot_cogs.BaseCog] = []
        
    async def post_setup(self) -> None:
        
        for cog in self.loaded_cogs:

            try:

                cog.post_setup()

            except Exception as e:

                logging.error(e, stack_info=True)
                logging.error(f"Could not load cog {cog}")

    async def setup_hook(self) -> None:

        for extension in self.cogs_to_load:
            
            try:
                cog = extension(self)

                await self.add_cog(cog)
                
                logging.info(f"Loaded cog {cog}")

                self.loaded_cogs.append(cog)

            except Exception as e:

                logging.error(e, stack_info=True)
                logging.error(f"Could not load cog {extension}")


        if self.testing_guild_id:
            
            logging.info(f"Setting testing guild to {self.testing_guild_id}")

            guild = discord.Object(self.testing_guild_id)

            self.tree.copy_global_to(guild=guild)

            await self.tree.sync(guild=guild)
