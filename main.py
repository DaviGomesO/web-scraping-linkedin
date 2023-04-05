from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import re
import datetime
import pandas as pd

# para separar a string quando encontrar o primeiro digito
padrao = r"(\d)"  # significa um digito

### Função de Scrolling na pagina
## Não está funcionando
'''# Realizar o scrolling até o fim da página
def Scrolling():
    contador = 0
    altura_anterior = driver.execute_script("return window.pageYOffset;")
    while contador < 2:
        # Realizar o scrolling até o fim da página
        actions = ActionChains(driver)
        actions.send_keys(Keys.END).perform()
        sleep(2)  # Aguardar um tempo para carregar mais vagas
    
        # Verificar se não há mais vagas para carregar (chegou ao fim da página)
        try:
            even_ver_mais = driver.find_elements(by=By.XPATH, value='//*[@id="main-content"]/section[2]/button')[0]
            #even_ver_mais.click()
            driver.execute_script("arguments[0].click();", even_ver_mais)
            # Verificar se a altura da página foi alterada
            altura_atual = driver.execute_script("return window.pageYOffset;")
            if altura_atual == altura_anterior:
                # Incrementar o contador quando o botão não estiver mais disponível
                contador += 1
            else:
                # Zerar o contador quando a página for expandida
                contador = 0
            altura_anterior = altura_atual
        except NoSuchElementException:
             # Incrementar o contador quando o botão não estiver mais disponível
            contador += 1
            continue
'''

### Funções de Scraping para páginas
## Raspagem nos dados do tipo de contratação e nível de experiência
def rasp(tipo, nivel, candidaturas):
    vagas_nivel = driver.find_elements(by=By.XPATH,
                                       value='//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[1]/span')
    for i in vagas_nivel:
        nivel.append(i.text)

    vagas_tipo = driver.find_elements(by=By.XPATH,
                                      value='//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[2]/span')
    for i in vagas_tipo:
        tipo.append(i.text)

    try:
        vagas_candidaturas = driver.find_elements(by=By.XPATH,
                                                  value='//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/figure/figcaption')
        if vagas_candidaturas[0].text == "Seja um dos 25 primeiros a se candidatar":
            candidaturas.append("Menos de 25 candidaturas")
        else:
            candidaturas.append(vagas_candidaturas[0].text)
    except:
        vagas_candidaturas = driver.find_elements(by=By.XPATH,
                                                  value='//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[2]')
        candidaturas.append(vagas_candidaturas[0].text)


## Raspagem nos dados de seguidores da empresa, localidade, e quantidade de funcionarios
def rasp_info_emp(seguidores_emp, local_emp, qtd_funcionarios):
    # tratar erro de quando não encontrar informações de texto sobre seguidores no linkedin
    try:
        elements = driver.find_elements(by=By.XPATH,
                                        value='//*[@id="main-content"]/section[1]/section/div/div[2]/div[1]/h3')
        if len(elements) > 0:
            info_aux = re.split(padrao, elements[0].text, maxsplit=1)
            seguidores_emp.append(info_aux[1] + info_aux[2])
        else:
            seguidores_emp.append("Não informado")

    except NoSuchElementException:
        seguidores_emp.append("Não informado")

    element_loc = driver.find_elements(by=By.XPATH, value='//*[@id="address-0"]')
    local_emp.append(element_loc[0].text)

    element_funcionario = driver.find_elements(by=By.XPATH,
                                               value='//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd')
    qtd_funcionarios.append(element_funcionario[0].text)


# Configurar o driver do navegador (exemplo usando o Chrome)
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.google.com")

# Busca para o Linkedin
sleep(2)
driver.find_element('name', 'q').send_keys('vagas marketing')
driver.get("https://www.linkedin.com")

# Não logar, abrir logo a aba de vagas
sleep(3)
driver.find_elements(by=By.XPATH, value='/html/body/nav/ul/li[4]/a')[0].click()

# Aplicando filtros
driver.find_element('name', 'keywords').clear()
driver.find_element('name', 'keywords').send_keys('Marketing E Publicidade')
driver.find_element('name', 'location').clear()
driver.find_element('name', 'location').send_keys('Brasil')

sleep(2)
driver.find_elements(by=By.XPATH, value='//*[@id="location-1"]')[0].click()

sleep(2)
driver.find_elements(by=By.XPATH, value='//*[@id="jserp-filters"]/ul/li[4]/div/div/button')[0].click()

