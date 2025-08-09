import base64
import requests
from urllib.parse import urlparse, parse_qs
"""
Esta clase sirve para hacer conexion y obtener los diferentes token, codes etc, para poder autentificarte
y jugar al bruto

Resumen:
Obtiene el login de eternal twin, esto general un sid que servira decirle al servidor que usuario esta 
realizando las solicitudes y es unico
Obtiene un csrf token, es un mecanismo de seguridad utilizado 
para proteger a las aplicaciones web de un tipo de ataque conocido como CSRF (Cross-Site Request Forgery o Falsificación de Peticiones de Sitios Cruzados
luego obtiene un code 
"""
class EternalTwinAuth:
    def __init__(self, username, password_hex, client_id, redirect_uri):
        self.username = username
        self.password_hex = password_hex
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.session = requests.Session()
        self.csrf_token = None
        self.connexion_token = None
        self.token_before_percent=None
        self.user_id=None
        self.base64_auth_string=None

    def login(self):
        print("#-------------------------------------------#\n")
        print("LOGIN\nhttps://eternaltwin.org/api/v1/auth/self?method=Etwin")
        url_login = "https://eternaltwin.org/api/v1/auth/self?method=Etwin"
        headers_login = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://eternaltwin.org",
            "Referer": "https://eternaltwin.org/login",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }
        data_login = {
            "login": self.username,
            "password": self.password_hex,
        }

        try:
            response_login = self.session.put(url_login, json=data_login, headers=headers_login)
            response_login.raise_for_status()  # Si no es 200, lanza una excepción
        except requests.exceptions.RequestException as e:
            print(f"Error en el login: {e}")
            print(f"Código de estado: {response_login.status_code}")
            return False

        print("Login exitoso.")
        print(f"Código de estado: {response_login.status_code}")
        json_response = response_login.json()
        self.user_id = json_response.get('id')
        
        #print(f"Respuesta del login: {json_response}")
        
        #print(f"Respuesta del login: ")
        #print(json.dumps(json_response, indent=4))
        print(f"Cookies almacenadas después del login: {self.session.cookies.get_dict()}")
        sid = self.session.cookies.get('sid')
        print("SID: " + sid)        
        return True
    
    """
    Esta URL (https://eternaltwin.org/oauth/authorize) es donde inicias el proceso de 
    autorización con el servidor de autenticación. 
    Al redirigir al usuario allí, el servidor pedirá permiso para acceder a sus datos. 
    Una vez el usuario otorga los permisos, el servidor redirige de vuelta a tu aplicación a una 
    URL de "callback" (por ejemplo, https://brute.eternaltwin.org/oauth/callback), 
    añadiendo un parámetro code en la URL.
    """
    def authorize(self):
        print("#-------------------------------------------#\n")
        url_authorize = "https://eternaltwin.org/oauth/authorize"
        params = {
            "access_type": "offline",
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "scope": "base",
            "state": "",
        }

        headers_login = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://eternaltwin.org",
            "Referer": "https://eternaltwin.org/login",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }

        try:
            response_authorize = self.session.get(url_authorize, params=params, headers=headers_login)
            response_authorize.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error en la autorización: {e}")
            return None

        print("Redirección exitosa.")
        #print("URL de redirección:", response_authorize.url)
        return response_authorize.url

    def extract_code(self, redirect_url):
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        code = query_params.get('code', [None])[0]
        if code is None:
            print("No se pudo extraer el código de la URL.")
        return code

    def get_csrf_token(self):
        print("#-------------------------------------------#\n")
        url_csrf = "https://brute.eternaltwin.org/api/csrf?"
        response = self.session.get(url_csrf)
        if response.status_code == 200 or response.status_code == 304:
            print("Token CSRF obtenido correctamente.")
            self.csrf_token = self.session.cookies.get("csrfToken")
            if self.csrf_token:
                #print(f"Token CSRF: {self.csrf_token}")
                self.get_token_before_percent()
                return self.csrf_token
            else:
                print("No se encontró el token CSRF en las cookies.")
        else:
            print(f"Error al obtener el token CSRF. Código de estado: {response.status_code}")
        return None

    def get_access_token(self, code):
        print("#----------------------------------------#\n")
        url_token = "https://brute.eternaltwin.org/api/oauth/token"

        params = {
            "code": code
        }

        headers_token = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://brute.eternaltwin.org",
            "Referer": f"https://brute.eternaltwin.org/oauth/callback?code={code}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "x-csrf-token": self.csrf_token,
        }

        try:
            response_token = self.session.get(url_token, params=params, headers=headers_token)
            response_token.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener el token: {e}")
            return None

        json_response = response_token.json()
        self.connexion_token = json_response.get("connexionToken")
        if self.connexion_token:
            #print(f"Token de conexión: {self.connexion_token}")
            return self.connexion_token
        return None

    def authenticate_user(self):
        print("#-------------------------------------------#\n")
        print("Autentificando en el bruto...")
        url = "https://brute.eternaltwin.org/api/user/authenticate"
        data_authenticate = {
            "login": self.user_id,
            "token": self.connexion_token
        }
        login = self.user_id
        auth_string = f"{login}:{self.connexion_token}"
        self.base64_auth_string = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
        #print(f"Base64 auth string: {self.base64_auth_string}")

        headers = {
            "Authorization": f"Basic {self.base64_auth_string}",
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": self.token_before_percent,
        }

        cookies = {
            'csrfToken': self.csrf_token,
            'user': self.user_id,
            'token': self.connexion_token,
        }

        try:
            response = self.session.post(url, headers=headers, cookies=cookies, json=data_authenticate)
            response.raise_for_status()  # Verifica el status 200
        except requests.exceptions.RequestException as e:
            print(f"Error en la autenticación: {e}")
            return None
        print("Autentificacion exitosa")
        print(response.status_code)
        #print(response.json())
        return response

    def  get_token_before_percent(self):
        self.token_before_percent = self.csrf_token.split('%')[0]
        

    def get_cookies(self):
        """Método para obtener las cookies almacenadas en la sesión."""
        return self.session.cookies.get_dict()
    

    