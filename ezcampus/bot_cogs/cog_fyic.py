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
import json

import aiohttp

import discord
from discord.ext import commands

from . import BaseCog

from .. import ezcampus_api

class FYICCog(BaseCog):
    
    """
    
    A cog to provide commands for the FYIC event
    
    """
    
    FYIC_GUILD_ID: int = 1161735662249201707
    VERIFIED_ROLE_ID: int = 1161736593304998009
    fyic_guild = None
    
    def post_setup(self) -> None:

        self.fyic_guild = self.bot.get_guild(self.FYIC_GUILD_ID)
        
        if self.fyic_guild is None:

            logging.error(f"Could not load {self}! The Guild was not found!")
    

    async def cog_check(self, ctx: commands.Context):
        
        if self.fyic_guild is None:

            return False
        
        if ctx.guild and ctx.guild.id != self.FYIC_GUILD_ID:

            return False
        
        return True


    @commands.dm_only()
    @commands.command( name='login', description="Login to the event")
    async def login_(self, ctx: commands.Context, username: str, password: str): 
        
        if not ctx.author or ctx.author.bot:

            return 
        
        if not username or not password:

            return await ctx.send("Username or Password must not be empty!")
        
        guild_member = self.fyic_guild.get_member(ctx.author.id)

        if not guild_member:
            
            return await ctx.send(f"You must be part of the {self.fyic_guild.name} server to use this command.")
        
        
        logging.info(f"User {guild_member} is logging in with user {username}")
        
        session = await ezcampus_api.User.instance().login(username, password) 
        session.access_token = "" # we don't need this
        
        if session is None:
            
            return await ctx.send("Could not login! There was an error.")

        try:
            
            role = self.fyic_guild.get_role(self.VERIFIED_ROLE_ID)
            
            if not role:

                return await ctx.send("Could not give you the verified role. The role does not exist! Please let the commity team know!")

            await guild_member.add_roles(role, reason="The user verified with EZCampus", atomic=True)

            await ctx.send(f"You have been verified as {session.username}!")

        except discord.Forbidden:

            return await ctx.send("I don't have permission to give you role. Please let the commity team know!")

        except Exception as e:

            logging.error(e, stack_info=True)
            logging.error(f"Could not give {guild_member} a role!")
            
            return await ctx.send("Could not give you the verified role. Something has gone wrong!")
        
        try:

            await guild_member.edit(nick=session.username)

        except discord.Forbidden:

            return await ctx.send("I don't have permission to change your nickname. Please let the commity team know!")

        except Exception as e:

            logging.error(e, stack_info=True)
            logging.error(f"Could not change {guild_member} nickname!")
            
            return await ctx.send("Could not change your nickname. Something has gone wrong!")

