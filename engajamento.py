import pip
import shutil
import sqlite3
from sqlite_utils import Database
import subprocess, time
from time import sleep
import numpy as np
from array import array 
import os
from selenium import webdriver 
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from random import randrange 

subprocess.run('downloadplaylist.py -e ', shell=True)  #Você pode optar em manter esta linha ou não, na minha opnião, você pode executar este arquivo separadamente, neste momento.
#Esta parte do Script, ainda não está concluida, mas é apenas para Layout, não interfere no Script de engajamento.
#cmd = "wmic path Win32_VideoController get CurrentVerticalResolution,CurrentHorizontalResolution"
#size_tuple = tuple(map(int,os.popen(cmd).read().split()[-2::]))
#Esta parte do Script, ainda não está concluida, mas é apenas para Layout, não interfere no Script de engajamento.

#Este é Class para deletar aquivos na pasta %tmp%
def handler(func, path, exc_info):
    print(exc_info)
#Este é Class para deletar aquivos na pasta %tmp%

clear = lambda: os.system('cls')  #Chama o CLS do CMD para limpar a tela, se você não estiver utilizando o Python sobre o CMD, pode ser que não seja necessario.

#Padrões do Selenium, valide a versão do Selenium e do Chrome.
#Link do Selenium: https://chromedriver.chromium.org/downloads verifique no Chrome, sobre ajuda e sobre, ali use a mesma versão para baixar o selenium chromedriver_win32.zip

chrome_options = webdriver.ChromeOptions() #Se você possui uma pasta padrão para o Selenium informe aqui ("caminho\file.exe"), se deixa na mesma pasta do Script, deixe em branco ()
chrome_options.add_argument("--mute-audio") #Deixa o Selenium em mudo
chrome_options.add_argument("-window-size=480,320") #Define o tamanho das janelas em 480x320
#chrome_options.add_argument("--start-maximized") #Caso não esteja utilizando a opção acima, ele abre maximizado.
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required"); #Ativa o autoplay do Youtube.
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

#Algumas maquinas apresentam erros que estão informados nos comentários, se aparecer, apenas descomente as linhas.
# chrome_options.add_argument("--disable-software-rasterizer"); #trata o erro ERROR:gpu_init.cc(426) Passthrough is not supported GL is disabled
# chrome_options.add_argument("--disable-gpu"); #trata o erro ERROR:gpu_init.cc(426) Passthrough is not supported GL is disabled
# chrome_options.add_argument("--disable-infobars") #ERROR:device_event_log_impl.cc(
# chrome_options.add_argument("--ignore-ssl-errors=yes") #ERROR:device_event_log_impl.cc(
# chrome_options.add_argument("--ignore-certificate-errors") #ERROR:device_event_log_impl.cc(

try:
    clear() #limpa a tela

    
    print("\n\n\n\t------------------------------------------------------------")
    print("\t- Aqui você informa quantos ambientes serão carregados")
    print("\t- Para um computador até 4GB")
    print("\t- Recomendo de 2 até 5 ambientes")
    print("\n\n\n\t------------------------------------------------------------")
    retorno = float(input("\n\tPor favor apenas numero:\n\t-> ")) #Nesta parte você informa quantas telas do navegador, deseja abrir
    retorno = int(retorno) 
    
    print("\n\n\n\t------------------------------------------------------------")
    print("\tInforme o tempo de atualização das visualizações:")
    atualiza = float(input("\tO Youtube recomenda 30 segundos:\n\t-> ")) #Nesta parte, quantos segundos cada tela irá rodar os vídeos.
    #if atualiza < 40: #para uma garantia de CPM e visualização, o proprio Youtube recomenda fortemente que rode o vídeo 30 segundos.
    #    atualiza = 40
    atualiza = int(atualiza)

except ValueError:
    print("\n\tPoxa, apenas numeros:") #só uma validação caso coloque outro tipo de caracteres.

