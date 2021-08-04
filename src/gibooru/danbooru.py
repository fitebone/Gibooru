from datetime import datetime, date
from gibooru import Gibooru
from typing import Optional, List, Literal
from pydantic import BaseModel, HttpUrl, validator, PositiveInt
from httpx import Response, URL
import re

'''
https://danbooru.donmai.us/wiki_pages/help%3Ausers
Anonymous:
Search 2 tags
Browse 1000 pages in a search

Member:
Favorite 10k posts
3 Favorite groups

Gold:
Search 6 tags
Browse 2000 pages in a search
View censored tags (loli, shota, etc)
Favorite 20k posts
5 Favorite groups

Plat:
Search 12 tags
Browse 5000 pages in a search
Favorite unlimited posts
10 Favorite groups

Builder:
Search unlimited tags
Unlimited Favorite groups

Maximum limit of results to return per page:
200 for /posts.json, 1000 for everything else

Common Parameters:
page
limit
search[id]
search[created_at]
search[updated_at]
search[order]?

Numeric search parameters support ranges:
100
>100
>=100
<100
<=100
100,200,300
100..200 (inclusive)

Date parameters support ranges:
2012-01-01
>2012-01-01
>=2012-01-01
<2012-01-01
<=2012-01-01
2012-01-01,2012-01-02
2012-01-01..2013-01-01 (inclusive)

Boolean parameters accept any of the following values for true or false:
True: true, t, yes, y, on, 1
False: false, f, no, n, off, 0

Most string parameters support using asterisks (*) as wildcards. 
Wildcards can be escaped with \*. 
Literal backslashes can be escaped with \\.
'''

