import requests
import time
from mercadolibre import exceptions
from mercadolibre.decorators import valid_token
from urllib.parse import urlencode


class Client(object):
    BASE_URL = 'https://api.mercadolibre.com'

    auth_urls = {
        'MLA': "https://auth.mercadolibre.com.ar",  # Argentina
        'MLB': "https://auth.mercadolibre.com.br",  # Brasil
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
        self._refresh_token = None
        self.user_id = None
        self.expires_in = None
        self.expires_at = None
        try:
            self.auth_url = self.auth_urls[site]
        except KeyError as e:
            raise exceptions.InvalidSite()

    def authorization_url(self, redirect_uri):
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
            'refresh_token': self._refresh_token,
        }
        return self._token(self._post('/oauth/token', params=params))

    def set_token(self, token):
        if isinstance(token, dict):
            self.access_token = token.get('access_token', None)
            self._refresh_token = token.get('refresh_token', None)
            self.user_id = token.get('user_id', None)
            self.expires_in = token.get('expires_in', None)
            self.expires_at = token.get('expires_at', None)
        else:
            self.access_token = token

    @property
    def is_valid_token(self):
        if self.expires_at:
            return self.expires_at > time.time()
        else:
            return None

    @valid_token
    def me(self):
        """Returns account information about the authenticated user.

        Returns:
            A dict.
        """
        return self._get('/users/me')

    @valid_token
    def get_user(self, user_id):
        """User account information.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}'.format(user_id))

    def update_user(self):
        raise NotImplementedError

    @valid_token
    def get_user_address(self, user_id):
        """Returns addresses registered by the user.

        Args:
            user_id:

        Returns:
            A list.
        """
        return self._get('/users/{}/addresses'.format(user_id))

    @valid_token
    def get_user_accepted_payment_methods(self, user_id):
        """Returns payment methods accepted by a seller to collect its operations.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}/accepted_payment_methods'.format(user_id))

    @valid_token
    def get_application(self, application_id):
        """Returns information about the application.

        Args:
            application_id:

        Returns:
            A dict.
        """
        return self._get('/applications/{}'.format(application_id))

    @valid_token
    def get_user_brands(self, user_id):
        """This resource retrieves brands associated to an user_id. The official_store_id attribute identifies a store.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}/brands'.format(user_id))

    @valid_token
    def get_user_classifields_promotion_packs(self, user_id):
        """Manage user promotion packs.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}/classifieds_promotion_packs'.format(user_id))

    def create_user_classifields_promotion_packs(self):
        raise NotImplementedError

    @valid_token
    def get_project(self, project_id):
        """Manage projects.

        Returns:
            A dict.
        """
        return self._get('/projects/{}'.format(project_id))

    def create_project(self):
        raise NotImplementedError

    def update_project(self):
        raise NotImplementedError

    def delete_project(self):
        raise NotImplementedError

    @valid_token
    def get_my_feeds(self):
        """Notifications history.

        Returns:
            A dict.
        """
        params = {
            'app_id': self.client_id
        }
        return self._get('/myfeeds', params=params)

    @valid_token
    def get_sites(self):
        """Retrieves information about the sites where MercadoLibre runs.

        Returns:
            A list.
        """
        return self._get('/sites')

    @valid_token
    def get_listing_types(self, site_id):
        """Returns information about listing types.

        Args:
            site_id:

        Returns:
            A dict.
        """
        return self._get('/sites/{}/listing_types'.format(site_id))

    @valid_token
    def get_listing_exposures(self, site_id):
        """Returns different exposure levels associated with all listing types in MercadoLibre.

        Args:
            site_id:

        Returns:
            A dict.
        """
        return self._get('/sites/{}/listing_exposures'.format(site_id))

    @valid_token
    def get_categories(self, site_id):
        """	Returns available categories in the site.

        Args:
            site_id:

        Returns:
            A list.
        """
        return self._get('/sites/{}/categories'.format(site_id))

    @valid_token
    def get_category(self, category_id):
        """Returns information about a category.

        Args:
            category_id:

        Returns:
            A dict.
        """
        return self._get('/categories/{}'.format(category_id))

    @valid_token
    def get_category_attributes(self, category_id):
        """Displays attributes and rules over them in order to describe the items that are stored in each category.

        Args:
            category_id:

        Returns:
            A dict.
        """
        return self._get('/categories/{}/attributes'.format(category_id))

    @valid_token
    def get_countries(self):
        """Returns countries information.

        Returns:
            A list.
        """
        return self._get('/countries')

    @valid_token
    def get_country(self, country_id):
        """Returns country information by country_id.

        Returns:
            A dict.
        """
        return self._get('/countries/{}'.format(country_id))

    @valid_token
    def get_state(self, state_id):
        """	Returns state information.

        Args:
            state_id:

        Returns:
            A dict.
        """
        return self._get('/states/{}'.format(state_id))

    @valid_token
    def get_city(self, city_id):
        """Returns city information.

        Args:
            city_id:

        Returns:
            A dict.
        """
        return self._get('/cities/{}'.format(city_id))

    @valid_token
    def get_currencies(self):
        """	Returns information about all available currencies in MercadoLibre.

        Returns:
            A list.
        """
        return self._get('/currencies')

    @valid_token
    def get_currency(self, currency_id):
        """Returns information about available currencies in MercadoLibre by currency_id.

        Args:
            currency_id:

        Returns:
            A dict.
        """
        return self._get('/currencies/{}'.format(currency_id))

    @valid_token
    def list_item(self, title, condition, category_id, price, currency_id, available_quantity, buying_mode,
                  listing_type_id, warranty, description=None, video_id=None, pictures=None, **kwargs):
        """

        Args:
            title:
            condition:
            category_id:
            price:
            currency_id:
            available_quantity:
            buying_mode:
            listing_type_id:
            warranty:
            description:
            video_id:
            pictures:
            **kwargs:

        Returns:
            A dict.
        """
        data = {
            'title': title,
            'condition': condition,
            'category_id': category_id,
            'price': price,
            'currency_id': currency_id,
            'available_quantity': available_quantity,
            'buying_mode': buying_mode,
            'listing_type_id': listing_type_id,
            'warranty': warranty,
        }
        if description:
            data['description'] = description
        if video_id:
            data['video_id'] = video_id
        if pictures:
            if isinstance(pictures, str):
                pictures = [{'source': pictures}]
            elif isinstance(pictures, list):
                pictures = [{'source': p} for p in pictures]
            else:
                raise exceptions.InvalidPictureParameter()
            data['pictures'] = pictures
        data.update(kwargs)
        return self._post('/items', json=data)

    def _token(self, response):
        if 'expires_in' in response:
            expires_in = response['expires_in']
            expires_at = time.time() + int(expires_in)
            response['expires_at'] = expires_at
            self.expires_at = expires_at
        return response

    def _get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def _request(self, method, endpoint, params=None, **kwargs):
        _params = {'access_token': self.access_token}
        if params:
            _params.update(params)
        response = requests.request(method, self.BASE_URL + endpoint, params=_params, **kwargs)
        return self._parse(response)

    def _parse(self, response):
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        return r
