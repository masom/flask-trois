from shopify_trois import Credentials

SHOPIFY_CREDENTIALS = Credentials(
    api_key='your api key',
    secret='your api key secret',
    scope=frozenset(['write_blogs', 'read_order'])
)
