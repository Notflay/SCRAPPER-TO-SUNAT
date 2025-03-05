
import requests
from bs4 import BeautifulSoup


#links
#http://impperu.ramo.com.br:7071/api/tipoCambio?later=0

def consulta_api():
    url = "http://impperu.ramo.com.br:7071/api/tipoCambio?later=0"
    session = requests.Session()
    print("prueba")
    response = session.get(url, timeout=10)

    if (response.status_code == 200):
        #es necesario que convierta a float para que pueda ser operado
        print(float(response.content))
        print("Conexion exitosa")

    

consulta_api()       

