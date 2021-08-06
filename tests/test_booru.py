import os
import sys
dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
path = os.path.join(root, 'src')
sys.path.insert(0, path)
from gibooru import Danbooru, DanbooruImage, Gelbooru, GelbooruImage
import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    # Get posts from Danbooru pages
    async def test_danbooru_pages(self):
        d = Danbooru()
        d.num_page_urls = 20
        await d.search_posts()
        posts = await d.pages_to_posts()
        await d._close()
        self.assertLessEqual(len(posts), d.num_page_urls*d.limit)
        self.assertGreater(len(posts), 0)

    # Get posts from Danbooru pages with limit
    async def test_danbooru_pages_limit(self):
        d = Danbooru()
        d.num_page_urls = 20
        limit = 35
        await d.search_posts(limit=limit)
        posts = await d.pages_to_posts()
        await d._close()
        self.assertLessEqual(len(posts), d.num_page_urls*limit)
        self.assertGreater(len(posts), 0)

    # Get images from pages Danbooru
    async def test_danbooru_images(self):
        d = Danbooru()
        d.num_page_urls = 1
        d.limit = 5
        await d.search_posts()
        images = await d.pages_to_images()
        await d._close()
        x = images[0]
        self.assertIsNotNone(x)
        self.assertLessEqual(len(images), d.num_page_urls*d.limit)
        self.assertGreater(len(images), 0)

    # Get images from pages Danbooru with limit
    async def test_danbooru_images_limit(self):
        d = Danbooru()
        d.num_page_urls = 1
        limit = 5
        await d.search_posts(limit=limit)
        images = await d.pages_to_images()
        await d._close()
        x = images[0]
        self.assertIsNotNone(x)
        self.assertLessEqual(len(images), d.num_page_urls*limit)
        self.assertGreater(len(images), 0)

    # Get posts from Gelbooru pages
    async def test_gelbooru_pages(self):
        g = Gelbooru()
        g.num_page_urls = 10
        await g.search_posts()
        posts = await g.pages_to_posts()
        await g._close()
        self.assertLessEqual(len(posts), g.num_page_urls*g.limit)
        self.assertGreater(len(posts), 0)

    # Get posts from Gelbooru pages with limit
    async def test_gelbooru_pages_limit(self):
        g = Gelbooru()
        g.num_page_urls = 10
        limit = 35
        await g.search_posts(limit=limit)
        posts = await g.pages_to_posts()
        await g._close()
        self.assertLessEqual(len(posts), g.num_page_urls*limit)
        self.assertGreater(len(posts), 0)

    # Get images from pages Gelbooru
    async def test_gelbooru_images(self):
        g = Gelbooru()
        g.num_page_urls = 1
        g.limit = 5
        await g.search_posts()
        images = await g.pages_to_images()
        await g._close()
        x = images[0]
        self.assertIsNotNone(x)
        self.assertLessEqual(len(images), g.num_page_urls*g.limit)
        self.assertGreater(len(images), 0)
    
    # Get images from pages Gelbooru with limit
    async def test_gelbooru_images_limit(self):
        g = Gelbooru()
        g.num_page_urls = 1
        limit = 5
        await g.search_posts(limit=limit)
        images = await g.pages_to_images()
        await g._close()
        x = images[0]
        self.assertIsNotNone(x)
        self.assertLessEqual(len(images), g.num_page_urls*limit)
        self.assertGreater(len(images), 0)

if __name__ == '__main__':
    unittest.main()