# variaveis principais
urlinicial = "https://www.youtube.com/channel/UCdOA_1KzXHIp3gmVyyYv2sg"  #Informe o seu canal
playlist = "https://www.youtube.com/playlist?list=PL_bWKnK7ufEAzouYibMW-Uvo6BDR0HzOP" #Informe a sua playlist

media1 = 0 #É só uma variavel de contadores 
media2 = 0 #É só uma variavel de contadores
linha = 0 #É só uma variavel de contadores
contador = {} #Criando uma Array

video = {} #Criando uma Array
browser = {} #Criando uma Array
browser_list = [] #Criando uma Array

viewers = 0 #É só uma variavel de contadores 
prepararfechar = 0 #É só uma variavel de contadores 

#Neste momento ele vai carregar o DB alimentado pelo downloadplaylist.py
conn = sqlite3.connect('youtube.db') 
cursor = conn.cursor() #manipulando o DB
cursor.execute("SELECT aidvideo, aurlvideo, aviewers FROM VIEWERS ORDER BY aviewers Desc LIMIT " + str(retorno)) #selecionando os vídeos mais visualizados.
records = cursor.fetchall() #contador
clear() #Limpa a tela

print("\n\t------------------------------------") #imprime uma taleba com as informações dos mais visualizado, para você ter uma noção, pode usar o modulo panda se preferir
print("\t- ", int(retorno), " vídeos mais visualizados")
print("\n\t- Viewers \t | Link do vídeo")

for row in records: #Soma para fazer a média dos mais vistos
    print("\t- ", row[2], " \t | ", row[1])
    maior = row[2]
    media1 = media1 + row[2]
print("\tMédia Maxima: ", str(round(media1 / len(records)))) #Aqui é apenas para você ter a informação da média dos videos mais vistos.
conn.commit() #Fecha a manipulação

# Mesma rotina para leitura da tabela, só que vai retornar os menos vistos, esses serão os preferenciais para aumentar o engajamento.
cursor.execute("SELECT aidvideo, aurlvideo, aviewers, atitulo FROM VIEWERS ORDER BY aviewers Asc LIMIT " + str(retorno))
records = cursor.fetchall()
print("\n\t------------------------------------")
print("\t- ", int(retorno), " vídeos menos visualizados")
print("\n\t- Viewers \t | Link do vídeo")

for row in records: #Soma para fazer a média dos menos vistos
    print("\t- ", row[2], " \t | ", row[1])
    menor = row[2]
    media2 = media2 + menor

    #Agora vamos aplicar as informações dos vídeos menos vistas para alguns Array.
    video['id' + str(linha)] = row[0] 
    video['url' + str(linha)] = row[1]
    video['visualizacao' + str(linha)] = row[2]
    video['titulo' + str(linha)] = row[3]
    locals().update(video) #declarando a array
    linha = linha + 1 #apenas um contador.

    
conn.commit() 
conn.close() #Fecha o Banco

print("\tMédia Minima: ", str(round(media2 / int(retorno))))
print("\n\t------------------------------------")
print("\t", int(retorno), " janelas, serão recarregadas a cada ", int(atualiza), " segundos. Num total de ",
      str(round((((media1 / int(retorno)) / (media2 / int(retorno)))) / retorno)), " vezes.")
print("\t------------------------------------\n")

time.sleep(1) #você define um tempo para que o usuario possa ler as informações acima.
#os.system("pause") #Se preferir pode pausar, o OS está utilizando o pause via Windows, defina de acordo com seu sistema operacional.

#estas informações é apenas para Layout, não interfere na execução do Script
pontox = 0 #altura 1920
pontoy = 0 #larura 1080

