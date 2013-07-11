from shopify_trois import Credentials

credentials = Credentials(
    api_key='your api key',
    secret='your api key secret',
    scope=frozenset['write_blog', 'read_order']
)
