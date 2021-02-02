from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from threading import Thread
from bs4 import BeautifulSoup, SoupStrainer
from selenium.webdriver.chrome.options import Options
from datetime import date
# from Parsers import Parser, Parser2
# from WebAutomationRegister import Bot_Registro
import time
import os
import pickle
import json
import base64
import datetime
import requests
import timeit
# WebScraping

ThTime = 0.09
# C:\Users\ricar\Downloads\chromedriver_win32\chromedriver.exe

# Linux_Driver_Path = "/usr/src/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
# browser = webdriver.PhantomJS(Linux_Driver_Path)

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(
    executable_path='C:\\Users\\ricar\\Downloads\\chromedriver_win32\\chromedriver.exe')
winHandleBefore = browser.current_window_handle
# We have to change the webdriver path
# browser = webdriver.Chrome(chrome_options=options,
#                            executable_path="/usr/local/bin/chromedriver")
os.system('clear')
print("Chrome Browser Invoked")
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def ReadFileText(path):
    content = ""
    f = open(path, "r", encoding='utf-8')
    if f.mode == "r":
        content = f.readable()
        if content == True:
            text = f.readlines()[1:]
        else:
            return "The file is not readable in ReadFileText() function"
    return text


def Print_List(lst1, lst2, lst3):
    lstClases3 = []

    print("\n")
    print("PARSING LIST HACK1N....")
    print("Listing Clases....")
    print("\n")
    for p in lst1:
        time.sleep(ThTime)
        print(p)

    print("\n")
    print("PARSING LIST HACK1N....")
    print("Listing Masters....")
    print("\n")

    print("\n")
    for t in lst2:
        time.sleep(ThTime)
        print(t)

    print("\n")
    print("PARSING LIST HACK1N....")
    print("Listing the objects....")
    print("\n")

    print("\n")
    for q in lst1:
        lstClases3.append(Clases_Unitec(q[0], q[1]))

    print("\n")
    for l in lstClases3:
        print("CodeInfo: %s" % l.CodeInfo)
        print("Name: %s" % l.ClassName)
        time.sleep(0.200)
    return lstClases3


def border_msg(msg):
    count = len(msg)
    for i in range(0, len(msg)):
        count += 1

    count = count
    dash = "-"
    for i in range(0, count+1):
        dash += "-"

    count = count+2

    ver = "{a}{b:^{c}}{d}".format(a="|", b=msg, c=count, d="|")
    print(ver)


def Message_error_exception(Msg, status):
    border_msg(Msg)
    border_msg(status)


def find_option_from_table_tr(_XPath, _option=""):
    try:
        if _option == "":
            browser.refresh()
            time.sleep(2)
            lstMenu = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.XPATH, _XPath)))
            return lstMenu
        lstMenu = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.XPATH, _XPath)))
        lst_tr = lstMenu.find_elements_by_tag_name("tr")

        for tr in lst_tr:
            if tr.text.find(_option) >= 1:
                ActionChains(browser).click(tr).perform()
                time.sleep(2)
                return browser.current_window_handle
        print("We haven't found the option that you asked")
        return "Option not found"
    except:
        print("137")
        return "error"


def url_parser(_link):
    # /webapps/blackboard/content/listContent.jsp?
    #
    # course_id=
    # _137561_1&
    #
    # content_id=
    # _8204572_1&
    #
    # mode=
    # reset
    blackboard_domain = "https://unitec.blackboard.com"

    current_url_splited = _link.split('?')
    lstcourse_id = current_url_splited[1].split('&')
    lstcourseData = lstcourse_id[0].split('=')
    lstcourseContent = lstcourse_id[1].split('=')
    course_id = lstcourseData[1]
    content_id = lstcourseContent[1]
    url = blackboard_domain + current_url_splited[0]

    new_current_url = {"course_id": course_id,
                       "content_id": content_id, "mode": "reset"}
    Full_url = ("%s%s?course_id=%s&content_id=%s&mode=reset" % (
        blackboard_domain, current_url_splited[0], course_id, content_id))

    return url, new_current_url, Full_url


class Base_Header:
    def __init__(self, _name, _href):
        self.Name = _name
        self.link_href = _href


class Base_Detail:
    def __init__(self):
        self.Detail_Attachments = []
        self.Detail_Description = ""

    def Add_Detail(self, _detail):
        self.Detail.append(_detail)


