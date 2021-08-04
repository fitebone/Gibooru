import os
import sys
dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
path = os.path.join(root, 'src')
sys.path.insert(0, path)
from gibooru import Gelbooru
import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    # Get random post
    async def test_get_random_post(self):
        g = Gelbooru()
        r1 = await g.get_random_post()
        id1 = r1.json()[0]['id']
        r2 = await g.get_random_post()
        id2 = r2.json()[0]['id']
        await g.client.aclose()
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        self.assertNotEqual(id1, id2)

    async def test_search_posts(self):
        pass

if __name__ == '__main__':
    unittest.main()