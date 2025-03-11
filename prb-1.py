import requests
from bs4 import BeautifulSoup
from Extraccion import  obtener_datos

def consultar_ruc(ruc):
    url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.62 Safari/537.36'
    }
    
    session = requests.Session()
    # Solicitud inicial
    response = session.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return "Error al acceder a la página principal"
        
    # 2 parte de la petición 
    numeroDNI = "12345678"

    # Datos para la solicitud POST
    data = {
        'accion': 'consPorTipdoc',
        'razSoc': '',
        'nroRuc': '',
        'nrodoc': '12345678',
        'contexto': 'ti-it',
        'modo': '1',
        'search1': '',
        'rbtnTipo': '2',
        'tipdoc': '1',
        'search2': numeroDNI,
        'search3': '',
        'codigo': ''
    } 
    # URL para la solicitud POST
    post_url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
    
    # Solicitud POST
    post_response = session.post(post_url, headers=headers, data=data)

    #print(post_response.content)
    if post_response.status_code != 200:
        return "Error al realizar la solicitud POST"
    
    soup = BeautifulSoup(post_response.content, 'html.parser')
    num_rnd_input = soup.find('input', {'name': 'numRnd'})
    if not num_rnd_input:
        return "Error al encontrar el campo numRnd"
    
    num_rnd_value = num_rnd_input['value']

    data = {
        'accion': 'consPorRuc',
         'actReturn': '1',
          'nroRuc': ruc,
           'numRnd': num_rnd_value,
            'modo': '1'
    }

    # URL para la solicitud POST

    post_response = session.post(post_url, headers=headers, data=data)
    if post_response.status_code != 200:
        return "Error al realizar la solicitud POST"

    soup = BeautifulSoup(post_response.content, 'html.parser')
    
     # Extraer el valor del campo desRuc
    des_ruc_input = soup.find('input', {'name': 'desRuc'})
    if des_ruc_input:
        des_ruc_value = des_ruc_input['value']
        print(f"Razón Social: {des_ruc_value}")
    else:
        print("No se encontró el campo desRuc")
    

    oEnSUNAT = obtener_datos(post_response.text)
    print(oEnSUNAT.__dict__)


    return "Solicitud POST realizada con éxito"
    # Extraer el nombre comercial
    # list_group_items = soup.find_all('div', class_='list-group-item')
    # if len(list_group_items) >= 3:
    #     nombre_comercial_div = list_group_items[2]
    #     nombre_comercial = nombre_comercial_div.find('p', class_='list-group-item-text').get_text(strip=True)
    #     print(f"Nombre Comercial: {nombre_comercial}")
    # else:
    #     print("No se encontró el nombre comercial")
    
    # return "Solicitud POST realizada con éxito"

# Ejemplo de uso
ruc = "20106897914"
estado_ruc = consultar_ruc(ruc)
#print(estado_ruc)