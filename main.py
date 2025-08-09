# main.py
import os, json, asyncio
from config.upgrade_criteria import json_subida_nivel
from core.auth_handler import authenticate_user
from core.brute_logic import procesar_bruto

def cargar_usuarios():
    env_json = os.getenv("BRUTOS_JSON")
    if env_json:
        return json.loads(env_json)
    # fallback para desarrollo local
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'data', 'datos.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

usuarios = cargar_usuarios()

async def main_async_processor():
    for usuario in usuarios:
        auth = authenticate_user(usuario["usuario"], usuario["contrasenia"])
        for bruto_name in usuario["brutos"]:
            await procesar_bruto(auth, bruto_name, json_subida_nivel, usuario["tournament"])

if __name__ == "__main__":
    asyncio.run(main_async_processor())
