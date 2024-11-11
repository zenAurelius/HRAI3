
import pandas as pd
import numpy as np
import time
import skills
import combine



def pct_place(df):
    pct = 100 * len(df[df.ch_ordreArrivee_1 <= 3.0]) / len(df)
    print(f'placé {pct}%')

'''df = pd.read_csv('./data/pmu2014_c_e.csv')
print(df.describe())
##df[df.ch_nom_1 == 'VALEUR DANOVER'].to_csv('test.csv')


result = result = df.groupby(['aid_cr', 'ch_nom_1']).first().reset_index()
result['Rang'] = result.groupby('aid_cr')['ELO_1'].rank(ascending=False)

pct_place(result[result.Rang == 1.0])
pct_place(result[result.Rang == 2.0])
pct_place(result[result.Rang == 3.0])
pct_place(result[result.Rang == 10.0])'''


# df = pd.read_csv('./data/pmu2016cc_os.csv')
# # df = df[df.ch_driver_1 == 'E. RAFFIN']
# # df.to_csv('./data/pmu2016m.csv')
# df.head(5000).to_csv('./data/pmu2016s.csv')

# df = pd.read_csv('./data/pmu2016s.csv')
# df.ch_estplace_1 = (df['ch_ordreArrivee_1'] < 3) | ((df['ch_ordreArrivee_1'] == 3) & (df['cr_nombreDeclaresPartants'] > 7))
# print(df[['cr_nombreDeclaresPartants','ch_ordreArrivee_1','ch_estplace_1']])
# df.to_csv('./data/pmu2016sc.csv')

# df = pd.read_csv('./data/pmu2016s.csv')
# df = df[(df.aid_pt_2 == '160101R01C0409') & (df.aid_pt_1 == '160101R01C0404')]
# df.to_csv('./data/pmu2016_cas', index=False)

# df = pd.read_csv('./data/pmu2016cc_os.csv')
# result = df[df.ch_dernierRapportDirect_rapport_1 > 0].groupby(['aid_cr', 'ch_nom_1']).first().reset_index()
# print(len(result))
# result['OS_R'] = result.groupby('aid_cr')['OS_ORD_1'].rank(ascending=False)
# df = result[result.OS_R == 1.0]
# print(df[['ch_dernierRapportDirect_rapport_1','OS_ORD_1']].describe())


# Améliorer la lecture du fichier : traiter DtypeWarning 85 seconds => 10 seconds
''' CLEAN(C) FROM RAW '''
# start_time = time.time()
# df = pd.read_csv('./data/pmu2016.csv')
# elapsed_time = time.time() - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")

# start_time = time.time()
# df = combine.clean(df)
# elapsed_time = time.time() - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# df.to_csv('./data/pmu2016_c.csv', index=False)

''' CONBINE(V) FROM CLEAN(C) '''
# start_time = time.time()
# df = pd.read_csv('./data/pmu2016_c.csv')
# elapsed_time = time.time() - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# start_time = time.time()
# df = combine.un_vs_un(df)
# elapsed_time = time.time() - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# df.to_csv('./data/pmu2016_v.csv', index=False)

''' SKILLED(OS) FROM COMBINE(V) '''
start_time = time.time()
df = pd.read_csv('./data/pmu2016_v.csv')
elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
start_time = time.time()
df = skills.calc_oskill(df,teams_members=['pis_cheval', 'pis_driver'])
elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
df.to_csv('./data/pmu2016_os.csv', index=False)

# df = pd.read_csv('./data/pmu2017_os_s.csv')
# print(df.dtypes)