class Danbooru(Gibooru):
    '''Danbooru API client'''
    def __init__(self):
        self.api_base = 'https://danbooru.donmai.us/'
        self.ext = '.json'
        self.page_urls = []
        self.last_query = ''
        self.limit = 200
        #self.page_urls_amount = 20 Reliant on limit and maximum pages searchable
        super().__init__()
    
    def _authenticate(self, params: dict):
        _dict = params
        if self.authentication:
            _dict = {**_dict, **self.authentication}
        return _dict
    
    async def _close(self):
        await self.client.aclose()

    async def _get_count(self, query: str) -> tuple:
        endpoint = self.api_base + 'counts/posts.json?' + query
        response = await self.client.get(endpoint)
        post_count = response.json()['counts']['posts']
        page_count = post_count // self.limit
        return post_count, page_count

    def _update_urls(self, endpoint: str, query: str, base_page: int, pages: int) -> List[str]:
        if not base_page:
            base_page = 1
        return list(endpoint + re.sub('page=\d*&', f'page={page}&', query) for page in range(base_page, base_page+pages))

    async def get_post(self, 
        id: Optional[PositiveInt] = None, 
        md5: Optional[str] = None
        ) -> Response:
        '''Searches for a single post from Danbooru
        
        Parameters
        ----------
        id: Optional[int]
            The id of the post, if not given a random post will be found
        '''

        endpoint = self.api_base + 'posts'
        if id:
            endpoint += f'/{id}' + self.ext
        elif md5:
            endpoint += self.ext + f'?md5={md5}'
        else:
            endpoint += '/random' + self.ext
        self.last_query = endpoint
        return await self.client.get(endpoint)

    async def search_posts(self, 
        page: Optional[PositiveInt] = None, 
        tags: Optional[str] = None
        ) -> Response:
        endpoint = self.api_base + 'posts' + self.ext + '?'
        data = {'page': page, 'tags': tags}
        params = {}
        params = self._authenticate(params)
        for k, v in data.items():
            if v:
                params[k] = v
        response = await self.client.get(endpoint, params=params)
        query = response.url.query.decode('utf-8')

        #self.page_urls = self._update_urls(endpoint, query, page, self.page_urls_amount)
        self.last_query = endpoint + query
        return response

    async def search_tags(self,
        page: Optional[PositiveInt] = None,
        name: Optional[str] = None,
        order: Optional[Literal['date', 'count', 'name']] = None,
        hide_empty: Optional[bool] = None,
        category: Optional[Literal[0,1,3,4,5]] = None,
        has_artist: Optional[bool] = None,
        has_wiki_page: Optional[bool] = None
        ) -> Response:
        endpoint = self.api_base + 'tags' + self.ext + '?'
        data = {
            'commit': 'Search', 
            'page': page, 
            'search[name_or_alias_matches]': name,
            'search[order]': order, 
            'search[hide_empty]': hide_empty, 
            'search[category]': category,
            'search[has_artist]': has_artist,
            'search[has_wiki_page]': has_wiki_page,
            }
        params = {}
        params = self._authenticate(params)
        for k, v in data.items():
            if v:
                params[k] = v
        response = await self.client.get(endpoint, params=params)
        query = response.url.query.decode('utf-8')
        #self.page_urls = self._update_urls(endpoint, query, page, self.page_urls_amount)
        self.last_query = endpoint + query
        return response

    async def search_artists(self,
        page: Optional[PositiveInt] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
        order: Optional[Literal['name', 'updated_at', 'post_count']] = None,
        has_tag: Optional[bool] = None,
        is_banned: Optional[bool] = None,
        is_deleted: Optional[bool] = None,
        ) -> Response:
        endpoint = self.api_base + 'artists' + self.ext + '?'
        data = {
            'commit': 'Search', 
            'page': page, 
            'search[any_name_matches]': name,
            'search[url_matches]': url, 
            'search[order]': order, 
            'search[has_tag]': has_tag,
            'search[is_banned]': is_banned,
            'search[is_deleted]': is_deleted,
            }
        params = {}
        params = self._authenticate(params)
        for k, v in data.items():
            if v:
                params[k] = v
        response = await self.client.get(endpoint, params=params)
        query = response.url.query.decode('utf-8')
        #self.page_urls = self._update_urls(endpoint, query, page, self.page_urls_amount)
        self.last_query = endpoint + query
        return response

    async def explore(self, 
        page: Optional[PositiveInt] = None,
        date: Optional[date] = None,
        option: Literal['popular', 'curated', 'viewed', 'searches', 'missed_searches'] = 'popular',
        ) -> Response:
        endpoint = self.api_base + 'explore/posts/' + option + self.ext + '?'
        data = {'page': page, 'date': date}
        params = {}
        params = self._authenticate(params)
        for k, v in data.items():
            if v:
                params[k] = v
        response = await self.client.get(endpoint, params=params)
        query = response.url.query.decode('utf-8')
        if option == 'popular' or option == 'curated':
            self.page_urls = self._update_urls(endpoint, query, page, self.page_urls_amount)
        self.last_query = endpoint + query
        return response

# Needed?
class DanbooruImage(BaseModel):
    id: int
    created_at: datetime
    uploader_id: int
    score: int
    source: HttpUrl
    md5: str
    last_comment_bumped_at: Optional[datetime]
    rating: str
    image_width: int
    image_height: int
    tag_string: str
    is_note_locked: bool
    fav_count: int
    file_ext: str
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
    has_large: bool
    has_visible_children: bool
    tag_string_general: str
    tag_string_character: str
    tag_string_copyright: str
    tag_string_artist: str
    tag_string_meta: str
    file_url: HttpUrl
    large_file_url: HttpUrl
    preview_file_url: HttpUrl

    def __str__(self):
        return self.file_url

    def __repr__(self):
        return self.id
    
    @validator(
        'tag_string_general',
        'tag_string_character',
        'tag_string_copyright',
        'tag_string_artist',
        'tag_string_meta',
    )
    def check_tags(cls, v):
        return v.split(' ')



# Utility Methods
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


danbooru_number_regex = '((<=?\d+)|(>=?\d+)|(\d+\.\.\.?\d+)|(\.\.\d+)|(\d+\.\.)|((?:\d+,?)+))+?'
# Really needed? idk
class DanbooruNumber(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=danbooru_number_regex,
            examples=['100', '100,200,300', '<100', '<=100', '>100', '>=100', '100..200', '100...200', '..100', '100..']
        )
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('String required')
        m = re.search(danbooru_number_regex, v)
        if not m:
            raise ValueError('Invalid Danbooru number format')
        # Intervals only work low to high, check?
        return cls(f'{m.group()}')
