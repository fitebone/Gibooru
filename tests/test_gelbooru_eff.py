import os
import sys
dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
path = os.path.join(root, 'src')
sys.path.insert(0, path)
from gibooru import Gelbooru, GelbooruImage
import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    # Get json from Gelbooru response
    async def test_gelbooru_response_json(self):
        g = Gelbooru(limit=50)
        r = await g.search_posts()
        json, valid = g.response_to_json(r)
        await g._close()
        self.assertTrue(valid)
        self.assertGreater(len(json), 0)
    
    # Get posts from Gelbooru response
    async def test_gelbooru_response_posts(self):
        g = Gelbooru(limit=50)
        r = await g.search_posts()
        posts = g.response_to_posts(r)
        await g._close()
        self.assertLessEqual(len(posts), g.num_page_urls*g.limit)
        self.assertGreater(len(posts), 0)

    # Get images from Gelbooru response
    async def test_gelbooru_response_images(self):
        g = Gelbooru(limit=5)
        r = await g.search_posts()
        images = await g.response_to_images(r)
        await g._close()
        x = images[0]
        self.assertIsNotNone(x)
        self.assertLessEqual(len(images), g.num_page_urls*g.limit)
        self.assertGreater(len(images), 0)

    # Get json from Danbooru pages
    async def test_gelbooru_json(self):
        g = Gelbooru(limit=50)
        g.num_page_urls = 10
        await g.search_posts()
        posts = await g.pages_to_json()
        await g._close()
        self.assertLessEqual(len(posts), g.num_page_urls*g.limit)
        self.assertGreater(len(posts), 0)

    # Get posts from Gelbooru pages
    async def test_gelbooru_pages(self):
        g = Gelbooru(limit=50)
        g.num_page_urls = 10
        await g.search_posts()
        posts = await g.pages_to_posts()
        await g._close()
        self.assertLessEqual(len(posts), g.num_page_urls*g.limit)
        self.assertGreater(len(posts), 0)

    # Get images from pages Gelbooru
    async def test_gelbooru_images(self):
        g = Gelbooru(limit=5)
        g.num_page_urls = 1
        await g.search_posts()
        images = await g.pages_to_images()
        await g._close()
        x = images[0]
        self.assertIsNotNone(x)
        self.assertLessEqual(len(images), g.num_page_urls*g.limit)
        self.assertGreater(len(images), 0)

if __name__ == '__main__':
    unittest.main()