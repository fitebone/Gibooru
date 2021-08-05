import os
import sys
dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
path = os.path.join(root, 'src')
sys.path.insert(0, path)
from gibooru import Danbooru, DanbooruImage, Gelbooru, GelbooruImage
import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    # Get DanbooruImage(s) from pages Danbooru
    async def test_danbooru_pages(self):
        d = Danbooru()
        d.num_page_urls = 20
        await d.search_posts()
        posts = await d.get_posts_from_pages()
        await d._close()
        self.assertLessEqual(len(posts), d.num_page_urls*d.limit)

    # Get DanbooruImage(s) from pages Danbooru with limit
    async def test_danbooru_pages_limit(self):
        d = Danbooru()
        d.num_page_urls = 20
        limit = 35
        await d.search_posts(limit=limit)
        posts = await d.get_posts_from_pages()
        await d._close()
        self.assertLessEqual(len(posts), d.num_page_urls*limit)

    # Get GelbooruImage(s) from pages Gelbooru
    async def test_gelbooru_pages(self):
        g = Gelbooru()
        g.num_page_urls = 20
        await g.search_posts()
        posts = await g.get_posts_from_pages()
        await g._close()
        self.assertLessEqual(len(posts), g.num_page_urls*g.limit)
    
    # Get GelbooruImage(s) from pages Gelbooru with limit
    async def test_gelbooru_pages_limit(self):
        g = Gelbooru()
        g.num_page_urls = 20
        limit = 35
        await g.search_posts(limit=limit)
        posts = await g.get_posts_from_pages()
        await g._close()
        self.assertLessEqual(len(posts), g.num_page_urls*limit)

if __name__ == '__main__':
    unittest.main()