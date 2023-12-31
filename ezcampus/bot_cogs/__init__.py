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


from . cog_base import BaseCog
from . cog_bot_events import BotEventCog
from . cog_test import TestCog
from . cog_basics import BasicsCog
from . cog_search import SearchCog
from . cog_fyic import FYICCog


ALL_COGS = [
    BotEventCog,
    TestCog,
    BasicsCog,
    SearchCog,
    FYICCog
]