for i in range(linha): #Chegou a hora para 
    contador['a' + str(i)] = 0  # Limpa a variavel para redefinir as contagens do navegador
    browser['a' + str(i)] = webdriver.Chrome(chrome_options=chrome_options) #Alimenta a variavel com as informações do chrome_options, lembrando que aqui é um loop, você pode criar chrome_options independentes
    #posicionando as telas
    #print('a' + str(i),' - ',pontox) # Lembrando que isso é apenas para Layout não afeta o engajamento, neste caso ele só está posicionando as telas para ser apresentada.
    if (pontox >= (size_tuple[0]/2)):
        pontox = 0
        pontoy = (size_tuple[1]/2)
    browser['a' + str(i)].set_window_position(pontox, pontoy)
    #browser['a' + str(i)].set_window_size(pontox,round(size_tuple[1]/2))
    #size(largura,altura)
    pontox = round(pontox + (size_tuple[0] / (retorno+1))) #informa o proximo ponto do Layout onde a tela será aberta
    
    
    locals().update(browser) #Atualizando as Array dos Browser
    browser_list.append(browser['a' + str(i)]) #Abrindo as janelas de acordo com o total de janelas que você escolheu
    print("\n\n\n\t--------------------------------------------")
    print("\t- Carregando os ambiente ", str(i), ", para os engajamentos dos videos")
    print("\t--------------------------------------------")
    video['carregamento' + str(i)] = 20# round(((media1/int(retorno))/(media2/int(retorno)))/retorno) #Aqui informa quantas vezes o vídeo irá rodar, 
    locals().update(video) #Atualizando as Array dos vídeos


    
for browsera in browser_list:
    browsera.get(urlinicial)  #Cada Browser carregado, vai incluir seu canal, fazendo o YT subir seu rank nas consultas
    
a=0 #Contador para diminuir tempo de espera após carregar todos os broswers
while (True):
    try:
        clear() #Limpa a tela
        x = randrange(0, len(browser_list))  # Escolhe o ambiente randomicamente para recarregar com o vídeo disposto
        if int(contador['a' + str(x)]) <= int(video['carregamento' + str(x)]): #Enquanto não atinge o minimo estabelecido da contagem, ele continua abrindo os videos
            conn = sqlite3.connect('youtube.db') #Abre o SQL para atualizar o contador
            cursor = conn.cursor()
            browser_list[x - 1]
            print("\n\n\n\t--------------------------------------------") #textos para referencias
            print("\t- Atualizando, o ambiente", x + 1)
            print("\t- Engajando o vídeo: ")
            print("\t- ", video['titulo' + str(x)])
            print("\t- Falta ", int(video['carregamento' + str(x)]) - int(contador['a' + str(x)]), " rotinas")
            if int(viewers) > 0: 
                print("\t- Total de viewers deste bot = ", viewers)
            print("\t--------------------------------------------")
            if a != 0: #Aguarda o tempo que você estabeleceu, em contagem regressiva, para recarregar a pagina novamente
                for i in range(atualiza, -1, -1):
                    print(f"\b\b\b\t{i}", end="", flush=True)
                    time.sleep(1)
            a = 1 #realinha o contador de tempo para funcionar o temporizador para a sequencia de videos
            try: 
                browser['a' + str(x)].get(video['url' + str(x)]) #carrega o vídeo da Array no Browser determinando para ela
            except:
                browser['a' + str(x)].close
                if(browser['a' + str(x)].close): #Se algum erro acontecer, e fechar, ele reabre a mesma janela com o vídeo pendente.
                    try:
                        browser['a' + str(x)].get(video['url' + str(x)]) 
                    except:
                        pass
                pass
