from .eternal_twin_auth import EternalTwinAuth

from core.utils import random_sleep

def authenticate_user(username, password):
    password_hex = ''.join(format(ord(c), '02x') for c in password)
    client_id = "brute_production@clients"
    redirect_uri = "https://brute.eternaltwin.org/oauth/callback"
    
    auth = EternalTwinAuth(username, password_hex, client_id, redirect_uri)
    auth.login()
    random_sleep()
    authorize_url = auth.authorize()
    code = auth.extract_code(authorize_url)
    random_sleep()
    auth.get_csrf_token()
    random_sleep()
    auth.get_access_token(code)
    random_sleep()
    auth.authenticate_user()

    return auth
