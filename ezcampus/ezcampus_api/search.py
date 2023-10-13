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
import aiohttp

from dataclasses import dataclass

@dataclass
class ExtraData:
    building: str
    building_description: str

@dataclass
class CourseData:
    course_data_id: int
    course_id: int
    course_code: str
    course_crn: str
    course_desc: str
    class_type: str
    instructors: list[ExtraData | dict ]
    extra: list
    ranking: int
    course_title: str




class Search():
    """
    Provides access to the EZCampus search api
    """

    EZCAMPUS_SEARCH_API_BASE = "https://search.ezcampus.org/searchIndex/"
    POST_SEARCH = f"{EZCAMPUS_SEARCH_API_BASE}search"
    
    SEARCH_METHOD_FUZZY = True
    SEARCH_METHOD_NATIVE = False
    
    __INSTANCE = None
    
    def __init__(self, httpClient: aiohttp.ClientSession) -> None:
        self.session = httpClient

    @staticmethod
    def instance(client: aiohttp.ClientSession=None):
        
        if not Search.__INSTANCE:
            Search.__INSTANCE = Search(client)
            
        return Search.__INSTANCE
        

    async def search(self, 
                     search_term: str, 
                     term_id:int, 
                     search_method: bool=SEARCH_METHOD_NATIVE, 
                     page: int=1, results_per_page: int=10) -> list[CourseData]:
        
        payload = {
            "search_term" : search_term,
            "page" : page,
            "results_per_page" : results_per_page,
            "term_id": term_id,
            "search_method": search_method
        }
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        async with self.session.post(self.POST_SEARCH, json=payload, headers=headers) as response:
            
            if response.status == 200:
                
                return [CourseData(**course) for course in await response.json()]
            
            logging.warning(f"Got reponse {response.status} when fetching search results")
            logging.warning(f"Got reponse {await response.text()} when fetching search results")
            
