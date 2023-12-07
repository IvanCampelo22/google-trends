from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import re 
from models.graph_models import Graphic
from database.conn import session

def bot_graphic(param, country: None, period: None, initial_date: None, end_date: None) -> None:
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
                body_element = driver.find_element(By.TAG_NAME, 'body')
                body_element.click()
                sleep(2)

                country_selector_trigger = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".hierarchy-select.ng-pristine.ng-valid")))
                country_selector_trigger.click()
                sleep(2)

                element = wait.until(EC.visibility_of_element_located((By.ID, 'input-8')))

                wait.until(EC.element_to_be_clickable((By.ID, 'input-8')))

                element.clear()
                sleep(3)
                element.send_keys(country)
                sleep(3)

                country_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{country}')]")))
                country_option.click()
            except Exception as e:
                print(f"Erro ao interagir com o campo de autocompletar para países: {e}")

        sleep(10)
        
        if period:
            try:
                custom_selector = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'custom-date-picker')))

                custom_selector.click()

                option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//md-option/div[contains(text(), '{period}')]")))
                option.click()

                driver.implicitly_wait(10)

                sleep(10)

                data_inicio_element = driver.find_element(By.CSS_SELECTOR, "div.custom-date-picker-dialog-range-from input")
                data_fim_element = driver.find_element(By.CSS_SELECTOR, "div.custom-date-picker-dialog-range-to input")

                data_inicio_element.clear()
                data_inicio_element.send_keys(initial_date)  
                data_inicio_element.send_keys(Keys.RETURN) 

                sleep(5)

                data_fim_element.clear()
                data_fim_element.send_keys(end_date)  
                data_fim_element.send_keys(Keys.RETURN) 

                sleep(5)

                javascript_code = "document.querySelector('button[aria-label=\"OK\"]').click();"
                driver.execute_script(javascript_code)
                sleep(5)

                driver.implicitly_wait(10)

                sleep(10)

            except Exception as e:
                print(f"Erro ao interagir com o date picker: {e}")
        
        sleep(10)


        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table_div = soup.find('div', {'aria-label': 'A tabular representation of the data in the chart.'})
        if table_div:
            table = table_div.find('table')
            rows = table.find_all('tr')

            datas = []
            valores = []
            datas_limpa = []


            for row in rows[1:]:
                cols = row.find_all('td')
                data = cols[0].text.strip()
                datas.append(data)
                valor = cols[1].text.strip()
                valores.append(valor)
                for i in datas:
                    date = i.split(" às ")
                    if period == 'Na última hora' or period == 'Nas últimas 4 horas' or period == 'Ontem' or period == 'Últimos 7 dias':
                        just_date, just_hour = date[0], date[1]
                    else: 
                        just_hour = None
                    month = {"jan": "01", "fev": "02", "mar": "03", "abr": "04", "mai": "05", "jun": "06", "jul": "07", "ago": "08", "set": "09", "out": "10", "nov": "11", "dez": "12"}
                    mon = re.findall(r'\b(\w{3})\b', data)[0].lower()
                    mon_number = month[mon]
                    dia = re.findall(r'\d+', data)[0]
                    formated_date = f"{dia}-{mon_number}"

                    print("Data:", formated_date)
                    print("Hora:", just_hour)            

                    
                    data_graphic_trends = Graphic(
                        name = param,
                        date = formated_date,
                        hour = just_hour,
                        value = valor
                    )   

                    session.add(data_graphic_trends)
                    session.commit()


    except TimeoutException:
        print("Elemento não encontrado a tempo")
        driver.close()

