import base64
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
class BrutoManager:
    def __init__(self, auth):
        """
        Constructor para BrutoManager.
        auth: instancia de la clase EternalTwinAuth que contiene la sesión y los tokens.
        """
        self.auth = auth  # Instancia de EternalTwinAuth
        self.session = auth.session  # Usamos la sesión de EternalTwinAuth
        self.brute=None


    def get_opponents(self, bruto_id):
        """
        Obtiene la lista de oponentes de un bruto de la arena.
        bruto_id: ID del bruto para obtener los oponentes.
        """
        print("#-------------------------------------------#\n\n")
        url_opponents = f"https://brute.eternaltwin.org/api/brute/{bruto_id}/get-opponents/27"
        
        headers = {
            "Authorization": f"Basic {self.auth.base64_auth_string.strip()}",
            "Content-Type": "application/json",
            "x-csrf-token": self.auth.csrf_token,
            "Accept": "application/json",
            "Origin": "https://brute.eternaltwin.org",
            "Referer": f"https://brute.eternaltwin.org/{bruto_id}/arena",
        }
        
        cookies = self.auth.get_cookies()  # Usamos las cookies de la sesión activa
        
        try:
            response = self.session.get(url_opponents, headers=headers, cookies=cookies)
            response.raise_for_status()  # Lanza un error si el status code no es 200
            opponents = response.json()  # Suponemos que la respuesta es en formato JSON
            print("Listado de oponentes obtenidos correctamente")
            return opponents
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los oponentes: {e}")
            return None

    
        
    def get_for_hook_info(self, bruto_name):
        """
        Funcion para obtener informacion de un bruto
        Realiza una solicitud GET a la URL 'for-hook' del bruto.
        bruto_id: ID del bruto.
        """
        print("#-------------------------------------------#\n")

        url_for_hook = f"https://elbruto.eternaltwin.org/api/brute/{bruto_name}/for-hook?"

        # Agregamos los headers necesarios, incluyendo el csrf-token
        headers = {
            "Authorization": f"Basic {self.auth.base64_auth_string.strip()}",
            "Content-Type": "application/json",
            "x-csrf-token": self.auth.csrf_token,
            "Accept": "application/json",
            "Origin": "https://elbruto.eternaltwin.org",
            "Referer": f"https://elbruto.eternaltwin.org/{bruto_name}/cell",
        }

        # Usamos las cookies de la sesión activa
        cookies = self.auth.get_cookies()

        try:
            # Realizamos la solicitud GET
            response = self.session.get(url_for_hook, headers=headers, cookies=cookies)
            response.raise_for_status()  # Lanza un error si la respuesta no es 2xx
            print(f"Código de estado: {response.status_code}")
            print(f"Obtenida la informacion del bruto {bruto_name}")
            return response.json()  # Debería devolver un JSON con la respuesta
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la información de 'for-hook': {e}")
            return None
        
    def fight(self, brute1, brute2):
        """
        Inicia una pelea entre dos brutos.
        brute1: Nombre del primer bruto.
        brute2: Nombre del segundo bruto.
        """
        print("#-------------------------------------------#\n")
        url_fight = "https://brute.eternaltwin.org/api/fight?"  # URL para pelear
        
        # El payload con los nombres de los brutos
        data = {
            "brute1": brute1,  # Nombre del primer bruto
            "brute2": brute2,  # Nombre del segundo bruto
        }
        
        headers = {
            "Authorization": f"Basic {self.auth.base64_auth_string.strip()}",  # Autenticación básica
            "Content-Type": "application/json",  # Tipo de contenido
            "x-csrf-token": self.auth.token_before_percent,  # CSRF Token
            "Accept": "application/json",  # Esperamos una respuesta en formato JSON
            "Origin": "https://brute.eternaltwin.org",  # Referencia al origen
            "Referer": f"https://brute.eternaltwin.org/{brute1}/arena",  # Referencia al bruto
        }

        cookies = self.auth.get_cookies()  # Usamos las cookies de la sesión activa
        

        try:
            # Realizamos la solicitud PATCH
            response = self.session.patch(url_fight, json=data, headers=headers, cookies=cookies)
            response.raise_for_status()  # Si hay un error, levantará una excepción
            print(f"Código de estado de la pelea: {response.status_code}")
            if  response.status_code==200:
                print(f"{self.brute.name} vs {brute2}")
            return response.json()  # Devolvemos los datos de la pelea en formato JSON
        except requests.exceptions.RequestException as e:
            print(f"Error al intentar pelear: {brute2}")
            return response.status_code
        
    def register_to_tournament(self):
        print("#-------------------------------------------#\n")
        print("Registrando al torneo...")
        # Construir la URL de registro
        print(self.brute.name)
        url = f"https://brute.eternaltwin.org/api/tournament/{self.brute.name}/register?"
        
        # Headers necesarios para la solicitud
        headers = {
            "Authorization": f"Basic {self.auth.base64_auth_string.strip()}",  # Autenticación básica
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",  # Esperamos una respuesta en formato JSON
            "host": "brute.eternaltwin.org",  # Dominio de la solicitud
            "origin": "https://brute.eternaltwin.org",  # Origen de la solicitud
            "referer": f"https://brute.eternaltwin.org/{self.brute.name}/cell",  # Página de referencia
            "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",  # Información del navegador
            "sec-ch-ua-mobile": "?0",  # No es un dispositivo móvil
            "sec-ch-ua-platform": "\"Windows\"",  # Plataforma
            "sec-fetch-dest": "empty",  # Tipo de recurso solicitado
            "sec-fetch-mode": "cors",  # Modo de la solicitud
            "sec-fetch-site": "same-origin",  # Mismo origen
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",  # User Agent
            "x-csrf-token": self.auth.token_before_percent,
        }
        cookies = self.auth.get_cookies()  # Usamos las cookies de la sesión activa
        # Hacer la solicitud PATCH para registrarse en el torneo
        response = self.session.patch(url, headers=headers, cookies=cookies, json={})

        # Verificar la respuesta
        if response.status_code == 200:
            print("Registro al torneo exitoso!")
        else:
            print(f"Error al registrar al torneo: {response.status_code}")
            print(f"Respuesta: {response.text}")


    def SubidaNivel(self):
        """
        Devuelve codigo de error en caso de que no haya subida de nivel y nos devuelve la informacion de los choices
        """
        print("#-------------------------------------------#\n")
        url_lvlUp = f"https://brute.eternaltwin.org/api/brute/{self.brute.name}/level-up-choices?"  # URL para pelear
       
        
        headers = {
            "Authorization": f"Basic {self.auth.base64_auth_string.strip()}",  # Autenticación básica
            "Content-Type": "application/json",  # Tipo de contenido
            "x-csrf-token": self.auth.token_before_percent,  # CSRF Token
            "Accept": "application/json",  # Esperamos una respuesta en formato JSON
        }

    # Usamos las cookies de la sesión activa
        cookies = self.auth.get_cookies()

        try:
            # Realizamos la solicitud GET
            response = self.session.get(url_lvlUp, headers=headers, cookies=cookies)
            response.raise_for_status()  # Lanza un error si la respuesta no es 2xx
            print(f"Código de estado: {response.status_code}")
            print(f"Otenida la informacion del bruto {self.brute.name}")
            return response.json()  # Debería devolver un JSON con la respuesta
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la informacion de subida de nivel': {e}")
            
            return response.status_code
        
    def obtener_recompensas(self,data):
        """
        Me devuelve dos variables con la informacion de las dos posibles recompensas a elegir
        """
        print("#-------------------------------------------#\n")
        recompensa_izquierda = None
        recompensa_derecha = None

        for choice in data['choices']:
            if choice['path'][-1] == 'LEFT':
                if choice['type'] == 'weapon' and choice['weapon'] is not None:
                    recompensa_izquierda = choice['weapon']
                elif choice['type'] == 'skill' and choice['skill'] is not None:
                    recompensa_izquierda = choice['skill']
                elif choice['type'] == 'stats' and choice['stat1'] is not None:
                    recompensa_izquierda = f"{choice['stat1']} +{choice['stat1Value']}"
            elif choice['path'][-1] == 'RIGHT':
                if choice['type'] == 'weapon' and choice['weapon'] is not None:
                    recompensa_derecha = choice['weapon']
                elif choice['type'] == 'skill' and choice['skill'] is not None:
                    recompensa_derecha = choice['skill']
                elif choice['type'] == 'stats' and choice['stat1'] is not None:
                    recompensa_derecha = f"{choice['stat1']} +{choice['stat1Value']}"

        return recompensa_izquierda, recompensa_derecha
    

    def elegir_recompensa(self, recompensa_izquierda, recompensa_derecha, json_recompensas):
        """
        Elije la recompensa en funcion del json_recompensas elige una de las dos variables
        Puede devolver que se revise a mano
        """
        # Verificar si ambas recompensas son de tipo mascota
        if recompensa_izquierda in json_recompensas["mascotas"] and recompensa_derecha in json_recompensas["mascotas"]:
            # Si ambas son mascotas, elegir la que esté primero en la lista
            if json_recompensas["mascotas"].index(recompensa_izquierda) < json_recompensas["mascotas"].index(recompensa_derecha):
                return recompensa_izquierda
            else:
                return recompensa_derecha
            
        # Si una recompensa es una mascota y la otra es habilidad o arma, preferimos la mascota
        elif recompensa_izquierda in json_recompensas["mascotas"]:
            return recompensa_izquierda
        elif recompensa_derecha in json_recompensas["mascotas"]:
            return recompensa_derecha

        # Verificar si ambas recompensas son de tipo habilidad
        elif recompensa_izquierda in json_recompensas["habilidades"] and recompensa_derecha in json_recompensas["habilidades"]:
            # Si ambas son habilidades, elegir la que esté primero en la lista
            if json_recompensas["habilidades"].index(recompensa_izquierda) < json_recompensas["habilidades"].index(recompensa_derecha):
                return recompensa_izquierda
            else:
                return recompensa_derecha
        
        # Verificar si ambas recompensas son de tipo arma
        elif recompensa_izquierda in json_recompensas["armas"] and recompensa_derecha in json_recompensas["armas"]:
            # Si ambas son armas, elegir la que esté primero en la lista
            if json_recompensas["armas"].index(recompensa_izquierda) < json_recompensas["armas"].index(recompensa_derecha):
                return recompensa_izquierda
            else:
                return recompensa_derecha
        
        # Si una recompensa es habilidad y la otra es arma o atributo, preferimos la habilidad
        elif recompensa_izquierda in json_recompensas["habilidades"]:
            return recompensa_izquierda
        elif recompensa_derecha in json_recompensas["habilidades"]:
            return recompensa_derecha


        # Si ninguna de las recompensas es válida, revisamos a mano
        else:
            return "Hay que revisar a mano"


    def subir_nivel(self,direction):
        """
        Sube de nivel elige la opcion mejor
        """
        print("#-------------------------------------------#\n")
        url_lvlUp = f"https://brute.eternaltwin.org/api/brute/{self.brute.name}/level-up?" 
       
        
        headers = {
            "Authorization": f"Basic {self.auth.base64_auth_string.strip()}",  # Autenticación básica
            "Content-Type": "application/json",  # Tipo de contenido
            "x-csrf-token": self.auth.token_before_percent,  # CSRF Token
            "Accept": "application/json",  # Esperamos una respuesta en formato JSON
        }


        data = {
            "choice": direction,  # direcion de la recompensa
        }
    # Usamos las cookies de la sesión activa
        cookies = self.auth.get_cookies()

        try:
            # Realizamos la solicitud PATCH
            response = self.session.patch(url_lvlUp, json=data, headers=headers, cookies=cookies)
            response.raise_for_status()  # Lanza un error si la respuesta no es 2xx
            print(f"Código de estado: {response.status_code}")
            print("Se ha elegido la recompensa")
            return response.json()  # Debería devolver un JSON con la respuesta
        except requests.exceptions.RequestException as e:
            print(f"Error no se ha podido elegir la recompensa': {e}")
            return response.status_code