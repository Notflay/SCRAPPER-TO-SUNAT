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
                                                oEnSUNAT.DomicilioFiscal = limpiar_espacios(arr_resultado[1].strip())

                                                # Actividad(es) Económica(s)
                                                nombre_inicio = "<tbody>"
                                                nombre_fin = "</tbody>"
                                                arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                                if arr_resultado:
                                                    oEnSUNAT.ActividadesEconomicas = extraer_comprobantes_pago(arr_resultado[1].replace("\r\n", "").replace("\t", "").strip())

                                                    # Comprobantes de Pago c/aut. de impresión (F. 806 u 816)
                                                    arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                                    if arr_resultado:
                                                        oEnSUNAT.ComprobantesPago = extraer_comprobantes_pago(arr_resultado[1])

                                                        # Sistema de Emisión Electrónica
                                                        arr_resultado = extraer_contenido_entre_tag(contenido_html, int(arr_resultado[0]), nombre_inicio, nombre_fin)
                                                        if arr_resultado:
                                                            #oEnSUNAT.SistemaEmisionComprobante = arr_resultado[1].replace("\r\n", "").replace("\t", "").strip()
                                                            oEnSUNAT.SistemaEmisionComprobante = limpiar_espacios(extraer_comprobantes_pago(arr_resultado[1]))

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
                                                                    oEnSUNAT.Padrones =  extraer_comprobantes_pago(arr_resultado[1].replace("\r\n", "").replace("\t", "").strip())

                                                                    oEnSUNAT.TipoRespuesta = 1
                                                                    oEnSUNAT.MensajeRespuesta = "Ok"
    
    return oEnSUNAT


def limpiar_espacios(texto):
    return ' '.join(texto.split()).strip()

def extraer_comprobantes_pago(html):
    soup = BeautifulSoup(html, 'html.parser')
    comprobantes = [td.get_text(strip=True) for td in soup.find_all('td')]
    return ', '.join(comprobantes)