#1 Anuncio na abertura do vídeo ytp-ad-button ytp-flyout-cta-action-button
            try:     
                print(browser['a' + str(x)].execute_script("return document.readyState"))
                print(len(browser['a' + str(x)].find_elements(By.XPATH, '//button[@class="ytp-ad-button ytp-flyout-cta-action-button"]')))
                if(len(browser['a' + str(x)].find_elements(By.XPATH, '//button[@class="ytp-ad-button ytp-flyout-cta-action-button"]'))) > 0: 
                    wait = WebDriverWait(browser['a' + str(x)], 6)
                #if (x%2) == 0:
                    browser['a' + str(x)].maximize_window() #maximiza a tela para carregar anuncio
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-ad-button ytp-flyout-cta-action-button"]'))).click() 
                    browser['a' + str(x)].switch_to.window(browser['a' + str(x)].window_handles[1]) #Abre a aba 2
                    print(browser['a' + str(x)].execute_script("return document.readyState"))
                    time.sleep(1)    
                    browser['a' + str(x)].close() #fecha a aba 2
                    browser['a' + str(x)].switch_to.window(browser['a' + str(x)].window_handles[0]) #clica na aba 1
                    print(len(browser['a' + str(x)].find_elements(By.XPATH, '//button[@class="ytp-play-button ytp-button"]')))
                    if(len(browser['a' + str(x)].find_elements(By.XPATH, '//button[@class="ytp-play-button ytp-button"]'))) > 0: 
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-play-button ytp-button"]'))).click() 
                    time.sleep(1)
                else: 
                    time.sleep(1) 
                browser['a' + str(x)].set_window_size(480, 320) #volta para o tamanho original
            except: 
                pass
#1 Anuncio na abertura do vídeo ytp-ad-button ytp-flyout-cta-action-button
  
#2 Anuncio overlay ad ytp-ad-overlay-container
               
#deletando arquivos temporarios  
            dirPath = "%tmp%";
            dirPath = os.environ['TEMP'] 
            try:
               shutil.rmtree( dirPath, ignore_errors = True )
            except:
               print('Não deletou, mas tá de boas')
#Concluido deletando arquivos temporarios
            video['visualizacao' + str(x)] = video['visualizacao' + str(x)] + 1 #carrega o vídeo para a array correta
            somavisualizacao = video['visualizacao' + str(x)] #informa a visualização atual, para criar uma soma de controle dentro do banco
            idvideo = video['id' + str(x)] 
            cursor.execute(
                "UPDATE VIEWERS SET aviewers = " + str(somavisualizacao) + " WHERE aidvideo = '" + str(idvideo) + "'")
            contador['a' + str(x)] = contador['a' + str(x)] + 1
            locals().update(contador) #atualiza a array
            conn.commit()
            conn.close()
            time.sleep(0.5) #aguarda para continuar, lembrando que a base é realizada por segundo (1) equivale a 1 segundo
        if int(contador['a' + str(x)]) > int(video['carregamento' + str(x)]): #Se a contagem for atingir a visualização recomendada, ele atualiza o banco novamente
            subprocess.run('downloadplaylist.py -e ', shell=True)  #Executa a leitura do banco para atualizar o menor video visualizado
            conn = sqlite3.connect('youtube.db')
            cursor = conn.cursor()
            print("\tAmbiente ", x, "alterando vídeo de ", video['titulo' + str(x)])
            contador['a' + str(x)] = 0
            cursor.execute("SELECT aidvideo, aurlvideo, aviewers, atitulo FROM VIEWERS ORDER BY aviewers Asc LIMIT 1")
            records = cursor.fetchall()
            for row in records:
                media3 = row[2]
                # aqui os valores dos menos visualizados irão para uma Array(variavel)
                video['id' + str(x)] = row[0]
                video['url' + str(x)] = row[1]
                video['visualizacao' + str(x)] = row[2]
                video['titulo' + str(x)] = row[3]
                locals().update(video)
                linha = linha + 1
                video['carregamento' + str(x)] = 20  # round(((media1/int(retorno))/(media2/int(retorno))))
                print("\tpara ", video['titulo' + str(x)])
                print("\teste processo irá gerar ", video['carregamento' + str(x)], " visualizações")
                for i in range(atualiza, -1, -1):
                    print(f"\b\b\b\t{i}", end="", flush=True)
                    time.sleep(1)
            conn.commit()
            conn.close()
            time.sleep(1)
        clear()
    except sqlite3.OperationalError:
        print("Aff")
        pass
