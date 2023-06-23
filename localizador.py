import math
import requests
import json
import subprocess
import geocoder
import folium
import webbrowser


# Função para obter a localização a partir do endereço MAC
def get_location(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    response = requests.get(url)
    location = json.loads(response.content)
    return location

# Função para estimar a distância a partir do RSSI
def estimate_distance(rssi, tx_power, n):
    ratio = rssi * 1.0 / tx_power
    if ratio < 1.0:
        return math.pow(ratio, 10)
    else:
        return (0.89976) * math.pow(ratio, 7.7095) + 0.111

# Função para obter endereço IP da rede WiFi
def obter_endereco_ip_wifi():
    try:
        output = subprocess.check_output(["ipconfig"]).decode("utf-8")
        output = output[output.index("Wireless LAN adapter Wi-Fi:"):]
        output = output[output.index("IPv4 Address. . . . . . . . . . ."):].strip()
        ip_address = output[len("IPv4 Address. . . . . . . . . . . . . . "):output.index("(Preferred)")]
        return ip_address
    except:
        return None

# Função para obter a localização do endereço IP
def obter_localizacao_por_ip(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = json.loads(response.content.decode())
    if data["status"] == "success":
        lat = data["lat"]
        lon = data["lon"]
        return lat, lon
    else:
        return None

# Função para estimar a distância entre dois pontos geográficos em metros
def estimar_distancia(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians

    # Raio médio da Terra em metros necessário para calcular
    R = 6371000

    # Conversão para radianos
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Fórmula de Haversine para localização em dois pontos, usado em coordenadas  
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance

# Função para obter a latitude e longitude do usuário
def obter_coordenadas_usuario():
    g = geocoder.ip('me')
    if g.ok:
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        return latitude, longitude
    return None

# Obter as coordenadas do usuário
coordenadas_usuario = obter_coordenadas_usuario()

if coordenadas_usuario:
    latitude_usuario, longitude_usuario = coordenadas_usuario
    print("Latitude do usuário:", latitude_usuario)
    print("Longitude do usuário:", longitude_usuario)
else:
    print("Não foi possível obter as coordenadas do usuário.")

# Obter endereço MAC
mac_address = get_mac_address()

# Obter localização a partir do endereço MAC
location = get_location(latitude_usuario, longitude_usuario)

print("Localização do usuário:", location)

# Criar o mapa usando a biblioteca Folium
mapa = folium.Map(location=[latitude_usuario, longitude_usuario], zoom_start=15)

# Adicionar um marcador para a localização do usuário
folium.Marker([latitude_usuario, longitude_usuario], popup="Usuário").add_to(mapa)

# Salvar o mapa em um arquivo HTML
mapa.save('mapa.html')

# Abrir o arquivo HTML no navegador automaticamente
webbrowser.open('mapa.html')