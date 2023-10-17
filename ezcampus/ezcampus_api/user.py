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
class LoginData:
    access_token: str
    token_type: str
    username: str
    

class User():
    """
    Provides access to the EZCampus user api
    """

    EZCAMPUS_USER_API_BASE = "https://api.ezcampus.org/user/"
    POST_CREATE_USER= f"{EZCAMPUS_USER_API_BASE}create"
    POST_LOGIN_USER= f"{EZCAMPUS_USER_API_BASE}login"
    
    __INSTANCE = None
    
    def __init__(self, httpClient: aiohttp.ClientSession) -> None:
        self.session = httpClient

    @staticmethod
    def instance(client: aiohttp.ClientSession=None):
        
        if not User.__INSTANCE:
            User.__INSTANCE = User(client)
            
        return User.__INSTANCE
    
    async def login(self, username: str, password: str):
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        form = aiohttp.FormData()
        form.add_field('username', username)
        form.add_field('password', password)

        async with self.session.post(self.POST_LOGIN_USER, data=form, headers=headers) as response:
            
            if response.status != 200:

                logging.info(await response.text())

                return None
            
            json = await response.json()
            
            if "detail" not in json:

                return None
            
            return LoginData(**json["detail"])
    

    async def create(self, username: str, password: str, email: str,
                     year_of_study: int, 
                     name: str = "", 
                     description: str = "",
                     school_short_name: str = "",
                     program: str = "", 
                     is_private: bool = True, 
                     is_suspended: bool = False,
                     account_status: int = 0,
                     schedule_tag: str = ""):
        
        if not name:
            name = username
        
        payload = {
          "username": username,
          "email": email,
          "password": password,
          "name": name,
          "description": description,
          "school_short_name": school_short_name,
          "program": program,
          "year_of_study": year_of_study,
          "is_private": is_private,
          "is_suspended": is_suspended,
          "account_status": account_status,
          "schedule_tag": schedule_tag,
        }

        headers = {
            'Content-Type': 'application/json',
        }
        
        async with self.session.post(self.POST_CREATE_USER, json=payload, headers=headers) as response:
            
            if response.status != 200:

                logging.info(await response.text())
            
            return response.status == 200
        


if __name__ == "__main__":

    import asyncio
    
    async def main():

        async with aiohttp.ClientSession() as session:
            
            username = "test_user_2"
            password = "password123"
            email    = "email@gmail.com"

            print(await User.instance(session).create(
                username, password, email, 3
            ))
            
            print(await User.instance().login(username, password))
    

    asyncio.run(main())


    