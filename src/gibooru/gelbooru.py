from gibooru import Gibooru
from httpx import Response
from typing import List, Optional, Literal, Tuple
from pydantic import PositiveInt, BaseModel, validator

'''
Max limit is 1000
'''

class Gelbooru(Gibooru):
    '''Gelbooru API client'''
    def __init__(self, 
        api_key: Optional[str] = None, 
        user_id: Optional[str] = None,
        limit: int = 100 # Gelbooru default, max 1000
        ):
        super().__init__(api_key=api_key, user_id=user_id, default_limit=limit, image_schema=GelbooruImage)
        self.api_base = 'https://gelbooru.com/index.php?'

    async def get_random_post(self) -> Response:
        '''
        Gets a random post from Gelbooru
        '''
        endpoint = self.api_base
        params = {'page': 'post', 's': 'random'}
        params = self._authenticate(params)
        r = await self._get(endpoint, params=params)
        id_ = r.url.query.decode('utf-8').split('=')[-1]
        params = {'page': 'dapi', 's': 'post', 'q': 'index', 'json': 1, 'id': id_}
        params = self._authenticate(params)
        response = await self._get(endpoint, params=params)
        self.last_search = str(response.url)
        return response

    async def search_posts(self,
        page: Optional[PositiveInt] = None,
        limit: Optional[PositiveInt] = None,
        tags: Optional[List[str]] = None,
        id: Optional[PositiveInt] = None,
        cid: Optional[PositiveInt] = None
        ) -> Response:
        '''
        Searches for Gelbooru posts
        '''
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
        response = await self._get(endpoint, params=params)
        self._store_search_data(str(response.url), endpoint, params, page)
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
        '''
        Searches for Gelbooru tags
        '''
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
        response = await self._get(endpoint, params=params)
        self._store_search_data(str(response.url), endpoint, params, page)
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

class GelbooruImage(BaseModel):
    '''
    Representation of Gelbooru images
    '''
    source: Optional[str]
    directory: str
    hash: str
    height: int
    id: int
    image: str
    change: int
    owner: str
    parent_id: Optional[str]
    rating: str
    sample: int
    preview_height: int
    preview_width: int
    sample_height: int
    sample_width: int
    score: int
    tags: str
    title: str
    width: int
    file_url: str
    created_at: str
    post_locked: int

    def __str__(self):
        return self.file_url

    def __repr__(self) -> int:
        return self.id

    @validator('tags')
    def check_tags(cls, v) -> List[str]:
        return v.split(' ')

    @property
    def thumbnail(self) -> str:
        return f'https://img3.gelbooru.com/thumbnails/{self.directory}/thumbnail_{self.hash}.jpg'
