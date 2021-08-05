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
        r = await d.get_post()
        await d._close()
        self.assertGreater(len(r.json()), 0)
    
    # Get specific post by id
    async def test_get_post_id(self):
        d = Danbooru()
        r = await d.get_post(id=4677555)
        await d._close()
        self.assertEqual(r.json()['id'], 4677555)
    
    # Get specific post by md5
    async def test_get_post_md5(self):
        d = Danbooru()
        r = await d.get_post(md5='d1613e5f3730d85ea9ef92d813f4c431')
        await d._close()
        self.assertEqual(r.json()['md5'], 'd1613e5f3730d85ea9ef92d813f4c431')

    # Search posts no query
    async def test_search_posts(self):
        d = Danbooru()
        r = await d.search_posts()
        await d._close()
        self.assertEqual(len(r.json()), 20)
    
    # Search posts with limit
    async def test_search_posts_limit(self):
        d = Danbooru()
        r = await d.search_posts(limit=200)
        await d._close()
        self.assertEqual(len(r.json()), 200)

    # Search posts with query
    async def test_search_posts_query(self):
        d = Danbooru()
        r = await d.search_posts(page=10, tags='glasses')
        await d._close()
        self.assertEqual(len(r.json()), 20)
    
    # Search hot posts
    async def test_search_posts_hot(self):
        d = Danbooru()
        r = await d.search_posts(page=10, tags='order:rank')
        await d._close()
        self.assertEqual(len(r.json()), 20)

    # Search tags no (base) query
    async def test_search_tags(self):
        d = Danbooru()
        r = await d.search_tags()
        await d._close()
        self.assertEqual(len(r.json()), 20)

    # Search tags with limit
    async def test_search_tags_limit(self):
        d = Danbooru()
        r = await d.search_tags(limit=1000)
        await d._close()
        self.assertEqual(len(r.json()), 1000)

    # Search tags with query
    async def test_search_tags_query(self):
        d = Danbooru()
        r = await d.search_tags(page=2, name='*car*', order='count', hide_empty=True, category=0, has_artist=False, has_wiki_page=False)
        await d._close()
        self.assertEqual(len(r.json()), 20)

    # Search artists no query
    async def test_search_artists(self):
        d = Danbooru()
        x = await d.search_artists()
        await d._close()
        self.assertEqual(x.status_code, 200)
    
    # Search artists with limit
    async def test_search_artists_limit(self):
        d = Danbooru()
        r = await d.search_artists(limit=1000)
        await d._close()
        self.assertEqual(len(r.json()), 1000)

    # Search artists with query
    async def test_search_artists_query(self):
        d = Danbooru()
        r = await d.search_artists(page=2, limit=10, name='*a*', url='*k*', order='post_count', has_tag=True, is_banned=False, is_deleted=False)
        await d._close()
        self.assertEqual(len(r.json()), 10)

    # Get explore post no query
    async def test_explore_post(self):
        d = Danbooru()
        r = await d.explore_post()
        await d._close()
        self.assertEqual(len(r.json()), 20)
    
    # Get explore post with limit
    async def test_explore_post_popular(self):
        d = Danbooru()
        r = await d.explore_post(limit=1000)
        await d._close()
        self.assertEqual(len(r.json()), 1000)
    
    # Get explore post with query
    async def test_explore_post_curated(self):
        d = Danbooru()
        r = await d.explore_post(page=2, date='2021-01-05', option='curated')
        await d._close()
        self.assertEqual(len(r.json()), 20)

    # Get explore post viewed
    async def test_explore_post_viewed(self):
        d = Danbooru()
        r = await d.explore_post(option='viewed', date='2021-01-05')
        await d._close()
        self.assertEqual(len(r.json()), 100)

    # Get explore tag no query
    async def test_explore_tag_searches(self):
        d = Danbooru()
        r = await d.explore_tag()
        await d._close()
        self.assertGreaterEqual(len(r.json()), 99)

    # Get explore tag with query
    async def test_explore_tag_searches_query(self):
        d = Danbooru()
        r = await d.explore_tag(date='2021-04-07')
        await d._close()
        self.assertEqual(r.json()[0][0], 'genshin_impact')
    
    # Get explore tag no query
    async def test_explore_tag_missed_searches(self):
        d = Danbooru()
        r = await d.explore_tag(option='missed_searches')
        await d._close()
        self.assertGreaterEqual(len(r.json()), 99)

    # Get explore tag with query
    async def test_explore_tag_missed_searches_query(self):
        d = Danbooru()
        r = await d.explore_tag(option='missed_searches', date='2021-04-07')
        await d._close()
        self.assertEqual(r.json()[0][0], 'danboru')
    
if __name__ == '__main__':
    unittest.main()