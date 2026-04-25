#!/usr/bin/env python3
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import time

# Cargar keys
def load_keys():
    keys = {}
    with open('data_key.properties', 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                keys[key.strip()] = value.strip()
    return keys

class OAuthHandler(BaseHTTPRequestHandler):
    auth_code = None

    def do_GET(self):
        # Parsear la URL para obtener el código
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if 'code' in query_params:
            OAuthHandler.auth_code = query_params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>Autorizacion exitosa!</h1><p>Puedes cerrar esta ventana y volver a la terminal.</p>".encode('utf-8'))
            print(f"\n✓ Código de autorización recibido: {OAuthHandler.auth_code}")
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>Error</h1><p>No se recibio el codigo de autorizacion</p>".encode('utf-8'))

    def log_message(self, format, *args):
        # Silenciar logs de servidor
        pass

def exchange_code_for_token(client_id, client_secret, code):
    """Intercambiar el código de autorización por un access token"""
    url = "https://www.strava.com/api/v3/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al intercambiar código: {response.status_code}")
        print(response.text)
        return None

def save_token(access_token, refresh_token=None):
    """Guardar el access token en el archivo de propiedades"""
    keys = load_keys()
    keys['token'] = access_token
    if refresh_token:
        keys['refresh_token'] = refresh_token

    with open('data_key.properties', 'w') as f:
        for key, value in keys.items():
            f.write(f"{key}:{value}\n")
    print(f"✓ Token guardado en data_key.properties")

def main():
    keys = load_keys()
    client_id = keys.get('client_id')
    client_secret = keys.get('client_secret')

    if not client_id or not client_secret:
        print("Error: Faltan client_id o client_secret")
        return

    print("Iniciando servidor OAuth en localhost:80...")
    print("(Puede requerir permisos de administrador para puerto 80)\n")

    # Si el puerto 80 requiere sudo, usar puerto 8080
    try:
        # Intentar con puerto 80
        server = HTTPServer(('localhost', 80), OAuthHandler)
        port = 80
    except PermissionError:
        print("Puerto 80 requiere permisos. Usando puerto 8080...\n")
        server = HTTPServer(('localhost', 8080), OAuthHandler)
        port = 8080

    redirect_uri = f"http://localhost:{port}"

    # URL de autorización
    auth_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope=read,activity:read_all"

    print(f"Abriendo navegador para autorización...")
    print(f"URL: {auth_url}\n")

    # Abrir navegador
    webbrowser.open(auth_url)

    # Servir una sola solicitud
    server.handle_request()

    if not OAuthHandler.auth_code:
        print("Error: No se recibió el código de autorización")
        return

    print("\nIntercambiando código por access token...")
    token_data = exchange_code_for_token(client_id, client_secret, OAuthHandler.auth_code)

    if token_data:
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_at = token_data.get('expires_at')

        save_token(access_token, refresh_token)
        print(f"✓ Access token obtenido exitosamente")
        print(f"✓ Expira en: {time.ctime(expires_at)}")
        print(f"\nPuedes usar tu token ahora: {access_token[:20]}...")
        return True
    else:
        print("Error al obtener el token")
        return False

if __name__ == '__main__':
    main()
