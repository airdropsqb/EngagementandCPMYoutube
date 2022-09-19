from pytube import Playlist #É utilizado para consultar o Youtube e permitir a visualização da sua Playlist.
import sqlite3 #Permite o Python interagir com o SQLite, você pode usar outros bancos, mas para aprendizagem este serve.
from sqlite_utils import Database #É utilizado manusear o banco de dados DB criado em algum momento.

url = 'https://www.youtube.com/playlist?list=PL_bWKnK7ufEAzouYibMW-Uvo6BDR0HzOP'  #Aqui você alimenta a variavel, com o link da sua playlist.
purl = Playlist(url) #Neste momento o modulo pytube, converte sua variavel url para permitir a leitura dos dados do Youtube, na variavel purl.
total = len(purl.videos) #Aqui a leitura do total de vídeos na sua playlist.
ciclo = total #Dando o mesmo valor para uma segunda variavel, para calculos futuros.
validar = 0 #variavel para contadores
novoviewers = 0 #variavel para contadores
print(f'Carregando download: {url.title}', 'total de videos: ', total) #você não precisa exatamente deste print, serve para mostrar se foi conectado e validado.

conn = sqlite3.connect('youtube.db') #Caso não existe o DB, ele cria um para você
cursor = conn.cursor() #Ele ativa o controle e manipulação do banco de dados
cursor.execute("""CREATE TABLE IF NOT EXISTS VIEWERS (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             aidvideo TEXT, aurlvideo TEXT, atitulo TEXT, aviewers NUMERIC );""") # Aqui ele cria uma tabela, caso ela não exista, com os campos informados.
conn.commit() #Fecha a manipulação do banco
conn.close() #Desativa o acesso exclusivo ao banco, permitindo você manipular com outras aplicações.

for video in purl.videos: #Então ele vai gerar um loop executando funções informadas abaixo para cada vídeo da sua playlist.
    total = total - 1 #É apenas um contador, para você validar quantos vídeos faltam para serem lidos pelo Script.
    idvideo = str(video.video_id.strip()) #Estes dados, são lidos diretamente do Youtube, através da API do Pytube (https://pytube.io), o strip() remove espaços em branco desnecessários.
    linkvideo = str(video.watch_url.strip()) #Estes dados, são lidos diretamente do Youtube, através da API do Pytube (https://pytube.io), o strip() remove espaços em branco desnecessários.
    aviewers = str(video.views) #Estes dados, são lidos diretamente do Youtube, através da API do Pytube (https://pytube.io), o strip() remove espaços em branco desnecessários.
    titulo = str(video.title.strip()) #Estes dados, são lidos diretamente do Youtube, através da API do Pytube (https://pytube.io), o strip() remove espaços em branco desnecessários.
#   print("Falta: ", total ,"Vídeo: ", linkvideo, "Engajamento: ",aviewers) #você pode escolher imprimir cada linha consultada na tela.

    conn = sqlite3.connect('youtube.db') #acessando o db novamente.
    cursor = conn.cursor() #Ativando a manipulação do banco.
    cursor.execute("SELECT count(aidvideo), aviewers FROM VIEWERS WHERE aidvideo = '" + idvideo + "'") #Aqui, ele vai consultar se o ID youtube já está na tabela
    records = cursor.fetchall() #Aqui ele usa o count para dar valor a linha especifica da tabela.
    for row in records: 
        try:
            if row[0] == 0: #Então ele pergunta, se não existir retorno na consulta, então ele pode inserir os dados na tabela.
                try: 
                    cursor.execute(
                        "INSERT INTO VIEWERS (aidvideo, aurlvideo, aviewers, atitulo) SELECT  '" + idvideo + "', '" + linkvideo + "', '" + aviewers + "', '" + titulo + "' WHERE NOT EXISTS (SELECT aidvideo FROM VIEWERS WHERE aidvideo = '" + idvideo + "')")  #Insere uma linha caso não exista
                    print(total," -> Novo vídeo:  " + titulo + " total: ", aviewers, ".") #imprime um texto qualquer para informar inserção.
                    novoviewers = novoviewers + int(aviewers) #É apenas um contador.
                except:
                    validar = validar - 1 #É apenas um contador
                    pass #Se der erro de alguma forma ele continua a leitura da playlist.
            if int(row[1]) != int(aviewers): #Se existir, e o valor de visualizações for diferente, ele atualiza as visualizações de acordo com o que está no Youtube
                try:
                    cursor.execute(
                        "UPDATE VIEWERS SET aviewers = " + aviewers + " WHERE aidvideo = '" + str(idvideo) + "'")
                    print(total," -> Atualizado vídeo: " + titulo + " de ", row[1], " para ", aviewers, ".")
                    novoviewers = novoviewers + (int(aviewers)-int(row[1]))
                except:
                    validar = validar - 1
                    pass
            if int(row[1]) == int(aviewers):
                print(total, " -> Sem alteração no vídeo: " + titulo)

        except TypeError:
            pass
        conn.commit() #Fecha a manipulação do banco
        conn.close() #Desativa o acesso exclusivo ao banco, permitindo você manipular com outras aplicações.
    validar = validar + 1
print("Total de vídeos consultados: " + str(ciclo)) #São apenas textos de leitura, nada de mais.
print("Total de vídeos registrados: " + str(validar))
print("Sua playlist teve :",novoviewers," alterações de viewers")
