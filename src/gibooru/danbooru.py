from gibooru import Gibooru
from datetime import datetime, date
from typing import Optional, List, Literal, Tuple
from pydantic import BaseModel, validator, PositiveInt
from httpx import Response, URL

'''
Default is 20 results per page
Max limit is 200 for /posts.json, 1000 for everything else

Anonymous:
Search 2 tags
Browse 1000 pages in a search

Reads are not rate limited
'''

class Danbooru(Gibooru):
    '''Danbooru API client'''
    def __init__(self,
        api_key: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 20, # Danbooru default, max 200
        response_extension: Literal['.json', '.html', '.xml', '.atom'] = '.json'
        ):
        super().__init__(api_key=api_key, user_id=user_id, default_limit=limit, image_schema=DanbooruImage)
        self.api_base = 'https://danbooru.donmai.us/'
        self.ext = response_extension

    async def get_count(self, query: str, limit: Optional[int] = None) -> Tuple:
        '''
        Count the number of posts, and pages of such posts, resulting from a query
        '''
        endpoint = self.api_base + 'counts/posts.json?' + query
        response = await self.client.get(endpoint)
        post_count = response.json()['counts']['posts']
        if not limit:
            limit = self.default_limit
        page_count = post_count // limit
        return post_count, page_count

    async def get_post(self, 
        id: Optional[PositiveInt] = None, 
        md5: Optional[str] = None
        ) -> Response:
        '''
        Gets a single post from Danbooru

        If no id or md5 is given, a random post is found
        '''
        endpoint = self.api_base + 'posts'
        if id:
            endpoint += f'/{id}' + self.ext
        elif md5:
            endpoint += self.ext + f'?md5={md5}'
        else:
            endpoint += '/random' + self.ext
        self.last_search = endpoint
        return await self._get(endpoint)

    async def search_posts(self, 
        page: Optional[PositiveInt] = None, 
        limit: Optional[PositiveInt] = None,
        tags: Optional[str] = None, # order:rank for Hot posts
        **kwargs
        ) -> Response:
        '''
        Searches for Danbooru posts
        '''
        endpoint = self.api_base + 'posts' + self.ext + '?'
        if not limit:
            limit = self.limit
        data = {'page': page, 'tags': tags, 'limit': limit}
        params = {}
        params = self._authenticate(params)
        if kwargs:
            data = {**data, **kwargs}
        for k, v in data.items():
            if v:
                params[k] = v
        response = await self._get(endpoint, params=params)
        self._store_search_data(str(response.url), endpoint, params, page)
        return response

    async def search_tags(self,
        page: Optional[PositiveInt] = None,
        limit: Optional[PositiveInt] = None,
        name: Optional[str] = None,
        order: Optional[Literal['date', 'count', 'name']] = None,
        hide_empty: Optional[bool] = None,
        category: Optional[Literal[0,1,3,4,5]] = None,
        has_artist: Optional[bool] = None,
        has_wiki_page: Optional[bool] = None,
        **kwargs
        ) -> Response:
        '''
        Searches for Danbooru tags
        '''
        endpoint = self.api_base + 'tags' + self.ext + '?'
        if not limit:
            limit = self.limit
        data = {
            'commit': 'Search', 
            'page': page, 
            'limit': limit,
            'search[name_or_alias_matches]': name,
            'search[order]': order, 
            'search[hide_empty]': hide_empty, 
            'search[category]': category,
            'search[has_artist]': has_artist,
            'search[has_wiki_page]': has_wiki_page,
            }
        params = {}
        params = self._authenticate(params)
        if kwargs:
            data = {**data, **kwargs}
        for k, v in data.items():
            if v:
                params[k] = v
        response = await self._get(endpoint, params=params)
        self._store_search_data(str(response.url), endpoint, params, page)
        return response

    async def search_artists(self,
        page: Optional[PositiveInt] = None,
        limit: Optional[PositiveInt] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
        order: Optional[Literal['name', 'updated_at', 'post_count']] = None,
        has_tag: Optional[bool] = None,
        is_banned: Optional[bool] = None,
        is_deleted: Optional[bool] = None,
        **kwargs
        ) -> Response:
        '''
        Searches for Danbooru artists 
        '''
        endpoint = self.api_base + 'artists' + self.ext + '?'
        if not limit:
            limit = self.limit
        data = {
            'commit': 'Search', 
            'page': page, 
            'limit': limit,
            'search[any_name_matches]': name,
            'search[url_matches]': url, 
            'search[order]': order, 
            'search[has_tag]': has_tag,
            'search[is_banned]': is_banned,
            'search[is_deleted]': is_deleted,
            }
        params = {}
        params = self._authenticate(params)
        if kwargs:
            data = {**data, **kwargs}
        for k, v in data.items():
            if v:
                params[k] = v
        response = await self._get(endpoint, params=params)
        self.last_search = str(response.url)
        return response

    async def explore_post(self, 
        page: Optional[PositiveInt] = None,
        limit: Optional[PositiveInt] = None, # Only applies to popular
        date: Optional[date] = None,
        option: Literal['popular', 'curated', 'viewed'] = 'popular',
        scale: Optional[Literal['day', 'week', 'year']] = None,
        **kwargs
        ) -> Response:
        '''
        Explore Danbooru's most popular, curated, or viewed posts for a certain day, week, or month
        '''
        endpoint = self.api_base + 'explore/posts/' + option + self.ext + '?'
        if not limit:
            limit = self.limit
        data = {'page': page, 'date': date, 'limit': limit}
        params = {}
        params = self._authenticate(params)
        if kwargs:
            data = {**data, **kwargs}
        for k, v in data.items():
            if v:
                params[k] = v
        response = await self._get(endpoint, params=params)
        if option == 'popular' or option == 'curated': # Viewed doesnt have pages
            self.page_urls = self._update_urls(endpoint, params, page)
        self.last_search = str(response.url)
        return response
    
    async def explore_tag(self,
        date: Optional[date] = None,
        option: Literal['searches', 'missed_searches'] = 'searches',
        ) -> Response:
        '''
        Explore Danbooru's most popular tag searches by day, or most missed tag searches in the last week
        '''
        endpoint = self.api_base + 'explore/posts/' + option + self.ext + '?'
        params = {}
        if date:
            params['date'] = date
        response = await self._get(endpoint, params=params)
        self.last_search = str(response.url)
        return response

    @staticmethod
    def handle_response_code(self, code: int):
        reply, message = ()
        if code == 200:
            reply, message = ('OK', 'Request was successful')
        elif code == 204:
            reply, message = ('No Content', 'Request was successful')
        elif code == 400:
            reply, message = ('Bad Request', 'The given parameters could not be parsed')
        elif code == 401:
            reply, message = ('Unauthorized', 'Authentication failed')
        elif code == 404:
            reply, message = ('Not found', 'Not found')
        elif code == 410:
            reply, message = ('Gone', 'Pagination limit')
        elif code == 420:
            reply, message = ('Invalid Record', 'Record could not be saved')
        elif code == 422:
            reply, message = ('Locked', 'The resource is locked and cannot be modified')
        elif code == 423:
            reply, message = ('Already Exists', 'Resource already exists')
        elif code == 424:
            reply, message = ('Invalid Parameters', 'The given parameters were invalid')
        elif code == 429:
            reply, message = ('User Throttled', 'User is throttled, try again later')
        elif code == 500:
            reply, message = ('Internal Server Error', 'A database timeout, or some unknown error occurred on the server')
        elif code == 502:
            reply, message = ('Bad Gateway', 'Server cannot currently handle the request, try again later (heavy load)')
        elif code == 503:
            reply, message = ('Service Unavailable', 'Server cannot currently handle the request, try again later (downbooru)')
        else:
            reply, message = ('Unknown', 'Something went wrong')
        return reply, message

