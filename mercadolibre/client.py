import requests
import time
from mercadolibre import exceptions
from mercadolibre.decorators import valid_token
from urllib.parse import urlencode


class Client(object):
    BASE_URL = 'https://api.mercadolibre.com'

    auth_urls = {
        'MLA': "https://auth.mercadolibre.com.ar",  # Argentina
        'MLB': "https://auth.mercadolivre.com.br",  # Brasil
        'MCO': "https://auth.mercadolibre.com.co",  # Colombia
        'MCR': "https://auth.mercadolibre.com.cr",  # Costa Rica
        'MEC': "https://auth.mercadolibre.com.ec",  # Ecuador
        'MLC': "https://auth.mercadolibre.cl",  # Chile
        'MLM': "https://auth.mercadolibre.com.mx",  # Mexico
        'MLU': "https://auth.mercadolibre.com.uy",  # Uruguay
        'MLV': "https://auth.mercadolibre.com.ve",  # Venezuela
        'MPA': "https://auth.mercadolibre.com.pa",  # Panama
        'MPE': "https://auth.mercadolibre.com.pe",  # Peru
        'MPT': "https://auth.mercadolibre.com.pt",  # Prtugal
        'MRD': "https://auth.mercadolibre.com.do"  # Dominicana
    }

    def __init__(self, client_id, client_secret, site='MCO'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.expires_in = None
        self.expires_at = None
        try:
            self.auth_url = self.auth_urls[site]
        except KeyError as e:
            raise exceptions.InvalidSite()

    def get_authorization_url(self, redirect_uri):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri
        }
        url = self.auth_url + '/authorization?' + urlencode(params)
        return url

    def exchange_code(self, redirect_uri, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        return self._token(self._post('/oauth/token', params=params))

    def refresh_token(self):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }
        return self._token(self._post('/oauth/token', params=params))

    def set_token(self, token):
        if isinstance(token, dict):
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            self.user_id = token['user_id']
            self.expires_in = token['expires_in']
            if 'expires_at' in token:
                self.expires_at = token['expires_at']
        else:
            self.access_token = token

    @property
    def is_valid_token(self):
        if self.expires_at:
            return self.expires_at > time.time()
        else:
            return None

    def _token(self, response):
        if 'expires_in' in response:
            expires_in = response['expires_in']
            expires_at = time.time() + int(expires_in)
            response['expires_at'] = expires_at
            self.expires_at = expires_at
        return response

    def _get(self, endpoint, params=None):
        return self._request('GET', endpoint, params)

    def _post(self, endpoint, params=None, data=None):
        return self._request('POST', endpoint, params, data)

    def _put(self, endpoint, params=None, data=None):
        return self._request('PUT', endpoint, params, data)

    @valid_token
    def _request(self, method, endpoint, params=None, data=None):
        if params:
            params['access_token'] = self.access_token
        else:
            params = {'access_token': self.access_token}
        response = requests.request(method, self.BASE_URL + endpoint, params=params, data=data)
        return self._parse(response)

    def _parse(self, response):
        print(response.json())
        print(response.status_code)
        return response

    def me(self):
        """Returns account information about the authenticated user.

        Returns:

        """
        return self._parse(self._get('/users/me'))

    def get_user(self, customer_id):
        """User account information.

        Args:
            customer_id:

        Returns:

        """
        return self._parse(self._get('/users/{}'.format(customer_id)))

    def update_user(self):
        raise NotImplementedError

    def get_user_address(self, customer_id):
        """Returns addresses registered by the user.

        Args:
            customer_id:

        Returns:

        """
        return self._parse(self._get('/users/{}/addresses'.format(customer_id)))

    def get_user_accepted_payment_methods(self, customer_id):
        """Returns payment methods accepted by a seller to collect its operations.

        Args:
            customer_id:

        Returns:

        """
        return self._parse(self._get('/users/{}/accepted_payment_methods'.format(customer_id)))

    def get_application(self, application_id):
        """Returns information about the application.

        Args:
            application_id:

        Returns:

        """
        return self._parse(self._get('/applications/{}'.format(application_id)))

    def get_user_brands(self, user_id):
        """This resource retrieves brands associated to an user_id. The official_store_id attribute identifies a store.

        Args:
            user_id:

        Returns:

        """
        return self._parse(self._get('/users/{}/brands'.format(user_id)))

    def get_user_classifields_promotion_packs(self, user_id):
        """Manage user promotion packs.

        Args:
            user_id:

        Returns:

        """
        return self._parse(self._get('/users/{}/classifieds_promotion_packs'.format(user_id)))

    def create_user_classifields_promotion_packs(self):
        raise NotImplementedError

    def get_project(self, project_id):
        """Manage projects.

        Returns:

        """
        return self._parse(self._get('/projects/{}'.format(project_id)))

    def create_project(self):
        raise NotImplementedError

    def update_project(self):
        raise NotImplementedError

    def delete_project(self):
        raise NotImplementedError

    def get_my_feeds(self):
        """Notifications history.

        Returns:

        """
        params = {
            'app_id': self.client_id
        }
        return self._parse(self._get('/myfeeds', params=params))

    def get_sites(self):
        """Retrieves information about the sites where MercadoLibre runs.

        Returns:

        """
        return self._parse(self._get('/sites'))

    def get_listing_types(self, site_id):
        """Returns information about listing types.

        Args:
            site_id:

        Returns:

        """
        return self._parse(self._get('/sites/{}/listing_types'.format(site_id)))

    def get_listing_exposures(self, site_id):
        """Returns different exposure levels associated with all listing types in MercadoLibre.

        Args:
            site_id:

        Returns:

        """
        return self._parse(self._get('/sites/{}/listing_exposures'.format(site_id)))

    def get_categories(self, site_id):
        """	Returns available categories in the site.

        Args:
            site_id:

        Returns:

        """
        return self._parse(self._get('/sites/{}/categories'.format(site_id)))

    def get_category(self, category_id):
        """Returns information about a category.

        Args:
            category_id:

        Returns:

        """
        return self._parse(self._get('/categories/{}'.format(category_id)))

    def get_category_attributes(self, category_id):
        """Displays attributes and rules over them in order to describe the items that are stored in each category.

        Args:
            category_id:

        Returns:

        """
        return self._parse(self._get('/categories/{}/attributes'.format(category_id)))

    def get_countries(self):
        """Returns countries information.

        Returns:

        """
        return self._parse(self._get('/countries'))

    def get_country(self, country_id):
        """Returns country information by country_id.

        Returns:

        """
        return self._parse(self._get('/countries/{}'.format(country_id)))

    def get_state(self, state_id):
        """	Returns state information.

        Args:
            state_id:

        Returns:

        """
        return self._parse(self._get('/states/{}'.format(state_id)))

    def get_city(self, city_id):
        """Returns city information.

        Args:
            city_id:

        Returns:

        """
        return self._parse(self._get('/cities/{}'.format(city_id)))

    def get_currencies(self):
        """	Returns information about all available currencies in MercadoLibre.

        Returns:

        """
        return self._parse(self._get('/currencies'))

    def get_currency(self, currency_id):
        """Returns information about available currencies in MercadoLibre by currency_id.

        Args:
            currency_id:

        Returns:

        """
        return self._parse(self._get('/currencies/{}'.format(currency_id)))

    def list_item(self, title, condition, category_id, price, currency_id, available_quantity, buying_mode,
                  listing_type_id, video_id, warranty, pictures, description=None, **kwargs):
        return self._parse(self._post('/items'))