class Child_Detail_Attachments(Base_Header):
    def __init__(self, _name, _href):
        Base_Header.__init__(self, _name, _href)


class Template_resource_activities_child:
    def __init__(self, _header_obj, _content_obj):
        self.Header = _header_obj
        self.Detail_Content = _content_obj


class clsSemana:
    def __init__(self):
        self.Semana = 0
        self.Recursos = []
        self.Actividades = []


class RegistroSecciones:
    def __init__(self, _seccion, _codigo, _materia, _hora, _aula, _dias, _disp, _catedratico):
        self.Seccion = _seccion
        self.Codigo = _codigo
        self.Materia = _materia
        self.Hora = _hora
        self.Aula = _aula
        self.Dias = _dias
        self.Disposicion = _disp
        self.Catedratico_de_la_Muerte = _catedratico


class RegistroClases:
    __lstEstados2 = {"--": "CONFIRMACION PENDIENTE", "APB": "APROBADA", "REP": "REPROBADA", "SD": "SIN DERECHO",
                     "RET": "RETIRADO", "CNF": "PENDIENTE DE CONFIRAMCION REQUISITO", "CNU": "PENDIENTE DE CONFIRMACION DE UVS"}
    cSemana = clsSemana()

    def __init__(self, _Modulo="", _seccion="", _nombreClase="", _HoraInicio="", _ExamenI="", _ExamenII="", _ExamenIII="", _Acumulacion="", _Repos="", _Nota="", _Estado="", _Faltas=""):
        self.Modulo = _Modulo
        self.Seccion = _seccion
        self.NombreClase = _nombreClase
        self.HoraInicio = _HoraInicio
        self.ExamenI = _ExamenI
        self.ExamenII = _ExamenII
        self.ExamenIII = _ExamenIII
        self.Acumulacion = _Acumulacion
        self.Repos = _Repos
        self.Nota = _Nota
        self.Estado = _Estado
        self.Faltas = _Faltas
        self.Anio = datetime.datetime.now().year
        self.lstSemana = []
        self.cookies = []

    def scrap_recursos_actividades(self, _sender_cookie, sendedCount):
        # Activitie_Resource = Template_resource_activities_child()
        resp = requests.get(url=browser.current_url, cookies={
                            "s_session_id": _sender_cookie})
        soup = BeautifulSoup(resp.text, 'html.parser')
        lst_item_li = soup.findAll('li')

        for li_item in lst_item_li:
            try:
                BaseHeader = Base_Header("", "")
                BaseDetail = Base_Detail()
                # Looking for the header'a' tag
                print("Scrap info for a specific content")
                if li_item['class'] == ['clearfix', 'liItem', 'read']:
                    try:
                        # Hdeaer (item clearfix)
                        divTag = li_item.find_all('div')
                        # sub_ItemList_header = li_item.find(lambda x: x['class'] == ['item', 'clearfix'])
                        sub_ItemList_header = divTag[0]
                        if sub_ItemList_header['class'] == ['item', 'clearfix']:
                            header_text = ""
                            header_href = ""
                            header = sub_ItemList_header.find_all('a')
                            if(len(header) != 0):
                                header_text = header[0].get_text()
                                header_href = header[0]['href']
                            else:
                                header_text = sub_ItemList_header.text
                            BaseHeader.Name = header_text.replace('\n', '').strip()
                            BaseHeader.link_href = header_href
                            print(BaseHeader.Name)
                            print(BaseHeader.link_href)

                        # Detail
                        # sub_ItemList_detail = li_item.find_all(lambda x: x['class'] == ['details'])
                        sub_ItemList_detail = divTag[1]
                        if sub_ItemList_detail['class'] == ['details']:
                            # attachments
                            header_attachments = sub_ItemList_detail.find_all('a')
                            # In the array 'header_attachments' we have elements <a> wich we do not want to
                            for item in range(len(header_attachments)):
                                if(header_attachments[item].attrs['href'] != '#contextMenu' and header_attachments[item].attrs['href'] != '#close'):
                                    header_attachment_text = header_attachments[item].get_text().strip()
                                    header_attachment_href = header_attachments[item]['href']
                                    BaseDetail.Detail_Attachments.append(Child_Detail_Attachments(
                                        header_attachment_text, header_attachment_href))
                                    print(header_attachment_text)
                                    print(header_attachment_href)

                            # Description
                            # sub_ItemList_detail = li_item.find_all(lambda x: x['class'] == ['details'])
                            Detail_div_text1 = sub_ItemList_detail.find_all('div')
                            for x in Detail_div_text1:
                                if x['class'] == ['vtbegenerated']:
                                    Detail_text = x.text.replace('\n', '')
                                    BaseDetail.Detail_Description = Detail_text
                                    print(Detail_text)
                    except:
                        print("Some attribute is not found. Good luck next time")
                    finally:
                        if browser.title.find("ACTIVIDADES") != -1:
                            self.cSemana.Actividades.append(
                                Template_resource_activities_child(BaseHeader, BaseDetail))
                            continue
                        self.cSemana.Recursos.append(
                            Template_resource_activities_child(BaseHeader, BaseDetail))
            except:
                print("Maybe the tag with attribute 'class' is not found. Good luck")

        browser.close()
        sendedCount -= 1
        return sendedCount

    def RecusrosOrActividades(self, handler, sendedCount):
        # # Get First 3 character of a string in python
        # first_chars = sample_str[0:3] R E C U R S O S = 8, A C T I V I D A D E S = 11
        # print('First 3 character : ', first_chars)
        # The cookie we want is this: 's_session_id'
        # time.sleep(2)
        browser.switch_to.window(handler)
        sender_cookie = ""
        browser_cookies = browser.get_cookies()
        for item in browser_cookies:
            if(item["name"] == "s_session_id"):
                sender_cookie = item["value"]
        try:
            return self.scrap_recursos_actividades(sendedCount=sendedCount, _sender_cookie=sender_cookie)

        except NoSuchElementException:
            print("handling some error happened in scrap_recursos_actividades function")

    def ScrapingElementLocation(self, _xpath):
        lstTable = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, _xpath)))
        lst = lstTable.find_elements_by_tag_name('li')
        return lst

    def ScrapingBySemana(self, handler, sendedCount):
        Semana_FunctionCount = sendedCount
        title_fixed = ""
        list_Container_xpath = "//*[@id='content_listContainer']"
        lst = []

        browser.switch_to.window(handler)
        time.sleep(0.4)
        os.system('cls')
        print("Processing %s " % browser.title)
        lst = self.ScrapingElementLocation(list_Container_xpath)
        for item in lst:
            # We gotta fix the consideration of this part
            title_fixed = item.text[0:15].upper()
            if title_fixed.find("RECURSOS") != -1 or title_fixed.find("ACTIVIDADES") != -1:
                print(title_fixed)
                item_a = item.find_element_by_tag_name('a')
                time.sleep(1)
                ActionChains(browser).key_down(Keys.CONTROL).click(item_a).key_up(Keys.CONTROL).perform()
                Semana_FunctionCount = Semana_FunctionCount + 1
                currentHandler = browser.window_handles[Semana_FunctionCount]
                CountReturned = self.RecusrosOrActividades(currentHandler, Semana_FunctionCount)
                Semana_FunctionCount = CountReturned
                browser.switch_to.window(browser.window_handles[Semana_FunctionCount])

        print("%s is Done \n" % browser.title[0:9])
        browser.close()
        Semana_FunctionCount -= 1
        return Semana_FunctionCount

    def ScrapingBySemanas(self, handler, sendedCount):  # Thinking
        try:
            # We are gonna need te course_id and the contetn_id for the specific class
            Semanas_FunctionCount = sendedCount
            browser.switch_to.window(handler)
            print(browser.title)
            SemanaCount = 0
            href_link = ""
            current_s_session_cookie = ""
            current_s_session_cookie_dict = {}
            time.sleep(1)
            SessionCookies = browser.get_cookies()
            self.cookies = SessionCookies
            for cookie in SessionCookies:
                if cookie['name'] == "s_session_id":
                    current_s_session_cookie = cookie['value']
                    current_s_session_cookie_dict = {
                        cookie['name']: current_s_session_cookie}
                    break

            r = requests.post(url=browser.current_url,
                              cookies=current_s_session_cookie_dict)
            time.sleep(1)
            print("bot: We are trying to click the CONTENIDO DEL CURSO button")
            print("bot: We are printing the content of the class Protocolos de redes\n")

            soup = BeautifulSoup(r.text, 'html.parser')
            con = soup.find(id="courseMenuPalette_contents")
            for li in con.contents:
                for link in li.find_all('a', href=True):
                    if link.text.find('Contenido del curso') >= 0:
                        href_link = link['href']
                        break
            full_url = url_parser(href_link)[2]

            browser.execute_script("window.open();")
            Semanas_FunctionCount = Semanas_FunctionCount + 1
            browser.switch_to.window(
                browser.window_handles[Semanas_FunctionCount])
            browser.get(url=full_url)
            time.sleep(0.2)
            print("%s \n" % browser.title)

            time.sleep(.1)
            ElementSemanas = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='content_listContainer']")))
            lista_Semana = ElementSemanas.find_elements_by_tag_name("li")
            time.sleep(.1)

            for Semana in lista_Semana:
                TempText = ""
                TempText = Semana.text.upper()
                if TempText.find("SEMANA") == -1:
                    continue
                ElementSemana = Semana.find_element_by_tag_name('a')
                TempText = ElementSemana.text.upper()
                if TempText.find("SEMANA") != -1:
                    time.sleep(0.5)
                    SemanaCount += 1
                    self.cSemana = clsSemana()
                    self.cSemana.Semana = SemanaCount
                    ActionChains(browser).key_down(Keys.CONTROL).click(
                        ElementSemana).key_up(Keys.CONTROL).perform()
                    Semanas_FunctionCount = Semanas_FunctionCount + 1
                    currentHandler = browser.window_handles[Semanas_FunctionCount]
                    CountReturned = self.ScrapingBySemana(
                        currentHandler, Semanas_FunctionCount)
                    self.lstSemana.append(self.cSemana)
                    Semanas_FunctionCount = CountReturned
                    browser.switch_to.window(
                        browser.window_handles[Semanas_FunctionCount])

            print("We are Done for this current class")
            browser.close()
            Semanas_FunctionCount -= 1
            return Semanas_FunctionCount

        except Exception as e:
            os.system('clear')
            print("Something went wrong in line 348\n\n")
            print(e.__doc__)
            os.system('killall chrome')
            browser.quit()
            exit()

            # Now I have an idea about how to solve the problem of how to scrap the resources
            # and activities by each current class

    @property
    def Seccion(self):
        return self.__Seccion

    @Seccion.setter
    def Seccion(self, value):
        self.__Seccion = value.strip()
        return self.__Seccion

    @property
    def HoraInicio(self):
        return self.__horaInicio

    @HoraInicio.setter
    def HoraInicio(self, value):
        self.__horaInicio = value.strip()
        return self.__horaInicio

    @property
    def Nota(self):
        return self.__nota

    @Nota.setter
    def Nota(self, value):
        self.__nota = value.strip()
        return self.__nota

    @property
    def ExamenI(self):
        return self.__examenI

    @ExamenI.setter
    def ExamenI(self, value):
        self.__examenI = value.replace(" ", "")
        return self.__examenI

    @property
    def ExamenII(self):
        return self.__examenII

    @ExamenII.setter
    def ExamenII(self, value):
        self.__examenII = value.strip()
        return self.__examenII

    @property
    def ExamenIII(self):
        return self.__examenIII

    @ExamenIII.setter
    def ExamenIII(self, value):
        self.__examenIII = value.strip()
        return self.__examenIII

    @property
    def Acumulacion(self):
        return self.__Acumulacion

    @Acumulacion.setter
    def Acumulacion(self, value):
        self.__Acumulacion = value.strip()
        return self.__Acumulacion

    @property
    def Repos(self):
        return self.__repos

    @Repos.setter
    def Repos(self, value):
        self.__repos = value.strip()
        return self.__repos

    @property
    def Estado(self):
        return self.__Estado

    @Estado.setter
    def Estado(self, value):
        for key in RegistroClases.__lstEstados2:
            if value == key:
                self.__Estado = RegistroClases.__lstEstados2[key]
                return

    @property
    def Faltas(self):
        return self.__Faltas

    @Faltas.setter
    def Faltas(self, value):
        if value == '--':
            self.__Faltas = 0
            return


