import requests
from config import ACCESS_TOKEN, API_BASE_URL

def get_auth_status():
    """
    Kontrol için TMDB API'sine yetkilendirme başlatir.
    Bearer token kullanarak bir istek gönderir ve erişimi doğrular.
    """
    url = f"{API_BASE_URL}authentication"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Authentication successful!")
        return response.json()
    else:
        print(f"Authentication failed! Status Code: {response.status_code}")
        print(response.text)
        return None

def make_request(endpoint, params=None):
    """
    Genel bir API isteği gönderir.
    :param endpoint: TMDB API'sine özel uç nokta (ör. 'movie/11').
    :param params: İsteğe özel sorgu parametreleri.
    :return: API yaniti JSON formatinda.
    """
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        # print("make_request okey")
        return response.json()
    else:
        # print(f"make_request hatali! Status Code: {response.status_code}")
        # print(response.text)
        return None
