from datetime import datetime
from .booru import Gibooru
from typing import Optional
from pydantic import BaseModel, HttpUrl, validator
import os

class Danbooru(Gibooru):
    def __init__(self):
        self.api_base = 'https://danbooru.donmai.us'
        self.ext = '.json'
        super().__init__()
    
    async def get_post(self, id: Optional[int] = None):
        api = 'posts'
        path = ''
        if id:
            path = 'random'
        else:
            path = '{id}'
        endpoint = os.path.join(self.api_base, api, path) + self.ext
        return await self.client.build_request('GET', endpoint)

    async def get_posts(self, query: Optional[str] = None):
        api = 'posts' + self.ext
        if query:
            api += '?tags={query}'
        path = os.path.join(self.api_base, api)
        return await self.client.build_request('GET', path)

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
