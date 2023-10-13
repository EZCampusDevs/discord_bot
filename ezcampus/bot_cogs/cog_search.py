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

class SearchCog(BaseCog):
    
    """
    
    A cog to provide commands for searching courses using the EZCampus API
    
    """
    
    def setup(self) -> None:

        pass


    @commands.hybrid_command(
            name='search', 
            description="Search for courses with EZCampus")
    async def search_(self, ctx: commands.Context, search_term: str, term_id: int): 
        
        response  = await ezcampus_api.Search.instance().search(search_term=search_term, term_id=term_id) 
        
        if not response:

            return await ctx.send("Could not fetch any data!")
                

        embed = discord.Embed(color = self.bot.EMBED_STANDARD_COLOR)

        grouped = {}
        for course in response:
            
            if course.course_code not in grouped:

                grouped[course.course_code] = []
                
            grouped[course.course_code].append(course)
            

        for (course_code, courses) in grouped.items():
            
            if not courses:

                continue
            
            title = f"{courses[0].course_title} {course_code}"
            
            desc = "\n".join(f"{course.course_crn} {course.class_type}" for course in courses)

            embed.add_field(
                name=title, 
                value=desc)

        await ctx.send(embed=embed)




        




