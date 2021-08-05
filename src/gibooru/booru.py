import gibooru
import httpx
from typing import List, Optional, NoReturn
from abc import ABC
from pydantic import BaseModel
import re

class Gibooru(ABC):
    '''
    Base class to access Booru APIs

    Gibs you access to the Boorus' data
    '''
    def __init__(self, 
        api_key: Optional[str] = None, 
        user_id: Optional[str] = None, 
        default_limit: int = 100,
        image_schema: BaseModel = None
        ) -> NoReturn:
        self._api_key = api_key
        self._user_id = user_id
        self._image_schema = image_schema
        self._last_query = ''
        self._default_limit = default_limit # Number of items per page of data
        self._page_urls = [] # List of urls for pages of 'limit' amount of content from the booru
        self._num_page_urls = 100 # Alotted size of the list '_page_urls'
        self.client = httpx.AsyncClient()
    
    def _authenticate(self, params: dict) -> dict:
        '''
        Adds _api_key and _user_id to request query parameter dict
        '''
        _dict = params
        if self._api_key:
            _dict = {**_dict, **{'api_key': self._api_key, 'login': self._user_id}}
        return _dict
    
    async def _close(self):
        await self.client.aclose()

    async def _get(self, endpoint: str, params: Optional[dict] = None) -> httpx.Response:
        return await self.client.get(endpoint, params=params)

    def _update_urls(self, endpoint: str, query: str, base_page: int) -> List[str]:
        posts = []
        if not base_page:
            base_page = 1
        if isinstance(self, gibooru.Danbooru):
            posts = list(endpoint + re.sub('page=\d*&', f'page={page}&', query) for page in range(base_page, base_page + self.num_page_urls))
        elif isinstance(self, gibooru.Gelbooru):
            posts = list(endpoint + re.sub('pid=\d*&', f'pid={page}&', query) for page in range(base_page, base_page + self.num_page_urls))
        return posts

    async def get_posts_from_pages(self, limit: Optional[int] = None) -> List:
        posts = []
        if not limit:
            limit = self._default_limit
        for page in self._page_urls:
            response = await self._get(page)
            json = response.json()
            for i in range(limit):
                if 0 <= i < len(json):
                    posts.append(self._image_schema(**json[i]))
        return posts

    @staticmethod
    def response_to_json(self, response: httpx.Response) -> List[Optional[dict]]:
        '''
        Converts a response with json content into a pythonic json object
        '''
        return response.json()
    
    @property
    def last_query(self):
        return self._last_query
    
    @last_query.setter
    def last_query(self, query: str):
        self._last_query = query
    
    @property
    def limit(self):
        return self._default_limit
    
    @limit.setter
    def limit(self, limit: int):
        self._default_limit = limit

    @property
    def page_urls(self):
        return self._page_urls
    
    @page_urls.setter
    def page_urls(self, url_list: List[str]):
        self._page_urls = url_list

    @property
    def num_page_urls(self):
        return self._num_page_urls
    
    @num_page_urls.setter
    def num_page_urls(self, num_page_urls: int):
        self._num_page_urls = num_page_urls