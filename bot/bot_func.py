from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import os
from time import sleep
from loguru import logger


dir = os.path.join(os.path.dirname(__file__), 'downloads')
if not os.path.exists(dir):
    os.makedirs(dir)

class BotsFunctions():

        def by_region(driver, wait, country):
                logger.info("Interagindo com o campo de busca por região")
                body_element = driver.find_element(By.TAG_NAME, 'body')
                body_element.click()

                country_selector_trigger = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".hierarchy-select.ng-pristine.ng-valid")))
                country_selector_trigger.click()

                element = wait.until(EC.visibility_of_element_located((By.ID, 'input-8')))

                wait.until(EC.element_to_be_clickable((By.ID, 'input-8')))

                element.clear()
                sleep(3)
                element.send_keys(country)

                country_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{country}')]")))
                country_option.click()

                logger.success("Busca por região foi concluida!")

                sleep(10)


        def filter_date(driver, wait, period):
                logger.info("Interagindo com o filtro de data")
                custom_selector = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'custom-date-picker')))

                custom_selector.click()

                option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//md-option/div[contains(text(), '{period}')]")))
                option.click()

                driver.implicitly_wait(10)

                sleep(10)


        def filter_date_person(driver, initial_date, end_date, wait):
                logger.info('Interagindo com campos de data personalizada')
                custom_selector = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'custom-date-picker')))
                if custom_selector:
                        logger.success('Botão capturado com sucesso')
                        custom_selector.click()
                else:
                        logger.error('Botão não encontrado')
                        return ''

                sleep(10)

                custom_data_selector = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select_option_22"]')))
                if custom_data_selector:
                        logger.success('Botão capturado com sucesso')
                        custom_data_selector.click()
                else: 
                        logger.error('Botão não encontrado')

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


        def click_button_multi_timeline(wait):
                logger.info("Iniciando interação com Interesse ao Longo do tempo")
                export_button = wait.until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]'))
                )
                if export_button:
                        logger.success("Botão capturado com sucesso")
                        export_button.click()
                        sleep(2)

                        wait.until(
                                lambda x: len(os.listdir(dir)) > 0
                        )

                else: 
                        print("Botão não encontrado")
                        return ''
                        
                sleep(20)
                

        def click_button_geo_map(wait):
                logger.info("Iniciando interação com Sub-Região")
                export_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')))
                if export_button:
                        logger.success('Botao para download capturado')
                        export_button.click()
                        sleep(2)

                        wait.until(
                        lambda x: len(os.listdir(dir)) > 0
                        )
                else: 
                        logger.error('Botão não encontrado')
                        return ''
                
                sleep(20)


        def scroll(driver):
                logger.info("Rolando a tela para baixo")
                sleep(2)
                scroll_amount = 1000
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                logger.info("A rolagem de tela foi concluida!")

                sleep(10)

        
        def click_button_related_entities(wait):
                logger.info("Clicando no botão para baixar csv de Assuntos Relacionados")
                export_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[3]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')))
                if export_button: 
                        logger.success('Botao para download capturado')
                        export_button.click()
                else: 
                        logger.error('Botão não encontrado')
                        return ''
        
                sleep(10)


        def click_button_related_queries(wait):
                logger.info("Clicando no botão para baixar csv de Pesquisas Relacionadas")
                export_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')))
                if export_button:
                        logger.success("Botão para download encontrado")
                        export_button.click()
                else:
                        logger.error("Botão não encontrado")
                        return ''

                sleep(10)