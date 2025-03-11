from bs4 import BeautifulSoup

class EnSUNAT:
    def __init__(self):
        self.TipoRespuesta = None
        self.MensajeRespuesta = None
        self.RazonSocial = None
        self.TipoContribuyente = None
        self.NombreComercial = None
        self.FechaInscripcion = None
        self.FechaInicioActividades = None
        self.EstadoContribuyente = None
        self.CondicionContribuyente = None
        self.DomicilioFiscal = None
        self.ActividadesEconomicas = None
        self.ComprobantesPago = None
        self.SistemaEmisionComprobante = None
        self.AfiliadoPLEDesde = None
        self.Padrones = None

def extraer_contenido_entre_tag_string(cadena, nombre_inicio, nombre_fin):
    inicio = cadena.find(nombre_inicio)
    if inicio == -1:
        return ""
    inicio += len(nombre_inicio)
    fin = cadena.find(nombre_fin, inicio)
    if fin == -1:
        return ""
    return cadena[inicio:fin]

def extraer_contenido_entre_tag(cadena, posicion, nombre_inicio, nombre_fin):
    arr_respuesta = None
    posicion_inicio = cadena.find(nombre_inicio, posicion)
    if posicion_inicio > -1:
        posicion_inicio += len(nombre_inicio)
        if not nombre_fin:
            arr_respuesta = [str(len(cadena)), cadena[posicion_inicio:]]
        else:
            posicion_fin = cadena.find(nombre_fin, posicion_inicio)
            if posicion_fin > -1:
                posicion = posicion_fin + len(nombre_fin)
                arr_respuesta = [str(posicion), cadena[posicion_inicio:posicion_fin]]
    return arr_respuesta

def obtener_datos(contenido_html):
    oEnSUNAT = EnSUNAT()
    nombre_inicio = "<HEAD><TITLE>"
    nombre_fin = "</TITLE></HEAD>"
    contenido_busqueda = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
    
    if contenido_busqueda == ".:: Pagina de Mensajes ::.":
        nombre_inicio = "<p class=\"error\">"
        nombre_fin = "</p>"
        oEnSUNAT.TipoRespuesta = 2
        oEnSUNAT.MensajeRespuesta = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
    elif contenido_busqueda == ".:: Pagina de Error ::.":
        nombre_inicio = "<p class=\"error\">"
        nombre_fin = "</p>"
        oEnSUNAT.TipoRespuesta = 3
        oEnSUNAT.MensajeRespuesta = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
    else:
        oEnSUNAT.TipoRespuesta = 2
        nombre_inicio = "<div class=\"list-group\">"
        nombre_fin = "<div class=\"panel-footer text-center\">"
        contenido_busqueda = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
        
        if contenido_busqueda == "":
            nombre_inicio = "<strong>"
            nombre_fin = "</strong>"
            oEnSUNAT.MensajeRespuesta = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
            if oEnSUNAT.MensajeRespuesta == "":
                oEnSUNAT.MensajeRespuesta = "No se encuentra las cabeceras principales del contenido HTML"
        else:
            contenido_html = contenido_busqueda
            oEnSUNAT.MensajeRespuesta = "Mensaje del inconveniente no especificado"
            nombre_inicio = "<h4 class=\"list-group-item-heading\">"
            nombre_fin = "</h4>"
            resultado_busqueda = contenido_html.find(nombre_inicio)
            
            if resultado_busqueda > -1:
                resultado_busqueda += len(nombre_inicio)
                arr_resultado = extraer_contenido_entre_tag(contenido_html, resultado_busqueda, nombre_inicio, nombre_fin)
                if arr_resultado:
                    oEnSUNAT.RazonSocial = arr_resultado[1]

                    # Tipo Contribuyente
                    nombre_inicio = "<p class=\"list-group-item-text\">"
                    nombre_fin = "</p>"
                    arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                    if arr_resultado:
                        oEnSUNAT.TipoContribuyente = arr_resultado[1]

                        # Nombre Comercial
                        arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                        if arr_resultado:
                            oEnSUNAT.NombreComercial = arr_resultado[1].replace("\r\n", "").replace("\t", "").strip()

                            # Fecha de Inscripción
                            arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                            if arr_resultado:
                                oEnSUNAT.FechaInscripcion = arr_resultado[1]

                                # Fecha de Inicio de Actividades
                                arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                if arr_resultado:
                                    oEnSUNAT.FechaInicioActividades = arr_resultado[1]

                                    # Estado del Contribuyente
                                    arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                    if arr_resultado:
                                        oEnSUNAT.EstadoContribuyente = arr_resultado[1].strip()

                                        # Condición del Contribuyente
                                        arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                        if arr_resultado:
                                            oEnSUNAT.CondicionContribuyente = arr_resultado[1].strip()

                                            # Domicilio Fiscal
                                            arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                            if arr_resultado:
                                                oEnSUNAT.DomicilioFiscal = arr_resultado[1].strip()

                                                # Actividad(es) Económica(s)
                                                nombre_inicio = "<tbody>"
                                                nombre_fin = "</tbody>"
                                                arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                                if arr_resultado:
                                                    oEnSUNAT.ActividadesEconomicas = arr_resultado[1].replace("\r\n", "").replace("\t", "").strip()

                                                    # Comprobantes de Pago c/aut. de impresión (F. 806 u 816)
                                                    arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                                    if arr_resultado:
                                                        oEnSUNAT.ComprobantesPago = arr_resultado[1].replace("\r\n", "").replace("\t", "").strip()

                                                        # Sistema de Emisión Electrónica
                                                        arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                                        if arr_resultado:
                                                            oEnSUNAT.SistemaEmisionComprobante = arr_resultado[1].replace("\r\n", "").replace("\t", "").strip()

                                                            # Afiliado al PLE desde
                                                            nombre_inicio = "<p class=\"list-group-item-text\">"
                                                            nombre_fin = "</p>"
                                                            arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                                            if arr_resultado:
                                                                oEnSUNAT.AfiliadoPLEDesde = arr_resultado[1]

                                                                # Padrones
                                                                nombre_inicio = "<tbody>"
                                                                nombre_fin = "</tbody>"
                                                                arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                                                if arr_resultado:
                                                                    oEnSUNAT.Padrones = arr_resultado[1].replace("\r\n", "").replace("\t", "").strip()

                                                                    oEnSUNAT.TipoRespuesta = 1
                                                                    oEnSUNAT.MensajeRespuesta = "Ok"
    
    return oEnSUNAT

