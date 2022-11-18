from handler.handler import handle_optimize_request
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import post, Application

class MyAppTestCase(AioHTTPTestCase):
    """Integration test for the HTTP handler."""

    async def get_application(self):
        app = Application()
        app.add_routes([post('/spaceship/optimize', handle_optimize_request)])
        return app

    async def test_optimize(self):
        data = '[{"name": "Contract1", "start": 0, "duration": 5, "price": 10},{"name": "Contract2", "start": 3, "duration": 7, "price": 14},{"name": "Contract3", "start": 5, "duration": 9, "price": 8},{"name": "Contract4", "start": 5, "duration": 9, "price": 7}]'
        async with self.client.post('/spaceship/optimize', data = data) as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertEqual(text, '{"income": 18, "path": ["Contract1", "Contract3"]}')
