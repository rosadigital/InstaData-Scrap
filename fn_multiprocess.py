import datetime
import pandas as pd
import json
from urllib.request import urlopen
from unicodedata import normalize
import multiprocessing

# split a list into evenly sized chunks
def chunks(l, n):
    #l = data
    #n = size (2 or 3)
    x = range(0, len(l), n)
    # print('x',x)
    return [l[i:i+n] for i in x]

def do_job1(username,followers_names_list):
    print('func1: starting')
    # getting gender on IBGE
    nome = 0
    genero_b = []
    genero_f = []
    genero_m = []
    genero_f_list = []
    genero_m_list = []
    genero_b_list = []
    name_list = []

    followers_names_list_updated = {
        'adjusted_names': name_list,
        'gender_f': genero_f_list,
        'gender_m': genero_m_list,
        'gender_b': genero_b_list
    }

    followers_names_list_updated = pd.DataFrame(data=followers_names_list_updated)
    print('followers_names_list_updated',followers_names_list_updated)
    try:
        relatorio_BD04_updated_created = pd.read_csv(str(username) + '/relatorio_DB04_followers_names_list_' + str(username) + '.csv',
                                    index=False)
        relatorio_BD04 = relatorio_BD04_updated_created.append([followers_names_list_updated], ignore_index=True)
        relatorio_BD04.to_csv(str(username) + '/relatorio_DB04_followers_names_list_' + str(username) + '.csv',
                                    index=False)

    except:
        followers_names_list_updated.to_csv(str(username) + '/relatorio_DB04_followers_names_list_' + str(username) + '.csv',
                                    index=False)

    for nome in followers_names_list:
        print('-----------fn 01---------------------')
        # adjusting nome
        try:
            encoded_name = normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
        except:
            pass
        print('nome', encoded_name)
        name_list.append(encoded_name)

        IBGE_2010_amount = []
        if nome == "business":
            genero_b.append(1)
            genero_f.append(0)
            genero_m.append(0)
        elif nome == 'NaN':
            genero_b.append(0)
            genero_f.append(0)
            genero_m.append(0)
        else:
            IBGE_2010_amount_f = 0
            IBGE_2010_amount_m = 0
            try:
                url = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/" + encoded_name + "?sexo=F"
                print(url)
                response = urlopen(url)
                json_response = json.loads(response.read())
                json_response = json_response[0]['res'][-1]
                IBGE_2010 = []
                for value in json_response.items():
                    IBGE_2010.append(value[-1])
                IBGE_2010_amount_f = IBGE_2010[-1]
                print('teste', IBGE_2010_amount_f)
                # IBGE_2010_amount.append(IBGE_2010_amount_f)
            except:
                IBGE_2010_amount_f = 0

            try:
                url = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/" + encoded_name + "?sexo=M"
                response = urlopen(url)
                json_response = json.loads(response.read())
                json_response = json_response[0]['res'][-1]
                IBGE_2010 = []
                for value in json_response.items():
                    IBGE_2010.append(value[-1])
                IBGE_2010_amount_m = IBGE_2010[-1]
                print('teste', IBGE_2010_amount_m)
                # IBGE_2010_amount.append(IBGE_2010_amount_m)
            except:
                IBGE_2010_amount_m = 0

            if IBGE_2010_amount_f > IBGE_2010_amount_m:
                # if IBGE_2010_amount[0] > IBGE_2010_amount[1]:
                genero_f.append(1)
                genero_m.append(0)
                genero_b.append(0)
                print("Segundo senso do IBGE, em 2010, há grandes chances de que o nome", nome, "seja feminino")
                print("feminino", IBGE_2010_amount_f)
                print("masculino", IBGE_2010_amount_m)
            else:
                genero_m.append(1)
                genero_f.append(0)
                genero_b.append(0)
                print("Segundo senso do IBGE, em 2010, há grandes chances de que o nome", nome, "seja masculino")
                print("feminino", IBGE_2010_amount_f)
                print("masculino", IBGE_2010_amount_m)

    # followers_names_list = followers_names_list
    # followers_names_list['gender_f'] = genero_f
    # followers_names_list['gender_m'] = genero_m
    # followers_names_list['gender_b'] = genero_b

    genero_f_list = genero_f
    genero_m_list = genero_m
    genero_b_list = genero_b

    # print(name_list)
    # print(len(name_list))
    #
    # print(genero_f_list)
    # print(len(genero_f_list))
    #
    # print(genero_m_list)
    # print(len(genero_m_list))
    #
    # print(genero_b_list)
    # print(len(genero_b_list))


    followers_names_list_updated = {
        'adjusted_names': name_list,
        'gender_f': genero_f_list,
        'gender_m': genero_m_list,
        'gender_b': genero_b_list
    }

    followers_names_list_updated = pd.DataFrame(data=followers_names_list_updated)
    # print(followers_names_list_updated)

    relatorio_BD04 = pd.read_csv(str(username) + '/relatorio_DB04_followers_names_list_' + str(username) + '.csv')
    # print('relatorio_04',relatorio_BD04)

    relatorio_BD04 = relatorio_BD04.append([followers_names_list_updated], ignore_index=True)
    # print('relatorio_04',relatorio_BD04)

    relatorio_BD04.to_csv(str(username) + '/relatorio_DB04_followers_names_list_' + str(username) + '.csv',
                                    index=False)

    # os.remove(str(username)+'/relatorio_DB04_followers_names_list_adjusted_'+str(username)+'.csv')

def dispatch_jobs(data,username):
    total = len(data) #ex 20 dados
    chunk_size = total / 2 #chunks de 10

    #to create chunck
    slice = chunks(data, int(chunk_size))

    #grupos para pesquisar
    first = slice[0]
    second = slice[1]

    p1 = multiprocessing.Process(target=do_job1, args=(username,first,))
    p2 = multiprocessing.Process(target=do_job1, args=(username,second,))
    p1.start()
    p2.start()
    p1.join()
    p1.join()






def fn_multiprocess(username,root_folder):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    t0 = datetime.datetime.now()

    # username = 'coisandoporai'
    username = username
    path = root_folder + '/' + username

    #selecionar apenas coluna que será pesquisada
    file_name = '/relatorio_DB04_followers_names_list_adjusted_' + str(username)
    doc_source = pd.read_csv(str(username) + str(file_name) + '.csv')
    followers_names_list = doc_source['adjusted_names']
    data = followers_names_list
    print(len(data))
    dispatch_jobs(data, username)

    t1 = datetime.datetime.now()
    time_running = t1 - t0
    print(time_running)