class Clases_Unitec:
    def __init__(self, _codeInfo, _className):
        self.CodeInfo = _codeInfo
        self.ClassName = _className
        self.lstActivities = []


def Boot_Secciones():
    status = ""
    listado_Secciones = []

    status = find_option_from_table_tr(
        "//*[@id='menulayout']/tbody/tr/td/table", "Secciones Presencial")
    if status == "error" or status == "Option not found":
        return False
    time.sleep(1)
    xpath_table_seccion = "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table"
    lst = find_option_from_table_tr(xpath_table_seccion)
    lst_tr = lst.find_elements_by_tag_name("tr")
    for tr in lst_tr[1:]:
        column = tr.find_elements_by_tag_name("td")
        listado_Secciones.append(RegistroSecciones(
            column[0].text, column[1].text, column[2].text, column[3].text, column[4].text, column[5].text, column[6].text, column[7].text))
    # List max of 300 arrays


def Bot_Registro():
    os.system('cls')
    print("\n\n\nWe are hacking Unitec for fun HAHAHAHA xD")
    lst_Clases_Registro = []
    passw = ""
    account = 0
    campus = "CEUTEC SAP"

    Website_Page = "https://registro.unitec.edu/"
    Element_input1 = "cuenta"
    Element_input2 = "password"
    Element_input3 = "campus"
    Element_input4_Button = "Submit"

    file = open("UnitecCredential.txt", mode='r')
    all_of_it = file.read()
    all_of_it = all_of_it.split(',')
    passw = all_of_it[2]
    account = int(all_of_it[3])
    file.close()

    if(len(browser.window_handles) > 0):
        print("there are some windows handlers already")
    browser.switch_to_window(browser.window_handles[0])

    browser.get((Website_Page))
    cuenta = browser.find_element_by_name(Element_input1)
    pas = browser.find_element_by_name(Element_input2)
    camp = browser.find_element_by_name(Element_input3)
    sub = browser.find_element_by_name(Element_input4_Button)

    cuenta.send_keys(account)
    pas.send_keys(passw)
    camp.send_keys(campus)
    sub.click()

    handles = browser.window_handles

    browser.switch_to.window(handles[0])
    time.sleep(1)
    Items_bosy = WebDriverWait(browser, 1).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='menulayout']/tbody/tr/td/table")))
    Items_tr = Items_bosy.find_elements_by_tag_name("tr")

    for I in Items_tr:
        print(I.text)

    for RegistroItem in Items_tr:
        if RegistroItem.text.find("Rendimiento Semestral") >= 1:
            ActionChains(browser).click(RegistroItem).perform()
            break
    time.sleep(2)

    try:
        TempColumn2 = WebDriverWait(browser, 1).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]")))
        Items_table = WebDriverWait(browser, 1).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr[2]/td/table")))
        Items_tr = Items_table.find_elements_by_tag_name("tr")

        counter = 0
        for row in Items_tr[1:]:
            columns = row.find_elements_by_tag_name("td")
            lst_Clases_Registro.append(RegistroClases(columns[0].text, columns[1].text, columns[2].text, columns[3].text, columns[4].text,
                                                      columns[5].text, columns[6].text, columns[7].text, columns[8].text, columns[9].text, columns[10].text, columns[11].text))
            counter = counter + 1

        lst_Clases_Registro.reverse()
        print("Your clases are: \n")
        for LC in lst_Clases_Registro:
            print(LC.NombreClase)

        browser.execute_script("window.open();")
        browser.close()
        return lst_Clases_Registro
    except TimeoutException as exc:
        os.system("clear")
        print("\nNo se ha encontrado la tabla")
        print(TempColumn2.text)
        print(exc)
        print("bot: Creo que es temporada de matricula de clases Ricardo\n")
        return "SECCIONES"


