import pandas as pd
from unicodedata import normalize

def fn_ajuste_de_nomes(username):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    #importing db
    db02 = pd.read_csv(str(username)+'/relatorio_DB02_vid_and_img_'+str(username)+'.csv')
    followers_names_db02 = db02[['followers_links','followers_names']]
    db03 = pd.read_csv(str(username)+'/relatorio_DB03_bio_'+str(username)+'.csv')
    followers_names_db03 = db03[['followers_links','followers_names']]

    #concatenating db02 and db03
    frame = [followers_names_db02, followers_names_db03]
    followers_names_list = pd.concat(frame)
    followers_names_list = followers_names_list.drop_duplicates()
    followers_names_list = pd.DataFrame(data=followers_names_list)

    #getting first name
    followers_names_list_split = followers_names_list.followers_names.str.split(expand=True)[0]
    followers_names_list_split = pd.DataFrame(data=followers_names_list_split).rename(columns={0: "first_name"})
    # print(followers_names_list_split)

    followers_names_list = pd.concat([followers_names_list, followers_names_list_split], axis=1, sort=False)
    followers_names_list['adjusted_names'] = followers_names_list_split
    followers_names_list = followers_names_list.sort_values(by=['adjusted_names'])
    followers_names_list = followers_names_list.reset_index(drop=True)
    print(followers_names_list[['followers_names','first_name']])

    # MANUAL ADJUST OF NAMES IN SOME LINES (coisando por ai)
    # followers_names_list.at[0,'adjusted_names'] = 'Adriana'
    # followers_names_list.at[15,'adjusted_names'] = 'business'
    # followers_names_list.at[21,'adjusted_names'] = 'business'
    # followers_names_list.at[23,'adjusted_names'] = 'Debora'
    # followers_names_list.at[25,'adjusted_names'] = 'Damaris'
    # followers_names_list.at[30,'adjusted_names'] = 'Rubenique'
    # followers_names_list.at[31,'adjusted_names'] = 'joão'
    # followers_names_list.at[34,'adjusted_names'] = 'business'
    # followers_names_list.at[53,'adjusted_names'] = 'carlos'
    # followers_names_list.at[55,'adjusted_names'] = 'Kezia'
    # followers_names_list.at[64,'adjusted_names'] = 'business'
    # followers_names_list.at[81,'adjusted_names'] = 'nilson'
    # followers_names_list.at[82,'adjusted_names'] = 'business'
    # followers_names_list.at[83,'adjusted_names'] = 'Paula'
    # followers_names_list.at[86,'adjusted_names'] = 'business'
    # followers_names_list.at[87,'adjusted_names'] = 'juliana'
    # followers_names_list.at[88,'adjusted_names'] = 'business'
    # followers_names_list.at[91,'adjusted_names'] = 'ricardo'
    # followers_names_list.at[98,'adjusted_names'] = 'thais'
    # followers_names_list.at[101,'adjusted_names'] = 'business'
    # followers_names_list.at[105,'adjusted_names'] = 'business'
    # followers_names_list.at[107,'adjusted_names'] = 'ana'
    # followers_names_list.at[111,'adjusted_names'] = 'henrique'
    # followers_names_list.at[112,'adjusted_names'] = 'NaN'
    # followers_names_list.at[113,'adjusted_names'] = 'NaN'

    #creating business column with 1 for business and 0 for others
    # followers_names_list['gender_b'] = np.where(followers_names_list['adjusted_names'] != 'business', 0, 1)

    normalized_adjusted_names = []
    for adjusted_names in followers_names_list['adjusted_names']:
        try:
            encoded_name = normalize('NFKD', adjusted_names).encode('ASCII', 'ignore').decode('ASCII')
        except:
            pass
        print('nome', encoded_name)
        normalized_adjusted_names.append(encoded_name)

    followers_names_list['adjusted_names'] = normalized_adjusted_names

    # print(followers_names_list)

    followers_names_list = pd.DataFrame(data=followers_names_list)
    followers_names_list.to_csv(str(username) + '/relatorio_DB04_followers_names_list_adjusted_' + str(username) + '.csv', index=False)
    # print(followers_names_list)

