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

from discord.ext import commands

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot_util import BotClient

class BaseCog(commands.Cog):
    """ Base Nyaa Cog Class, all cogs should inherit from this """

    ezcampus_cog = True
    
    def __init__(self, bot: "BotClient") -> None:
        self.bot: "BotClient" = bot
        
        self.setup()

    def setup(self) -> None:
        """ Called inside __init__ """

    def shutdown(self) -> None:
        """ Perform cleanup """
    
    async def cog_check(self, ctx: commands.Context):
        """A local check which applies to all commands in this cog."""
        return True

    async def cog_command_error(self, ctx: commands.Context, error):
        """A local error handler for all errors arising from commands in this cog."""

        logging.error(error, exc_info=True)
