import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
import re
import uuid
import csv
from models.graph_models import Graphic
from selenium.webdriver.common.keys import Keys
from database.conn import session

dir = '/home/ivan/Projects/Charisma/google-trends/files/'

def bot_graphic(param, country: None, period: None, initial_date: None, end_date: None) -> None:
    try:
        chrome_options = Options()
        file_path = os.path.join(dir, 'multiTimeline.csv')

        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False
        })

        chrome_options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

        link = 'https://trends.google.com.br/trends/'

        driver.get(link)

        sleep(3)

        if os.path.exists(file_path):
            os.remove(file_path)

        wait = WebDriverWait(driver, 20)
        input_element = wait.until(EC.element_to_be_clickable((By.ID, 'i7')))
        input_element.clear()
        input_element.send_keys(param)
        sleep(10)
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
        
        sleep(20)

        wait = WebDriverWait(driver, 60)
        export_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.widget-actions-item.export'))
        )
        export_button.click()

        WebDriverWait(driver, 60).until(
            lambda x: len(os.listdir(dir)) > 0
        )

        sleep(20)

        try:
            with open(file_path, "r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)
                
                for _ in range(6): 
                    next(csv_reader)

                for row in csv_reader:
                    tempo = row[0]

                    try:
                        match = re.search(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2})?(?:[-+]\d{2}:\d{2})?', tempo)

                        if match:
                            tempo_formatado = match.group(0)

                            data_hora = datetime.strptime(tempo_formatado, '%Y-%m-%dT%H:%M:%S%z') if 'T' in tempo_formatado else datetime.strptime(tempo_formatado, '%Y-%m-%d')

                            data = data_hora.strftime('%Y-%m-%d')
                            hora = data_hora.strftime('%H:%M:%S')

                            valor_str = row[1].replace("<", "").strip()

                            numeros = re.findall(r'\d+', valor_str)

                            valor = int(numeros[0]) if numeros else None

                            print(f"Data: {data}, Hora: {hora}, Valor: {valor}")

                            new_uuid = uuid.uuid4()

                            data_graphic_trends = Graphic(
                                    uuid = new_uuid,
                                    name=param,
                                    date=data,
                                    hour=hora,
                                    value=str(valor)
                                )          
                            
                            try:
                                existing_record = session.query(Graphic).filter_by(
                                    name=param,
                                    date=data,
                                    hour=hora,
                                    value=str(valor)
                                ).one_or_none()

                                if existing_record:
                                    existing_record.uuid = new_uuid
                                else:
                                    session.add(data_graphic_trends)

                                session.commit()
                            except Exception as e:
                                session.rollback()
                                print(f"Erro ao inserir/atualizar registro: {str(e)}")

                    except Exception as e:
                        print(f"Erro ao processar linha: {e}")

                print("Dados processados com sucesso.")
        except Exception as e:
            print(f"Erro ao processar e salvar dados no banco de dados: {e}")
    finally:
        driver.quit()
    


        