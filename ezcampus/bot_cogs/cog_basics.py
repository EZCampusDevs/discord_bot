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

import discord
from discord.ext import commands

from . import BaseCog

class BasicsCog(BaseCog):
    
    def setup(self) -> None:

        self.INVITE_URL = f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions={self.bot.BOT_PERMISSION_NUMBER}&scope=bot"


    @commands.hybrid_command(
            name='invite', 
            aliases=['getinvite'],
            description="Get an invite link for the bot")
    async def invite_(self, ctx: commands.Context): 

        embed = discord.Embed(color = self.bot.EMBED_STANDARD_COLOR)
        
        embed.add_field(
            name="Invite Link", 
            value=f"You can invite me to servers using the following [Link]({self.INVITE_URL})")

        await ctx.send(embed=embed)