def obtener_datos2(contenido_html):
    oEnSUNAT = EnSUNAT()
    nombre_inicio = "<HEAD><TITLE>"
    nombre_fin = "</TITLE></HEAD>"
    contenido_busqueda = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
    
    if contenido_busqueda == ".:: Pagina de Mensajes ::.":
        nombre_inicio = "<p class=\"error\">"
        nombre_fin = "</p>"
        oEnSUNAT.TipoRespuesta = 2
        oEnSUNAT.MensajeRespuesta = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
    elif contenido_busqueda == ".:: Pagina de Error ::.":
        nombre_inicio = "<p class=\"error\">"
        nombre_fin = "</p>"
        oEnSUNAT.TipoRespuesta = 3
        oEnSUNAT.MensajeRespuesta = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
    else:
        oEnSUNAT.TipoRespuesta = 2
        nombre_inicio = "<div class=\"list-group\">"
        nombre_fin = "<div class=\"panel-footer text-center\">"
        contenido_busqueda = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
        
        if contenido_busqueda == "":
            nombre_inicio = "<strong>"
            nombre_fin = "</strong>"
            oEnSUNAT.MensajeRespuesta = extraer_contenido_entre_tag_string(contenido_html, nombre_inicio, nombre_fin)
            if oEnSUNAT.MensajeRespuesta == "":
                oEnSUNAT.MensajeRespuesta = "No se encuentra las cabeceras principales del contenido HTML"
        else:
            contenido_html = contenido_busqueda
            oEnSUNAT.MensajeRespuesta = "Mensaje del inconveniente no especificado"
            nombre_inicio = "<h4 class=\"list-group-item-heading\">"
            nombre_fin = "</h4>"
            resultado_busqueda = contenido_html.find(nombre_inicio)
            
            if resultado_busqueda > -1:
                resultado_busqueda += len(nombre_inicio)
                soup = BeautifulSoup(contenido_html, 'html.parser')
                # Está mal
                oEnSUNAT.RazonSocial = soup.find('h4', class_='list-group-item-heading').text.strip() 
                
                # Tipo Contribuyente
                oEnSUNAT.TipoContribuyente = soup.find('p', class_='list-group-item-text').text.strip()
                
                # Nombre Comercial
                oEnSUNAT.NombreComercial = soup.find_all('p', class_='list-group-item-text')[1].text.strip()
                
                # Fecha de Inscripción
                oEnSUNAT.FechaInscripcion = soup.find_all('p', class_='list-group-item-text')[2].text.strip()
                
                # Fecha de Inicio de Actividades
                oEnSUNAT.FechaInicioActividades = soup.find_all('p', class_='list-group-item-text')[3].text.strip()
                
                # Estado del Contribuyente
                oEnSUNAT.EstadoContribuyente = soup.find_all('p', class_='list-group-item-text')[4].text.strip()
                
                # Condición del Contribuyente
                oEnSUNAT.CondicionContribuyente = soup.find_all('p', class_='list-group-item-text')[5].text.strip()
                
                # Domicilio Fiscal
                oEnSUNAT.DomicilioFiscal = soup.find_all('p', class_='list-group-item-text')[6].text.strip()
                
                # Actividad(es) Económica(s)
                oEnSUNAT.ActividadesEconomicas = soup.find('tbody').text.strip()
                
                # Comprobantes de Pago c/aut. de impresión (F. 806 u 816)
                oEnSUNAT.ComprobantesPago = soup.find_all('tbody')[1].text.strip()
                
                # Sistema de Emisión Electrónica
                oEnSUNAT.SistemaEmisionComprobante = soup.find_all('tbody')[2].text.strip()
                
                # Afiliado al PLE desde
                oEnSUNAT.AfiliadoPLEDesde = soup.find_all('p', class_='list-group-item-text')[7].text.strip()
                
                # Padrones
                oEnSUNAT.Padrones = soup.find_all('tbody')[3].text.strip()
                
                oEnSUNAT.TipoRespuesta = 1
                oEnSUNAT.MensajeRespuesta = "Ok"
    
    return oEnSUNAT