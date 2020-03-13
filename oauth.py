from seagull_settings import  oauth
import os

github = oauth.register(
  'github',
  authorize_url="https://github.com/login/oauth/authorize/",
  client_id=os.getenv("GITHUB_CLIENT_ID"),
  client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
  access_token_url=os.getenv("GITHUB_ACCESS_TOKEN_URL"),
  client_kwargs={
    'scope': 'user'
  }
)