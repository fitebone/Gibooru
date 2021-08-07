import os
import sys
dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
path = os.path.join(root, 'src')
sys.path.insert(0, path)
from gibooru import Danbooru, DanbooruImage
import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    # Get json from Danbooru response
    async def test_danbooru_response_json(self):
        d = Danbooru(limit=50)
        r = await d.search_posts()
        json, valid = d.response_to_json(r)
        await d._close()
        self.assertTrue(valid)
        self.assertGreater(len(json), 0)

    # Get posts from Gelbooru response
    async def test_danbooru_response_posts(self):
        d = Danbooru(limit=50)
        r = await d.search_posts()
        posts = d.response_to_posts(r)
        await d._close()
        self.assertLessEqual(len(posts), d.num_page_urls*d.limit)
        self.assertGreater(len(posts), 0)

    # Get images from Gelbooru response
    async def test_danbooru_response_images(self):
        d = Danbooru(limit=5)
        r = await d.search_posts()
        images = await d.response_to_images(r)
        await d._close()
        x = images[0]
        self.assertIsNotNone(x)
        self.assertLessEqual(len(images), d.num_page_urls*d.limit)
        self.assertGreater(len(images), 0)

    # Get json from Danbooru pages
    async def test_danbooru_json(self):
        d = Danbooru(limit=50)
        d.num_page_urls = 10
        await d.search_posts()
        posts = await d.pages_to_json()
        await d._close()
        self.assertLessEqual(len(posts), d.num_page_urls*d.limit)
        self.assertGreater(len(posts), 0)

    # Get posts from Danbooru pages
    async def test_danbooru_pages(self):
        d = Danbooru(limit=50)
        d.num_page_urls = 10
        await d.search_posts()
        posts = await d.pages_to_posts()
        await d._close()
        self.assertLessEqual(len(posts), d.num_page_urls*d.limit)
        self.assertGreater(len(posts), 0)

    # Get images from pages Danbooru
    async def test_danbooru_images(self):
        d = Danbooru(limit=5)
        d.num_page_urls = 1
        await d.search_posts()
        images = await d.pages_to_images()
        await d._close()
        x = images[0]
        self.assertIsNotNone(x)
        self.assertLessEqual(len(images), d.num_page_urls*d.limit)
        self.assertGreater(len(images), 0)

if __name__ == '__main__':
    unittest.main()