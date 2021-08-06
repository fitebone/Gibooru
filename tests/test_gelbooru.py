import os
import sys
dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
path = os.path.join(root, 'src')
sys.path.insert(0, path)
from gibooru import Gelbooru
import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    # Get random post (buggy test)
    async def test_get_random_post(self):
        g = Gelbooru()
        r1 = await g.get_random_post()
        id1 = r1.json()[0]['id']
        r2 = await g.get_random_post()
        id2 = r2.json()[0]['id']
        await g._close()
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        self.assertNotEqual(id1, id2)

    # Search post no params
    async def test_search_posts(self):
        g = Gelbooru()
        r = await g.search_posts()
        await g._close()
        self.assertEqual(len(r.json()), 100)

    # Search post with limit
    async def test_search_posts_limit(self):
        g = Gelbooru()
        r = await g.search_posts(limit=500)
        await g._close()
        self.assertEqual(len(r.json()), 500)

    # Search post with page
    async def test_search_posts_page(self):
        g = Gelbooru()
        r1 = await g.search_posts(page=1)
        r2 = await g.search_posts(page=2)
        await g._close()
        self.assertNotEqual(r1.json()[0]['id'], r2.json()[0]['id'])
    
    # Search post with id
    async def test_search_posts_id(self):
        g = Gelbooru()
        r = await g.search_posts(id=6332706)
        await g._close()
        self.assertEqual(r.json()[0]['id'], 6332706)

    # Search post with tag and page
    async def test_search_posts_tag_page(self):
        g = Gelbooru()
        tag = '*cute*'
        r1 = await g.search_posts(tags=tag)
        r2 = await g.search_posts(tags=tag, page=2)
        await g._close()
        self.assertNotEqual(r1.json()[0]['id'], r2.json()[0]['id'])
    
    # Search post with tag, page, limit
    async def test_search_posts_tag_page_limit(self):
        g = Gelbooru()
        r = await g.search_posts(tags='*an*', page=10, limit=50)
        await g._close()
        self.assertEqual(len(r.json()), 50)
    
    # Search post with all params (counter-intuitive)
    async def test_search_posts_all(self):
        g = Gelbooru()
        r = await g.search_posts(tags='*an*', page=10, limit=200, id=6332706)
        await g._close()
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json())

    #TODO Check cid functionality

    # Search tags no params
    async def test_search_tags(self):
        g = Gelbooru()
        r = await g.search_tags()
        await g._close()
        self.assertEqual(len(r.json()), 100)
    
    # Search tags with page and limit
    async def test_search_tags_page_limit(self):
        g = Gelbooru()
        r = await g.search_tags(page=50, limit=69)
        await g._close()
        self.assertEqual(len(r.json()), 69)
    
    # Search tags with name
    async def test_search_tags_name(self):
        g = Gelbooru()
        r = await g.search_tags(name='moon')
        await g._close()
        self.assertEqual(r.json()[0]['tag'], 'moon')
    
    # Search tags with name(s)
    async def test_search_tags_names(self):
        g = Gelbooru()
        r = await g.search_tags(names='moon smile')
        await g._close()
        self.assertIn(r.json()[0]['tag'], ['smile', 'moon'])
        self.assertEqual(len(r.json()), 2)

    # Search tags with name pattern
    async def test_search_tags_name_pattern(self):
        g = Gelbooru()
        r = await g.search_tags(name_pattern='%as%')
        await g._close()
        self.assertEqual(len(r.json()), 100)

    # Search tags with order and orderby
    async def test_search_tags_name_pattern(self):
        g = Gelbooru()
        r1 = await g.search_tags(names='smile moon heart', order='asc', orderby='count')
        r2 = await g.search_tags(names='moon heart smile', order='desc', orderby='count')
        await g._close()
        self.assertEqual(r1.json()[0]['id'], r2.json()[-1]['id'])

    # Search tags after id
    async def test_search_tags_after_id(self):
        g = Gelbooru()
        r = await g.search_tags(after_id='499')
        await g._close()
        self.assertEqual(len(r.json()), 100)

    # Search tags with id
    async def test_search_tags_id(self):
        g = Gelbooru()
        r = await g.search_tags(id='3717')
        await g._close()
        self.assertEqual(r.json()[0]['tag'], 'reiko_kato')

    # Search comment API broken
    '''
    async def test_get_comment(self):
        g = Gelbooru()
        r = await g.search_tags(id=6969)
        await g._close()
        self.assertEqual(len(r.json()), 100)
    '''
    
if __name__ == '__main__':
    unittest.main()