# Needed?
class DanbooruImage(BaseModel):
    id: int = 0
    created_at: datetime
    uploader_id: int
    score: int
    source: str
    md5: Optional[str]
    last_comment_bumped_at: Optional[datetime]
    rating: str
    image_width: int
    image_height: int
    tag_string: str
    is_note_locked: bool
    fav_count: int
    file_ext: Optional[str]
    last_noted_at: Optional[datetime]
    is_rating_locked: bool
    parent_id: Optional[int]
    has_children: bool
    approver_id: Optional[int]
    tag_count_general: int
    tag_count_artist: int
    tag_count_character: int
    tag_count_copyright: int
    file_size: int
    is_status_locked: bool
    pool_string: str
    up_score: int
    down_score: int
    is_pending: bool
    is_flagged: bool
    is_deleted: bool
    tag_count: int
    updated_at: datetime
    is_banned: bool
    pixiv_id: Optional[int]
    last_commented_at: Optional[datetime]
    has_active_children: bool
    bit_flags: int
    tag_count_meta: int
    has_large: Optional[bool]
    has_visible_children: bool
    tag_string_general: str
    tag_string_character: str
    tag_string_copyright: str
    tag_string_artist: str
    tag_string_meta: str
    file_url: Optional[str]
    large_file_url: Optional[str]
    preview_file_url: Optional[str]

    def __str__(self):
        return self.file_url

    def __repr__(self) -> int:
        return self.id
    
    @validator(
        'tag_string_general',
        'tag_string_character',
        'tag_string_copyright',
        'tag_string_artist',
        'tag_string_meta',
    )
    def check_tags(cls, v) -> List[str]:
        return v.split(' ')

    @property
    def thumbnail(self) -> str:
        return self.preview_file_url
