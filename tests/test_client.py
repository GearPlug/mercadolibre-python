import ast
import os
from unittest import TestCase
from mercadolibre.client import Client
from urllib.parse import urlparse, parse_qs


class MercadoLibreTestCases(TestCase):
    def setUp(self):
        self.client_id = os.environ.get('client_id')
        self.client_secret = os.environ.get('client_secret')
        self.site = os.environ.get('site')
        self.client = Client(self.client_id, self.client_secret, self.site)
        self.redirect_url = os.environ.get('redirect_url')
        self.token = os.environ.get('token')
        self.client.set_token(ast.literal_eval(self.token))

    def test_authorization_url(self):
        url = self.client.authorization_url(self.redirect_url)
        self.assertIsInstance(url, str)
        o = urlparse(url)
        query = parse_qs(o.query)
        self.assertIn('client_id', query)
        self.assertEqual(query['client_id'][0], self.client_id)
        self.assertIn('redirect_uri', query)
        self.assertEqual(query['redirect_uri'][0], self.redirect_url)

    def test_me(self):
        response = self.client.me()
        self.assertEqual(response['id'], self.client.user_id)

    def test_get_user(self):
        response = self.client.get_user(self.client.user_id)
        self.assertEqual(response['id'], self.client.user_id)

    def test_get_user_address(self):
        response = self.client.get_user_address(self.client.user_id)
        self.assertIsInstance(response, list)

    def test_application(self):
        response = self.client.get_application(self.client_id)
        self.assertEqual(response['id'], int(self.client_id))
        response2 = self.client.get_project(response['project_id'])
        self.assertEqual(response2['id'], response['project_id'])

    def test_get_sites(self):
        response = self.client.get_sites()
        self.assertIsInstance(response, list)

    def test_get_categories(self):
        response = self.client.get_categories(self.site)
        self.assertIsInstance(response, list)

    def test_get_countries(self):
        response = self.client.get_countries()
        self.assertIsInstance(response, list)

    def test_get_currencies(self):
        response = self.client.get_currencies()
        self.assertIsInstance(response, list)
