import os
from flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app(
  'github',
    consumer_key=os.environ.get("GITHUB_CONSUMER_KEY"),   # consumer token
    consumer_secret=os.environ.get("GITHUB_CONSUMER_SECRET"),  # secret token
    request_token_params={"scope": "user:email"},  # add to request, specific for provider
    base_url="https://api.github.com/",  # service url
    request_token_url=None, # None for OAuth 2.0
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token", #
    authorize_url="https://github.com/login/oauth/authorize"
)