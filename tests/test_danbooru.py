import os
import sys
dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
path = os.path.join(root, 'src')
sys.path.insert(0, path)
from gibooru import Danbooru
import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    # Get random post: /posts/random
    async def test_get_post_random(self):
        d = Danbooru()
        x = await d.get_post()
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)
    
    # Get specific post: /posts/{id}
    async def test_get_post_id(self):
        d = Danbooru()
        x = await d.get_post(4677555)
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
        print(d.page_urls)
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)

    # Get tags with query
    async def test_search_tags_query(self):
        d = Danbooru()
        x = await d.search_tags(page=2, name='*car*', order='count', category=1)
        print(d.page_urls)
        await d.client.aclose()
        self.assertEqual(x.status_code, 200)
    
if __name__ == '__main__':
    unittest.main()