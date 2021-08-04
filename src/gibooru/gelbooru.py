from gibooru import Gibooru
from httpx import Response
from typing import List, Optional, Literal, Tuple
from pydantic import PositiveInt

'''
Max limit is 1000

&api_key=API_KEY_HERE&user_id=USER_ID_HERE

'''

class Gelbooru(Gibooru):
    '''Gelbooru API client'''
    def __init__(self, api_key: Optional[str] = None, user_id: Optional[str] = None):
        self.api_base = 'https://gelbooru.com/index.php?'
        self.last_query = ''
        self.authentication = {'api_key': api_key, 'user_id': user_id}
        self.limit = 100 # Gelbooru default
        super().__init__()

    def _authenticate(self, params: dict):
        _dict = params
        if self.authentication:
            _dict = {**_dict, **self.authentication}
        return _dict
    
    async def _close(self):
        await self.client.aclose()

    async def get_random_post(self) -> Response:
        endpoint = self.api_base
        params = {'page': 'post', 's': 'random'}
        params = self._authenticate(params)
        r = await self.client.get(endpoint, params=params)
        id_ = r.url.query.decode('utf-8').split('=')[-1]
        params = {'page': 'dapi', 's': 'post', 'q': 'index', 'json': 1, 'id': id_}
        params = self._authenticate(params)
        response = await self.client.get(endpoint, params=params)
        query = response.url.query.decode('utf-8')
        self.last_query = endpoint + query
        return response

    async def search_posts(self,
        page: Optional[PositiveInt] = None,
        limit: Optional[PositiveInt] = None,
        tags: Optional[List[str]] = None,
        id: Optional[PositiveInt] = None,
        cid: Optional[PositiveInt] = None
        ) -> Response:
        endpoint = self.api_base
        if not limit:
            limit = self.limit
        data = {
            'page': 'dapi', 
            's': 'post', 
            'q': 'index', 
            'json': 1, 
            'tags': tags, 
            'pid': page, 
            'limit': limit, 
            'cid': cid, 
            'id': id }
        params = {}
        for k, v in data.items():
            if v:
                params[k] = v
        params = self._authenticate(params)
        response = await self.client.get(endpoint, params=params)
        query = response.url.query.decode('utf-8')
        self.last_query = endpoint + query
        return response

    async def search_tags(self,
        page: Optional[PositiveInt] = None,
        limit: Optional[PositiveInt] = None,
        name: Optional[str] = None,
        names: Optional[str] = None,
        name_pattern: Optional[str] = None,
        id: Optional[PositiveInt] = None,
        after_id: Optional[PositiveInt] = None,
        order: Optional[Literal['asc', 'desc', 'ASC', 'DESC']] = None,
        orderby: Optional[Literal['date', 'count', 'name']] = None
        ) -> Response:
        endpoint = self.api_base
        if not limit:
            limit = self.limit
        data = {
            'page': 'dapi', 
            's': 'tag', 
            'q': 'index', 
            'json': 1, 
            'name': name,
            'names': names,
            'name_pattern': name_pattern,
            'pid': page, 
            'limit': limit, 
            'id': id,
            'after_id': after_id,
            'order': order,
            'orderby': orderby }
        params = {}
        for k, v in data.items():
            if v:
                params[k] = v
        params = self._authenticate(params)
        response = await self.client.get(endpoint, params=params)
        query = response.url.query.decode('utf-8')
        self.last_query = endpoint + query
        return response

    # API Not working for these?
    '''
    async def get_comment(self, id: PositiveInt):
        endpoint = self.api_base
        params = {
            'page': 'dapi',
            's': 'comment',
            'q': 'index',
            'post_id': id
        }
        params = self._authenticate(params)
        response = await self.client.get(endpoint, params=params)
        query = response.url.query.decode('utf-8')
        self.last_query = endpoint + query
        return response

    async def get_deleted_images(self, last_id: PositiveInt):
    '''