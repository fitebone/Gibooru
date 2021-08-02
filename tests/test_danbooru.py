import os
import sys
dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
path = os.path.join(root, 'src')
sys.path.insert(0, path)
from gibooru import Danbooru
import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    # Get random post
    async def test_get_post_random(self):
        d = Danbooru()
        x = await d.get_post()
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)
    
    # Get specific post by id
    async def test_get_post_id(self):
        d = Danbooru()
        x = await d.get_post(id=4677555)
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)
    
    # Get specific post by md5
    async def test_get_post_md5(self):
        d = Danbooru()
        x = await d.get_post(md5='d1613e5f3730d85ea9ef92d813f4c431')
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)

    # Get posts no query
    async def test_get_posts(self):
        d = Danbooru()
        x = await d.get_posts()
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)

    # Get posts with query
    async def test_get_posts_query(self):
        d = Danbooru()
        x = await d.get_posts(10, 'glasses')
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)

    # Get tags no (base) query
    async def test_search_tags(self):
        d = Danbooru()
        x = await d.search_tags()
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)

    # Get tags with query
    async def test_search_tags_query(self):
        d = Danbooru()
        x = await d.search_tags(page=2, name='*car*', order='count', category=1)
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)

    # Get explore no query
    async def test_explore(self):
        d = Danbooru()
        x = await d.explore()
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)
    
    # Get explore with query
    async def test_explore_query(self):
        d = Danbooru()
        x = await d.explore(page=2, date='2021-01-05', option='curated')
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)
    
if __name__ == '__main__':
    unittest.main()