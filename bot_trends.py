from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from datetime import datetime
import re
import os
import uuid
import csv
from loguru import logger

from models.graph_models import Graphic
from models.geo_map_models import GeoMap
from models.related_entities_models import RelatedEntitiesTop, RelatedEntitiesRising
from models.related_queries_models import RelatedQueriesTop, RelatedQueriesRising
from database.conn import session

dir = '/home/ivan/Projects/Charisma/google-trends/files/'

def bot_graphic(param, country: None, period: None, initial_date: None, end_date: None) -> None:
    logger.info("Iniciando bot")

    try:
        chrome_options = Options()

        file_path_multi_time_line = os.path.join(dir, 'multiTimeline.csv')
        file_path_geo_map = os.path.join(dir, 'geoMap.csv')
        file_path_related_entities = os.path.join(dir, f'relatedEntities.csv')
        file_path_related_queries = os.path.join(dir, f'relatedQueries.csv')

        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False
        })

        try: 
            chrome_options.add_argument("--start-maximized")
            driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
            link = 'https://trends.google.com.br/trends/'
            driver.get(link)

            logger.success("O site do Google Trends foi aberto com sucesso!")
        
        except Exception as e:
            logger.error(f"Não foi possível abrir o Google Trends: {e}")

        sleep(3)

        if os.path.exists(file_path_multi_time_line):
            os.remove(file_path_multi_time_line)

        if os.path.exists(file_path_geo_map):
            os.remove(file_path_geo_map)

        if os.path.exists(file_path_related_entities):
            os.remove(file_path_related_entities)

        if os.path.exists(file_path_related_queries):
            os.remove(file_path_related_queries)

        try: 
            wait = WebDriverWait(driver, 20)
            input_element = wait.until(EC.element_to_be_clickable((By.ID, 'i7')))
            input_element.clear()
            input_element.send_keys(param)

            sleep(10)

            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.UywwFc-LgbsSe')))
            button.click()

            sleep(20)

            logger.success("Login realizado com sucesso no Google Trends!")
        
        except Exception as e: 
            logger.error(f"Não foi possível fazer o login no Google Trends: {e}")

        if country:
            try:
                logger.info("Interagindo com o campo de busca por região")
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

                logger.success("Busca por região foi concluida!")
            except Exception as e:
                logger.error(f"Erro ao interagir com o campo de autocompletar para países: {e}")

        sleep(10)
        
        if period:
            try:
                logger.info("Interagindo com o filtro de data")

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
                logger.error(f"Erro ao interagir com o filtro de data: {e}")
        
        sleep(20)

        try:

            wait = WebDriverWait(driver, 60)
            export_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.widget-actions-item.export'))
            )
            export_button.click()

            WebDriverWait(driver, 60).until(
                lambda x: len(os.listdir(dir)) > 0
            )
        except Exception as e:
            logger.error(f"Erro ao interagir com o botão do filtro de data: {e}")

        sleep(20)

        try:
            logger.info("Iniciando processo de scrapping do Interesse ao Longo do Tempo")
            with open(file_path_multi_time_line, "r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)
                
                for _ in range(6): 
                    next(csv_reader)

                for row in csv_reader:
                    tempo = row[0]

                    try:
                        logger.info("Tratando dados")
                        match = re.search(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2})?(?:[-+]\d{2}:\d{2})?', tempo)

                        if match:
                            tempo_formatado = match.group(0)

                            data_hora = datetime.strptime(tempo_formatado, '%Y-%m-%dT%H:%M:%S%z') if 'T' in tempo_formatado else datetime.strptime(tempo_formatado, '%Y-%m-%d')

                            data = data_hora.strftime('%Y-%m-%d')
                            hora = data_hora.strftime('%H:%M:%S')

                            valor_str = row[1].replace("<", "").strip()

                            numeros = re.findall(r'\d+', valor_str)

                            valor = int(numeros[0]) if numeros else None

                            print(f"Parâmetro de pesquisa: {param}")
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
                                logger.success("Salvando no banco de dados Interesse ao Longo do Tempo")
                                with session.begin_nested():
                                    existing_record = session.query(Graphic).filter_by(
                                        name=param,
                                        date=data,
                                        hour=hora,
                                        value=str(valor)
                                    ).one_or_none()

                                if existing_record:
                                    existing_record.value = str(valor)
                                    existing_record.date = data 
                                    existing_record.hour = hora
                                else:
                                    session.merge(data_graphic_trends)

                                session.commit()
                            except Exception as e:
                                session.rollback()
                                logger.error(f"Erro ao inserir/atualizar registro: {str(e)}")

                    except Exception as e:
                        logger.error(f"Erro ao tratar dados: {str(e)}")            

                logger.success("Dados processados com sucesso.")
        except Exception as e:
            print(f"Erro ao processar e salvar dados no banco de dados: {e}")

        sleep(10)

        try:
            logger.info("Iniciando interação com Sub-Região")
            container_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.fe-geo-chart-generated.fe-atoms-generic-container')))
            export_button = container_div.find_element(By.CSS_SELECTOR, 'button.widget-actions-item.export')
            export_button.click()
            WebDriverWait(driver, 60).until(
                lambda x: len(os.listdir(dir)) > 0
            )
            logger.success("Interação com Sub-Região concluida!")
        except Exception as e:
            pass
        
        sleep(20)

        try:
            logger.info("Iniciando processo de scrapping do Sub-Região")
            with open(file_path_geo_map, "r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)

                for _ in range(2): 
                    next(csv_reader)

                for row in csv_reader:
                    region = row[0]
                    valor_str = row[1].replace("<", "").strip()
                    numeros = re.findall(r'\d+', valor_str)

                    value_region = int(numeros[0]) if numeros else None

                    if re.search(r'\(\d{2}/\d{2}/\d{4}, \d{2}:\d{2} – \d{2}/\d{2}/\d{4}, \d{2}:\d{2}\)', row[1]):
                        data_hora_str = re.search(r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) – (\d{2}/\d{2}/\d{4}, \d{2}:\d{2})', row[1])
                        data_inicio = data_hora_str.group(1)
                        data_fim = data_hora_str.group(2)
                    
                    print(f"Região: {region}, valor: {value_region}")
                    print(f"Data Inicial: {data_inicio}, Data Final: {data_fim}")

                    new_uuid = uuid.uuid4()

                    geo_map_trends = GeoMap(
                            uuid = new_uuid,
                            param=param,
                            initial_date=data_inicio,
                            end_date=data_fim,
                            region=region,
                            value=str(value_region)
                        )          
                    
                    try:
                        logger.info("Salvando no banco de dados Sub-Região")
                        with session.begin_nested():
                            existing_record = session.query(GeoMap).filter_by(
                                param=param,
                                initial_date=data_inicio,
                                end_date=data_fim,
                                region=region,
                                value=str(value_region)
                            ).one_or_none()

                        if existing_record:
                            existing_record.initial_date = data_inicio
                            existing_record.end_date = data_fim
                            existing_record.region = region 
                            existing_record.value = str(value_region)
                        else:
                            session.merge(geo_map_trends)

                        session.commit()
                    except Exception as e:
                        session.rollback()
                        logger.error(f"Erro ao inserir/atualizar registro de Sub-Região: {str(e)}")

        except Exception as e: 
            logger.error(f"Erro ao fazer scrapping de Sub-Região: {e}")

        sleep(10)

        try: 
            logger.info("Rolando a tela para baixo")
            sleep(2)
            scroll_amount = 1000
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            logger.info("A rolagem de tela foi concluida!")
        
        except Exception as e: 
            logger.error(f"Erro ao rolar para baixo: {e}")

        sleep(10)

        try: 
            logger.info("Clicando no botão para baixar csv de Assuntos Relacionados")
            export_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[3]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')))
            export_button.click()
            logger.success("Download de csv Assuntos Relacionados foi concluído!")
        except Exception as e: 
            logger.error(f"Erro ao clicar no botão para baixar o csv de Assuntos Relacionados: {e}")

        sleep(10)

        try: 
            logger.info("Iniciando processo de scrapping de Assuntos Relacionados TOP")
            with open(file_path_related_entities, "r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)

                for _ in range(4):
                    next(csv_reader)

                for row in csv_reader:
                    entities = row[0]
                    value_str = row[1].replace("<", "").strip()
                    numeros = re.findall(r'\d+', value_str)

                    value_related_entities = int(numeros[0]) if numeros else None

                    new_uuid = uuid.uuid4()

                    related_entities = RelatedEntitiesTop(
                            uuid = new_uuid,
                            param=param,
                            region=country,
                            initial_date=data_inicio,
                            end_date=data_fim,
                            entities=entities,
                            value=str(value_related_entities)
                        )          
                    
                    try:
                        logger.info("Salvando no banco de dados Assuntos Relacionados TOP")
                        with session.begin_nested():
                            existing_record = session.query(RelatedEntitiesTop).filter_by(
                                param=param,
                                region=country,
                                initial_date=data_inicio,
                                end_date=data_fim,
                                entities=entities,
                                value=str(value_related_entities)
                            ).one_or_none()

                        if existing_record:
                            existing_record.region = country 
                            existing_record.initial_date = data_inicio
                            existing_record.end_date = data_fim
                            existing_record.entities = entities
                            existing_record.value = value_related_entities
                        else:
                            session.merge(related_entities)

                        session.commit()
                    except Exception as e:
                        session.rollback()
                        logger.error(f"Erro ao inserir/atualizar registro na tabela de Assuntos Relacionados Top {str(e)}")
        except Exception as e:
            logger.error(f"Erro ao fazer scrapping das Assuntos Relacionados RISING: {e}")
            
        finally: 
            pass

        try: 
            logger.info("Iniciando processo de scrapping de Assuntos Relacionados RISING")
            rising_data = []
            with open(file_path_related_entities, "r", encoding="utf-8") as file:
                current_section = None
                for line in file:
                    line = line.strip()
                    
                    if line == "RISING":
                        current_section = rising_data
                    elif current_section is not None and line:
                        parts = line.split(",")
                        if len(parts) == 2:
                            entity, value = [part.strip() for part in parts]
                            current_section.append((entity, value))

            for entity, value in rising_data:
                print(f"Entidade: {entity}")
                print(f"Valor: {value}")
                print()

            
                new_uuid = uuid.uuid4()

                related_entities_rising = RelatedEntitiesRising(
                        uuid = new_uuid,
                        param=param,
                        region=country,
                        initial_date=data_inicio,
                        end_date=data_fim,
                        entities=entity,
                        value=str(value)
                    )          
                
                try:
                    logger.info("Salvando no banco de dados Assuntos Relacionados RISING")
                    with session.begin_nested():
                        existing_record = session.query(RelatedEntitiesRising).filter_by(
                            param=param,
                            region=country,
                            initial_date=data_inicio,
                            end_date=data_fim,
                            entities=entity,
                            value=str(value)
                        ).one_or_none()

                    if existing_record:
                        existing_record.region = country 
                        existing_record.initial_date = data_inicio
                        existing_record.end_date = data_fim
                        existing_record.entities = entity
                        existing_record.value = str(value)
                    else:
                        session.merge(related_entities_rising)

                    session.commit()
                except Exception as e:
                    session.rollback()
                    logger.error(f"Erro ao inserir/atualizar registro Assuntos Relacionados RISING: {str(e)}")

        except Exception as e:
            logger.error(f"Erro ao fazer scrapping das Assuntos Relacionados RISING: {e}")

        sleep(10)

        try: 
            logger.info("Clicando no botão para baixar csv de Pesquisas Relacionadas")
            export_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')))
            export_button.click()
            logger.success("Download de csv Pesquisas Relacionadas foi concluído!")
        except Exception as e: 
            logger.error(f"Erro ao clicar no botão para baixar csv de Pesquisas Relacionadas: {e}")

        sleep(10)

        try: 
            logger.info("Iniciando processo de scrapping de Pesquisas Relacionados TOP")
            with open(file_path_related_queries, "r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)

                for _ in range(4):
                    next(csv_reader)

                for row in csv_reader:
                    entities = row[0]
                    value_str = row[1].replace("<", "").strip()
                    numeros = re.findall(r'\d+', value_str)

                    value_related_queries = int(numeros[0]) if numeros else None

                    new_uuid = uuid.uuid4()

                    related_queries = RelatedQueriesTop(
                            uuid = new_uuid,
                            param=param,
                            region=country,
                            initial_date=data_inicio,
                            end_date=data_fim,
                            queries=entities,
                            value=str(value_related_entities)
                        )          
                    
                    try:
                        logger.info("Salvando no banco de dados Pesquisas Relacionadas TOP")
                        with session.begin_nested():
                            existing_record = session.query(RelatedQueriesTop).filter_by(
                                param=param,
                                region=country,
                                initial_date=data_inicio,
                                end_date=data_fim,
                                queries=entities,
                                value=str(value_related_queries)
                            ).one_or_none()

                        if existing_record:
                            existing_record.region = country
                            existing_record.initial_date = data_inicio
                            existing_record.end_date = data_fim
                            existing_record.queries = entities
                            existing_record.value = str(value_related_queries)
                        else:
                            session.merge(related_queries)

                        session.commit()
                    except Exception as e:
                        session.rollback()
                        logger.error(f"Erro ao inserir/atualizar registro na tabela de Pesquisas Relacionadas Top {str(e)}")
        except Exception as e:
            logger.error(f"Erro ao fazer scrapping das Pesquisas Relacionadas RISING: {e}")
            
        finally: 
            pass

        try: 
            logger.info("Iniciando processo de scrapping de Pesquisas Relacionadas RISING")
            rising_data = []
            with open(file_path_related_queries, "r", encoding="utf-8") as file:
                current_section = None
                for line in file:
                    line = line.strip()
                    
                    if line == "RISING":
                        current_section = rising_data
                    elif current_section is not None and line:
                        parts = line.split(",")
                        if len(parts) == 2:
                            entity, value = [part.strip() for part in parts]
                            current_section.append((entity, value))

            for entity, value in rising_data:
                print(f"Entidade: {entity}")
                print(f"Valor: {value}")
                print()

            
                new_uuid = uuid.uuid4()

                related_queries_rising = RelatedQueriesRising(
                        uuid = new_uuid,
                        param=param,
                        region=country,
                        initial_date=data_inicio,
                        end_date=data_fim,
                        queries=entity,
                        value=str(value)
                    )          
                
                try:
                    logger.info("Tentando inserir/atualizar registro Pesquisas Relacionadas RISING")
                    
                    # Iniciar uma nova transação para a consulta de pesquisa
                    with session.begin_nested():
                        existing_record = session.query(RelatedQueriesRising).filter_by(
                            uuid=new_uuid,
                            param=param,
                            region=country,
                            initial_date=data_inicio,
                            end_date=data_fim,
                            queries=entity,
                            value=str(value)
                        ).one_or_none()

                    if existing_record:
                        existing_record.region = country
                        existing_record.initial_date = data_inicio
                        existing_record.end_date = data_fim
                        existing_record.queries = entity
                        existing_record.value = str(value)
                    else:
                        session.merge(related_queries_rising)

                    session.commit()
                except Exception as e:
                    session.rollback()
                    logger.error(f"Erro ao inserir/atualizar registro Pesquisas Relacionadas RISING: {str(e)}")
        except Exception as e:
            logger.error(f"Erro ao fazer scrapping das Pesquisas Relacionadas RISING: {e}")

    finally:
        driver.quit()
    


        