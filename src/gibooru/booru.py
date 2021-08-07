import gibooru
import httpx
from typing import List, Optional, NoReturn, Tuple
from abc import ABC
from pydantic import BaseModel
import base64

# Should probably implement ABC somehow
class Gibooru(ABC):
    '''
    Base class to access Booru APIs

    Gibs you access to the Boorus' data
    '''
    def __init__(self, 
        api_key: Optional[str] = None, 
        user_id: Optional[str] = None, 
        default_limit: int = 100,
        image_schema: BaseModel = None,
        sync: bool = False) -> NoReturn:
        self._api_key = api_key
        self._user_id = user_id
        self._image_schema = image_schema
        self._last_search = ''
        self._last_params = {}
        self._default_limit = default_limit # Number of items per page of data
        self._page_urls = [] # List of urls for pages of 'limit' amount of content from the booru
        self._num_page_urls = 100 # Alotted size of the list '_page_urls'
        self.client = httpx.AsyncClient(http2=True)
    
    def _authenticate(self, params: dict) -> dict:
        '''
        Adds _api_key and _user_id to request query parameter dict
        '''
        _dict = params
        if self._api_key:
            _dict = {**_dict, **{'api_key': self._api_key, 'login': self._user_id}}
        return _dict
    
    async def _close(self):
        '''
        Close the httpx client
        '''
        await self.client.aclose()

    async def _get(self, endpoint: str, params: Optional[dict] = None) -> httpx.Response:
        '''
        Httpx client get using a url (endpoint) and parameters
        '''
        return await self.client.get(endpoint, params=params)

    def _update_urls(self, endpoint: str, params: str, base_page: int) -> List[str]:
        '''
        Returns a list of page urls using the specified endpoint and params

        Pages range from base_page to (base_page + num_page_urls)
        '''
        posts = []
        if not base_page:
            base_page = 1
        query_string = ''
        
        if isinstance(self, gibooru.Danbooru):
            for k, v in params.items():
                if k != 'page':
                    query_string += f'{k}={v}&'
            posts = list(endpoint + query_string + f'page={page}' for page in range(base_page, base_page + self.num_page_urls))
        elif isinstance(self, gibooru.Gelbooru):
            for k, v in params.items():
                if k != 'pid':
                    query_string += f'{k}={v}&'
            posts = list(endpoint + query_string + f'pid={page}' for page in range(base_page, base_page + self.num_page_urls))
        return posts

    def _store_search_data(self, search: str, endpoint: str, params: dict, page: int):
        '''
        Updates Gibooru variables based on last query

        Used only after queries that result in pages of data
        '''
        self.page_urls = self._update_urls(endpoint, params, page)
        self.last_search = search
        self.last_params = params

    async def pages_to_json(self) -> List[Optional[dict]]:
        '''
        Gets a list of json representations of the pages from the last query
        '''
        jsons = []
        for page in self._page_urls:
            response = await self._get(page)
            json = self.response_to_json(response)
            jsons.append(json)
        return jsons

    async def pages_to_posts(self) -> List[Optional[dict]]:
        '''
        Gets a list of <Booru>Image(s) representations of the posts from the last query
        '''
        posts = []
        for page in self._page_urls:
            response = await self._get(page)
            page_posts = self.response_to_posts(response)
            for i in range(len(page_posts)):
                posts.append(page_posts[i])
        return posts

    async def pages_to_images(self, thumbnail: bool = False) -> List[Tuple[bytes, str]]:
        '''
        Gets a list of byte data representations of the posts from the last query

        Time to complete depends on 'num_page_urls' and 'limit' which are configurable
        '''
        posts = await self.pages_to_posts()
        image_data = []
        for post in posts:
            r = None
            if thumbnail:
                r = await self._get(post.thumbnail)
            else:
                r = await self._get(post.file_url)
            data = base64.b64decode(r.content)
            ext = post.file_url.split('.')[-1]
            image_data.append((data, ext))
        return image_data

    # Could be static I guess
    def response_to_json(self, response: httpx.Response) -> Tuple[List[Optional[dict]], bool]:
        '''
        Converts a response with json content into a pythonic json object
        '''
        json = []
        valid = True
        try:
            json = response.json()
        except Exception:
            print('Not a valid JSON response')
            valid = False
        return json, valid
    
    def response_to_posts(self, response: httpx.Response) -> List[Optional[dict]]:
        '''
        Converts a response with json content into a list of Booru post representations

        Each <Booru>Image class is unique to their unique API responses
        '''
        json, valid = self.response_to_json(response)
        posts = []
        if valid:
            for i in range(len(json)):
                posts.append(self._image_schema(**json[i]))
        return posts

    async def response_to_images(self, response: httpx.Response, thumbnail: bool = False) -> List[bytes]:
        '''
        Converts a response with json content into list of image byte data
        '''
        posts = self.response_to_posts(response)
        image_data = []
        if len(posts) > 0:
            for post in posts:
                r = None
                if thumbnail:
                    r = await self._get(post.thumbnail)
                else:
                    r = await self._get(post.file_url)
                data = base64.b64decode(r.content)
                ext = post.file_url.split('.')[-1]
                image_data.append((data, ext))
        return image_data

    @property
    def last_search(self):
        return self._last_search
    
    @last_search.setter
    def last_search(self, search: str):
        self._last_search = search
    
    @property
    def last_params(self):
        return self._last_params
    
    @last_params.setter
    def last_params(self, params: dict):
        self._last_params = params
    
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