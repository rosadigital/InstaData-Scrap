import pandas as pd
import os

username = 'coisandoporai'

report_03_bio = pd.read_csv(str(username) + '/report_03_bio_' + str(username) + '.csv')
report_03_bio.to_csv(str(username) + '/report_03_' + str(username) + '.csv', index=False)
os.remove(str(username) + '/report_03_bio_' + str(username) + '.csv')