sleep(2)
driver.find_elements(by=By.XPATH, value='//*[@id="jserp-filters"]/ul/li[4]/div/div/div/div/div/div[1]/label')[0].click()

sleep(3)
driver.find_elements(by=By.XPATH, value='//*[@id="jserp-filters"]/ul/li[4]/div/div/div/button')[0].click()

# fecho evento de iniciar sessão
sleep(2)
try:
    evento_sessao = driver.find_elements(by=By.XPATH, value='/html/body/div[3]/button')[0]
    # Se o elemento estiver presente, clica nele para fechar o evento
    evento_sessao.click()
except:
    # Se o elemento não estiver presente, não faz nada
    pass

#Scrolling()

sleep(2)
# URL da vaga
vagas_links = driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/section[2]/ul/li/div/a')
vagas_links = [link.get_attribute('href') for link in vagas_links]

sleep(2)
# Nome da vaga
vagas_title = driver.find_elements(by=By.CLASS_NAME, value='base-search-card__title')
vagas_title = [titulo.text for titulo in vagas_title]

sleep(2)
# Nome da empresa contratante
vagas_empresa = driver.find_elements(by=By.CLASS_NAME, value='hidden-nested-link')
vagas_empresa = [empresa.text for empresa in vagas_empresa]

sleep(2)
# Tipo de contratação
# Nível de experiência
# Número de candidaturas
# URL da empresa contratante
# Número de seguidores da empresa
# Local sede da empresa
# Número de funcionários
# Horário de realização do Scraping
vagas_tipo, vagas_nivel, links_sites_emp, num_candidaturas = [], [], [], []
seguidores_empresa, local_empresa, qtd_func = [], [], []
horario_Scraping = []

j = 0
for i in vagas_links:
    agora = datetime.datetime.now()
    formatado = agora.strftime("%d/%m/%Y %H:%M")
    print(formatado)
    horario_Scraping.append(formatado)
    sleep(2)
    driver.get(i)

    # verificar se o url aberto foi o certo
    while driver.current_url != i:
        driver.get(i)
        # print(j,driver.current_url)

    rasp(vagas_nivel, vagas_tipo, num_candidaturas)

    site_empresa = driver.find_elements(by=By.XPATH,
                                        value='//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a')
    for k in site_empresa:
        # print(k.get_attribute('href'))
        links_sites_emp.append(k.get_attribute('href'))

    sleep(1)
    # Abrir site da empresa
    driver.get(links_sites_emp[j])

    # verificar se o url aberto foi o certo
    while driver.current_url != links_sites_emp[j]:
        driver.get(links_sites_emp[j])

    sleep(3)

    # fecho evento de logar se estiver presente
    try:
        evento_entrar = driver.find_elements(by=By.XPATH,
                                                 value='//*[@id="organization_guest_contextual-sign-in"]/div/section/button')[0]
        # Se o elemento estiver presente, clica nele para fechar o evento
        evento_entrar.click()
    except:
        # Se o elemento não estiver presente, não faz nada
        pass

    rasp_info_emp(seguidores_empresa, local_empresa, qtd_func)

    j = j + 1

# Modelo de contratação
###Só consigo ver o modelo de contratação de uma vaga se estiver logado na conta
# Data da postagem da vaga
###Só consigo ver a data de publicação de uma vaga se estiver logado na conta

# URL da candidatura
'''A URL da candidatura só consigo pegar se estiver logado, pois apenas direciona ao link aqueles que estiverem 
 cadastrados e logados'''

# Guardando informações no arquivo CSV
sleep(2)
col = ["URL da vaga no linkedin", "Nome da vaga",
                 "Nome da empresa contratante","URL da empresa contratante",
                "Tipo de contratação", "Nível de experiência", "Número de candidaturas para vaga",
                 "Horário do scraping", "Número de funcionários da empresa", "Número de seguidores da empresa",
                "Local sede da empresa"]
df = pd.DataFrame({"URL da vaga no linkedin":vagas_links, "Nome da vaga":vagas_title,
                 "Nome da empresa contratante":vagas_empresa,"URL da empresa contratante":links_sites_emp,
                "Tipo de contratação":vagas_tipo, "Nível de experiência":vagas_nivel, "Número de candidaturas para vaga":num_candidaturas,
                   "Horário do scraping": horario_Scraping, "Número de funcionários da empresa":qtd_func,
                   "Número de seguidores da empresa":seguidores_empresa,"Local sede da empresa":local_empresa})
df.head()
df.to_csv("Scraping (Outro)- Francisco Davi Gomes de Oliveira.csv", mode='w')

driver.quit()
