from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from time import sleep
import re 
from models.graph_models import Graphic
from database.conn import session

def bot_graphic(param, country: None) -> None:
    try:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Abre o Chrome em tela cheia

        driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))


        link = 'https://trends.google.com.br/trends/'

        driver.get(link)

        sleep(3)

        wait = WebDriverWait(driver, 20)
        input_element = wait.until(EC.element_to_be_clickable((By.ID, 'i7')))
        input_element.clear()
        input_element.send_keys(param)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.UywwFc-LgbsSe')))
        button.click()
        sleep(20)
        if country:
            try:
                # Garantindo que o campo de pesquisa perca o foco
                body_element = driver.find_element(By.TAG_NAME, 'body')
                body_element.click()
                sleep(2)

                # Acionando o seletor de países
                country_selector_trigger = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".hierarchy-select.ng-pristine.ng-valid")))
                country_selector_trigger.click()
                sleep(2)

                # Interagindo com o campo de autocompletar para países
                autocomplete_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "md-autocomplete")))
                autocomplete_input.clear()
                input_country = wait.until(EC.visibility_of_all_elements_located(By.ID, 'input-8'))
                input_country.send_keys(country)
                sleep(2)

                # Selecionando o país das sugestões
                country_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//md-autocomplete-wrap//span[contains(text(), '" + country + "')]")))
                country_option.click()
            except Exception as e:
                print(f"Erro ao interagir com o campo de autocompletar para países: {e}")

        # html = driver.page_source
        # soup = BeautifulSoup(html, 'html.parser')
        # table_div = soup.find('div', {'aria-label': 'A tabular representation of the data in the chart.'})
        # if table_div:
        #     table = table_div.find('table')
        #     rows = table.find_all('tr')

        #     datas = []
        #     valores = []
        #     datas_limpa = []


        #     for row in rows[1:]:  # Ignora o cabeçalho da tabela que contém os elementos <th>
        #         # Encontrando todas as células de cada linha
        #         cols = row.find_all('td')
        #         # A primeira célula (<td>) em cada linha contém a data
        #         data = cols[0].text.strip()
        #         datas.append(data)
        #         # A segunda célula (<td>) em cada linha contém o valor
        #         valor = cols[1].text.strip()
        #         valores.append(valor)
        #         for i in datas:
        #             date = i.split(" às ")
        #             just_date, just_hour = date[0], date[1] 
        #             month = {"jan": "01", "fev": "02", "mar": "03", "abr": "04", "mai": "05", "jun": "06", "jul": "07", "ago": "08", "set": "09", "out": "10", "nov": "11", "dez": "12"}
        #             mon = re.findall(r'\b(\w{3})\b', data)[0].lower()
        #             mon_number = month[mon]
        #             dia = re.findall(r'\d+', data)[0]
        #             formated_date = f"{dia}-{mon_number}"

        #             print("Data:", formated_date)  # Por exemplo, "27-11"
        #             print("Hora:", just_hour)            

                    
        #             data_graphic_trends = Graphic(
        #                 name = param,
        #                 date = formated_date,
        #                 hour = just_hour,
        #                 value = valor
        #             )   

        #             session.add(data_graphic_trends)
        #             session.commit()


    except TimeoutException:
        print("Elemento não encontrado a tempo")
        driver.close()

