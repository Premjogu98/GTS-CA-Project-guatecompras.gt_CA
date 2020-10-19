from selenium import webdriver
import time
from datetime import datetime
import global_var
import html
import ctypes
import wx
import sys, os
from googletrans import Translator
from selenium.webdriver.chrome.options import Options
from Scraping_Things import Scrap_data
app = wx.App()


def ChromeDriver():
    chrome_options = Options()
    chrome_options.add_extension('C:\\Translation EXE\\BrowsecVPN.crx')
    browser = webdriver.Chrome(executable_path=str(f"C:\\Translation EXE\\chromedriver.exe"),chrome_options=chrome_options)
    # browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between ( 5 ) SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(5)  # WAIT UNTIL CHANGE THE MANUAL VPN SETtING
    browser.get("https://www.guatecompras.gt/concursos/consultaConAvanz.aspx")
    browser.maximize_window()
    time.sleep(1)
    for Click_Estatus in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_ddlEstatus"]/option[3]'):
        Click_Estatus.click()
        time.sleep(3)
        break
    for Fecha in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_ddlTipoFecha"]/option[1]'):
        Fecha.click()
        time.sleep(8)
        break

    From_date = global_var.From_Date.lower().replace('january', 'enero').replace('february', 'febrero').replace('march', 'marzo') \
        .replace('april', 'abril').replace('may', 'Mayo').replace('june', 'junio').replace('july', 'julio') \
        .replace('august', 'agosto').replace('september', 'septiembre').replace('october', 'octubre') \
        .replace('november', 'noviembre').replace('december', 'diciembre')

    for SetFrom_date in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_txtFechaIni"]'):
        browser.execute_script("arguments[0].value = arguments[1]" , SetFrom_date , str(From_date))
        break
    time.sleep(3)

    To_date = global_var.To_Date.lower().replace('january', 'enero').replace('february', 'febrero').replace('march', 'marzo')\
        .replace('april', 'abril').replace('may', 'Mayo').replace('june', 'junio').replace('july', 'julio') \
        .replace('august', 'agosto').replace('september', 'septiembre').replace('october', 'octubre') \
        .replace('november', 'noviembre').replace('december', 'diciembre')
    for SetTo_date in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_txtFechaFin"]'):
        browser.execute_script("arguments[0].value = arguments[1]" , SetTo_date , str(To_date))
        break
    time.sleep(3)

    for Search in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_btnBuscar"]'):
        Search.click()
        break
    for NO_data_Found in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_lblMensaje"]'):
        NO_data_Found = NO_data_Found.get_attribute('innerHTML').strip()
        if NO_data_Found == 'No existen concursos, de acuerdo a los parámetros elegidos.':
            wx.MessageBox(' -_-  No Data Found ', 'guatecompras.gt', wx.OK | wx.ICON_INFORMATION)
            browser.close()
            sys.exit()
        break
    a = True
    while a == True:
        for if_found_table in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]'):
            time.sleep(2)
            Collect_link(browser)
            break

def Collect_link(browser):
    pages = browser.find_elements_by_xpath('//*[@class="TablaPagineo"]/td/a')
    pages_count = 0
    if len(pages) == 0:
        pages_count = 1
    else:
        pages_count = int(len(pages))
    Main_tender_detail_list = []
    for page_range in range(1, pages_count+1, 1):
        tr_count = 2
        for tender_id in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr/td[1]/div/span[1]'):
            tender_detail_list = []
            tender_id = tender_id.get_attribute('innerText').strip()
            tender_detail_list.append(tender_id)
            for publish_date in browser.find_elements_by_xpath(f'//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr[{str(tr_count)}]/td[1]/div/span[2]'):
                publish_date = publish_date.get_attribute('innerText').replace('..','.').strip()
                tender_detail_list.append(publish_date)
                break
            for tender_href in browser.find_elements_by_xpath(f'//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr[{str(tr_count)}]/td[2]/div/div/a'):
                tender_href = tender_href.get_attribute('href').strip()
                tender_detail_list.append(tender_href)
                break
            Main_tender_detail_list.append(tender_detail_list)
            tr_count += 1
        if len(pages) != 0:
            while True:
                try:
                    for next_page in browser.find_elements_by_xpath(f'//*[@class="TablaPagineo"]/td/a[{str(page_range)}]'):
                        next_page.click()
                        time.sleep(10)
                        break
                    break
                except:
                    print('Next Page Error')      
            tr_count = 2
    nav_links(Main_tender_detail_list,browser)

def nav_links(Main_tender_detail_list,browser):

    for details in Main_tender_detail_list:
        browser.get(details[2])
        time.sleep(2)
        get_htmlsource_text = ''
        for get_htmlsource in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_WUCDetalleConcurso_divDetalleConcurso"]'):
            get_htmlsource_text = get_htmlsource.get_attribute('outerHTML').strip()
            break
        for tabs in browser.find_elements_by_xpath('//*[@class="rtsUL"]/li/a'):
            tabs_text = tabs.get_attribute('innerText').strip()
            if 'Proceso de Adjudicación' in tabs_text:
                tabs.click()
                time.sleep(2)
                for tab_htmlsource in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_divContenidoTab"]'):
                    get_htmlsource_text += tab_htmlsource.get_attribute('outerHTML').strip()
                    break
                contactor_name = ''
                contact_amount = ''
                for contactor_name in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_wcuConsultaConcursoAdjudicaciones_acDocumentos"]/div[1]/table/tbody/tr/td[3]'):
                    contactor_name = contactor_name.get_attribute('innerText').strip()
                    break
                for contact_amount in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_wcuConsultaConcursoAdjudicaciones_acDocumentos"]/div[1]/table/tbody/tr/td[5]'):
                    contact_amount = contact_amount.get_attribute('innerText').replace(',','').strip()
                    break
                break
        get_htmlsource_text = get_htmlsource_text.replace('href="/concursos/','href="https://www.guatecompras.gt/concursos/').replace('href="/compradores/', 'href="https://www.guatecompras.gt/compradores/').replace('src="/imagenes/','src="https://www.guatecompras.gt/imagenes/').replace('position: fixed; left: 0px; top: 0px; z-index', '').replace('alt="Procesando"', '').replace('Por favor, espere un momento...', '').replace("indicator.gif", '').replace('href="/', 'href="https://www.guatecompras.gt/compradores/').replace('\n','')
        Entity_name_url = get_htmlsource_text.partition("Entidad:")[2].partition("</tr>")[0]
        Entity_name_url = Entity_name_url.partition('<a href="')[2].partition('\"')[0]
        Entity_name_Decoded_url = html.unescape(str(Entity_name_url))
        browser.get(Entity_name_Decoded_url)
        for Entity_name_URL_data in browser.find_elements_by_xpath('//*[@class="TablaForm3"]'):
            Entity_name_URL_data = Entity_name_URL_data.get_attribute("outerHTML")
            get_htmlsource_text += "<br><h2>Buyer Entity Detail</h2><br>" + Entity_name_URL_data
            break
        
        Scrap_data(browser, get_htmlsource_text,details,contactor_name,contact_amount)
        print(f" Total: {str(len(Main_tender_detail_list))} Duplicate: {str(global_var.duplicate)} Inserted: {str(global_var.inserted)}\n")
    ctypes.windll.user32.MessageBoxW(0, f"Total: {str(len(Main_tender_detail_list))}\nDuplicate: {str(global_var.duplicate)}\nInserted: {str(global_var.inserted)}", "guatecompras.gt", 1)
    browser.close()
    sys.exit()

ChromeDriver()