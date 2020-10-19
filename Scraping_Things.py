import re
import time
import sys , os
import string
from datetime import datetime,timedelta
import global_var
import html
from Insert_On_Datbase import create_filename,insert_in_Local
import wx
import html
app = wx.App()


def Scrap_data(browser, get_htmlsource_text,details,contactor_name,contact_amount):

    SegFields = []
    for data in range(45):
        SegFields.append('')
    Decoded_get_htmlSource: str = html.unescape(str(get_htmlsource_text))
    Decoded_get_htmlSource: str = re.sub('\s+', ' ', str(Decoded_get_htmlSource)).replace("\n","").replace("<br>","")
    a = True
    while a == True:
        try:
            # ==================================================================================================================
            # Purchaser_Email ID

            Email_ID = Decoded_get_htmlSource.partition("Direcciones de Correo: </div>")[2].partition("</div>")[0]
            Email_ID = Email_ID.partition('<a href="')[2].partition('"')[0].replace('mailto:','')
            SegFields[1] = Email_ID.strip() # Purchaser_Email ID

            # ==================================================================================================================
            # Address

            Municipality = Decoded_get_htmlSource.partition("Municipio:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Municipality = re.sub(cleanr, '', Municipality).strip()
            Municipality = string.capwords(str(Municipality))

            Direction = Decoded_get_htmlSource.partition("Dirección:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Direction = re.sub(cleanr, '', Direction).strip()
            Direction = string.capwords(str(Direction))
            
            Phones = Decoded_get_htmlSource.partition("Teléfonos:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Phones = re.sub(cleanr, '', Phones)
            Phones = Phones.partition("ext.")[0].strip()

            Fax_Numbers = Decoded_get_htmlSource.partition("Números de Fax:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Fax_Numbers = re.sub(cleanr, '', Fax_Numbers).strip()
            Fax_Numbers = Fax_Numbers.partition("ext.")[0].strip()

            Postal_mail = Decoded_get_htmlSource.partition("Apartado Postal:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Postal_mail = re.sub(cleanr, '', Postal_mail).strip()

            if Postal_mail != "[--No Especificado--]":
                Collected_Address = Municipality + "," + Direction + "<br>\n" + "Teléfonos: " + Phones + "<br>\n" + "Números de Fax: " + Fax_Numbers + "<br>\n" + "Apartado Postal: " + Postal_mail
                SegFields[2] = Collected_Address
            else:
                Collected_Address = str(Municipality) + "," + str(Direction) + "<br>\n" + "Teléfonos: " + str(Phones)+ "<br>\n" + "Números de Fax: " + Fax_Numbers
                SegFields[2] = Collected_Address  # Purchaser_Address

            # ==================================================================================================================
            # 
            contactor_name = string.capwords(contactor_name)
            SegFields[3] = contactor_name.replace(',,',',')  # Contractor_name

            SegFields[7] = global_var.pur_country_code # Purchaser_Country

            SegFields[5] = global_var.cont_country_code  # Contractor_Country

            # ==================================================================================================================
            # Purchaser_URL

            Websites = Decoded_get_htmlSource.partition("Páginas Web:")[2].partition("</tr>")[0]
            Websites = Websites.partition("<a href=\"")[2].partition("\" target")[0].strip()
            if Websites != "[--No Especificado--]":
                SegFields[8] = Websites.strip()  # Purchaser_URL
            else:
                SegFields[8] = ""

            # ==================================================================================================================
            # Purchaser_name

            Entity = Decoded_get_htmlSource.partition("MasterGC_ContentBlockHolder_lblEntidad")[2].partition("</span>")[0]
            Entity = Entity.partition('">')[2].strip()
            if Entity != "":
                SegFields[12] = Entity.strip()
            else:
                SegFields[12] = ""

            # ==================================================================================================================
            # reference_no

            Tender_no = Decoded_get_htmlSource.partition("NOG:")[2].partition("</b>")[0]
            cleanr = re.compile('<.*?>')
            Tender_no = re.sub(cleanr, '', Tender_no)
            SegFields[13] = Tender_no.strip()


            SegFields[14] = "0" # news_check

            SegFields[16] = "1" # qc

            SegFields[17] = global_var.exe_no  # CA_exe_number

            # ==================================================================================================================
            # Tender Details

            Title = Decoded_get_htmlSource.partition("Descripción: </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Title = re.sub(cleanr, '', Title)
            Title = string.capwords(str(Title.strip()))
            if Title != "":
                SegFields[19] = Title  # short_descp

            Modality = Decoded_get_htmlSource.partition("Modalidad: </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Modality = re.sub(cleanr, '', Modality)
            Modality = string.capwords(str(Modality.strip()))
            

            Type_of_contest = Decoded_get_htmlSource.partition("Tipo de concurso: </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Type_of_contest = re.sub(cleanr, '', Type_of_contest)
            Type_of_contest = string.capwords(str(Type_of_contest.strip()))
        
            # Receiving_Offers = Decoded_get_htmlSource.partition("Tipo de recepción de ofertas: </div>")[2].partition("</div>")[0]
            # cleanr = re.compile('<.*?>')
            # Receiving_Offers = re.sub(cleanr, '', Receiving_Offers).strip()
            # Receiving_Offers = string.capwords(str(Receiving_Offers.strip()))

            Process_Type = Decoded_get_htmlSource.partition("Tipo Proceso: </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Process_Type = re.sub(cleanr, '', Process_Type)
            Process_Type = string.capwords(str(Process_Type.strip()))

            # Compliance_Bond_percentage = Decoded_get_htmlSource.partition("Porcentaje de Fianza de cumplimiento:  </div>")[2].partition("</div>")[0]
            # cleanr = re.compile('<.*?>')
            # Compliance_Bond_percentage = re.sub(cleanr, '', Compliance_Bond_percentage)

            # Percentage_of_support_bond = Decoded_get_htmlSource.partition("Porcentaje de Fianza de sostenimiento:  </div>")[2].partition("</div>")[0]
            # cleanr = re.compile('<.*?>')
            # Percentage_of_support_bond = re.sub(cleanr, '', Percentage_of_support_bond).strip()

            Status = Decoded_get_htmlSource.partition("> Estatus: </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Status = re.sub(cleanr, '', Status).strip()
            Status = string.capwords(str(Status.strip()))

            Collected_Tender_Details = str(Title) + "<br>\n" + "Modalidad: " + str(Modality) + "<br>\n" + "Tipo de concurso: " + str(Type_of_contest) + "<br>\n" + "Tipo Proceso: " + str(Process_Type) + "<br>\n" + "Estatus: " + str(Status)
            SegFields[18] = Collected_Tender_Details # award_details

            # ==================================================================================================================
            # contract_date

            Bid_submission_date = Decoded_get_htmlSource.partition("Fecha de publicación: </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Bid_submission_date = re.sub(cleanr, '', Bid_submission_date)
            Bid_submission_date = Bid_submission_date.partition("Hora:")[0].strip().replace(' ', '')
            Month = Bid_submission_date.partition(".")[2].partition(".")[0].strip().lower()

            if Month == "enero":
                Bid_submission_date = Bid_submission_date.replace('.enero.', '.January.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "febrero":
                Bid_submission_date = Bid_submission_date.replace('.febrero.', '.February.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "marzo":
                Bid_submission_date = Bid_submission_date.replace('.marzo.', '.March.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "abril":
                Bid_submission_date = Bid_submission_date.replace('.abril.', '.April.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "mayo":
                Bid_submission_date = Bid_submission_date.replace('.mayo.', '.May.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "junio":
                Bid_submission_date = Bid_submission_date.replace('.junio.', '.June.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "julio" :
                Bid_submission_date = Bid_submission_date.replace('.julio.', '.July.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "agosto":
                Bid_submission_date = Bid_submission_date.replace('.agosto.', '.August.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "septiembre" :
                Bid_submission_date = Bid_submission_date.replace('.septiembre.', '.September.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "octubre":
                Bid_submission_date = Bid_submission_date.replace('.octubre.', '.October.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "noviembre":
                Bid_submission_date = Bid_submission_date.replace('.noviembre.', '.November.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            elif Month == "diciembre":
                Bid_submission_date = Bid_submission_date.replace('.diciembre.', '.December.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFields[24] = mydate

            SegFields[20] = '0'
            if contact_amount != '':
                SegFields[21] = contact_amount  # contract_value
                SegFields[22] = "GTQ" # contract_currency


            SegFields[28] = "https://www.guatecompras.gt/concursos/consultaConcurso.aspx?nog="+str(SegFields[13]).strip()  # tender_doc_file_col2

            # Source Name
            SegFields[31] = global_var.source  # source_col1

            for SegIndex in range(len(SegFields)):
                print(SegIndex, end=' ')
                print(SegFields[SegIndex])
                SegFields[SegIndex] = html.unescape(str(SegFields[SegIndex]))
                SegFields[SegIndex] = str(SegFields[SegIndex]).replace("'", "''")

            if len(SegFields[19]) >= 200:
                SegFields[19] = str(SegFields[19])[:200]+'...'

            if len(SegFields[18]) >= 1500:
                SegFields[18] = str(SegFields[18])[:1500]+'...'
                
            insert_in_Local(get_htmlsource_text , SegFields)
            a = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            a = True