def Boot_Unitec(lstRegistro):
    os.system('cls')
    print("Hack for fun kids....")

    password = ""
    username = ""
    count = 0
    lstCurrentClases = []
    Website_Page = "https://portal.unitec.edu"
    Element_User = "ctl03_tbUsuario"
    Element_Passwor = "ctl03_tbContrasena"
    Element_Submit = "ctl03_bIngresar"
    Element_Blackboard = "img3"
    browser.switch_to.window(browser.window_handles[0])

    try:

        verify = requests.get("https://www.google.com")
        print("Status code is: %s" % verify.status_code)

        file = open("UnitecCredential.txt", mode='r')
        all_of_it = file.read()
        all_of_it = all_of_it.split(',')
        username = all_of_it[0]
        password = all_of_it[1]
        file.close()

        lstCurrentClases.append(lstRegistro[1])
        # # importatnt code for later
        # for clase in lstRegistro:
        #     # if clase.Estado == "CONFIRMACION PENDIENTE":
        #     if clase.Modulo == '2':
        #         if clase.NombreClase.find("SOFTWARE II") >= 1:
        #             continue
        #         lstCurrentClases.append(clase)

        try:
            # browser.execute_script("window.open();")
            browser.get((Website_Page))
            # browser.switch_to()

            User = browser.find_element_by_id(Element_User)
            Pass = browser.find_element_by_id(Element_Passwor)
            Submit = browser.find_element_by_id(Element_Submit)

            User.send_keys(username)
            Pass.send_keys(password)
            Submit.click()
            # time.sleep(2)
        except:
            os.system('cls')
            print("We are already logged")

        browser.get((Website_Page))
        time.sleep(.1)
        try:
            exB = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, "ctl03_bContinuar")))
            exB.click()
        except:
            print("Error ocurred")

        BlackBoard = browser.find_element_by_id(Element_Blackboard)
        BlackBoard.click()

        browser.close()

        handles = browser.window_handles
        size = len(handles)

        for x in range(size):
            browser.switch_to.window(handles[x])
            print(browser.title)

        print("You are in \n %s" % browser.title)
        print("\nwaiting five seconds ...")
        time.sleep(.1)
        try:
            Agree_Button = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, "agree_button")))
            Agree_Button.click()
        except:
            print('Notr found')
        
        Insitucion_Label_td = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='MyInstitution.label']/a")))
        browser.execute_script("arguments[0].click();", Insitucion_Label_td)

        print("Waiting Five Seconds until the element is located")
        time.sleep(5)
        AcaClases = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='_3_1termCourses_noterm']/ul")))
        items = AcaClases.find_elements_by_tag_name("a")

        print("\nHERE WE ARE PRINTING THE <li> Elements, those that are about to be click\n")
        for ter in items:
            print(ter.text)
            time.sleep(ThTime)

        for T in items:
            for clases in lstCurrentClases:
                temp = ""
                temp = T.text.upper()
                if temp.startswith(clases.Seccion):
                    time.sleep(.2)
                    ActionChains(browser).key_down(Keys.CONTROL).click(T).key_up(Keys.CONTROL).perform()
                    count = count + 1

        handles = browser.window_handles
        size = len(handles)
        all_of_it = ""
        for hand in handles:
            print(hand)

        for X in range(size):
            if count == 0:
                return lstCurrentClases
            Y = browser.window_handles[count]
        # Problema El orden en que el bot hace el scraping es diferente al orden de como estan los objetos
        # To do: Revertir el orden en el que se hace el scarping para cada clase o revertir el orden de cuando  se guardan los objetos en Boot_Registro
            print('\n Proccesing %s \n' % Y)
            ScrapClass = lstCurrentClases[count - 1]
            Recount = ScrapClass.ScrapingBySemanas(handler=Y, sendedCount=count)
            s = json.dumps(ScrapClass.__dict__,default=lambda o: o.__dict__, indent=4)
            try:
                result = requests.post("http://localhost:3006/api/unitec/saveupdate", data=s, headers=headers)
                print(s)
                print(result.text)
            except:
                print("the request to the database failed")
            browser.switch_to.window(browser.window_handles[Recount])
            browser.close()
            Recount -= 1
            count = Recount
    except:
        os.system('clear')
        print("Something went wrong \n\n")
        browser.quit()


def fibonacci(number):
    if number == 0:
        return
    value = fibonacci(number - 1) + fibonacci(number - 2)
    print(value)
    return value


if __name__ == "__main__":

    start = timeit.default_timer()

    while True:
        lstregistro = Bot_Registro()
        lstClass = Boot_Unitec(lstregistro)
    stop = timeit.default_timer()

    print('Time: ', stop - start)

    Message_error_exception("Without errors", "Done")

# Let's run the damn thing
# WepApp coming soon for this WebBrowser Bot - PathFinderWide2.0
