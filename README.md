# mercadolibre-python

mercadolibre is an API wrapper for MercadoLibre written in python

## Installing
```
pip install mercadolibre-python
```

## Usage
```
from mercadolibre.client import Client

client = Client('CLIENT_ID, 'CLIENT_SECRET', site='MCO')
```

Get authorization url
```
url = client.authorization_url('REDIRECT_URL')
```

Exchange the code for an access token
```
token = client.exchange_code('REDIRECT_URL', 'CODE')
```

Set the token
```
client.set_token('TOKEN')
```

Refresh the token
```
new_token = client.refresh_token()
```

Get account information
```
response = client.me()
```

Get account information for an user
```
response = client.get_user('USER_ID')
```

Get user address
```
response = client.get_user_address('USER_ID')
```

Get accepted payment methods for an user
```
response = client.get_user_accepted_payment_methods('USER_ID')
```

Get application information
```
response = client.get_application('APPLICATION_ID')
```

Get user brands
```
response = client.get_user_brands('USER_ID')
```

Get project information
```
response = client.get_project('PROJECT_ID')
```

Get project information
```
response = client.get_project('PROJECT_ID')
```

Get sites
```
response = client.get_sites(')
```

Get listing types
```
response = client.get_listing_types('SITE_ID')
```

Get listing exposures
```
response = client.get_listing_exposures('SITE_ID')
```

Get categories
```
response = client.get_categories('SITE_ID')
```

Get category
```
response = client.get_category('CATEGORY_ID')
```

Get category attributes
```
response = client.get_category_attributes('CATEGORY_ID')
```

Get countries
```
response = client.get_countries()
```

Get country
```
response = client.get_country('COUNTRY_ID')
```

Get state
```
response = client.get_state('STATE_ID')
```

Get city
```
response = client.get_city('CITY_ID')
```

Get currencies
```
response = client.get_currencies()
```

Get currency
```
response = client.get_currency('CURRENCY_ID')
```

List item
```
item = {'title': 'Test item - Moto G 4th Gen', 'condition': 'used', 'category_id': 'MCO174749', 'price': 10,
        'currency_id': 'COP',
        'available_quantity': 1, 'buying_mode': 'buy_it_now', 'listing_type_id': 'free', 'warranty': '24 months',
        'video_id': 'zQF96f01duA',
        'pictures': ['https://mxmoto.vteximg.com.br/arquivos/ids/156297-600-600/92849LYESAF5_1_1.png']}

response = client.list_item(**item)
```

## Requirements
- requests

## Tests
```
python tests/test_client.py
```
