
import pandas as pd
import numpy as np
import skills



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


# from openskill.models import PlackettLuce
# model = PlackettLuce()
# ch1 = model.rating(name='ch_1',mu=25, sigma=8.33333333)
# dv1 = model.rating(name='dv_1',mu=52.5001247052428, sigma=6.16190376200572)
# ch2 = model.rating(name='ch_2',mu=25, sigma=8.3333333)
# dv2 = model.rating(name='dv_2',mu=5.35705378196938, sigma=6.16190376200572)
# team1 = [ch1, dv1]
# team2 = [ch2, dv2]
# #[team1, team2] = model.rate([team1, team2],ranks=[1,1])
# #[team1, team2] = model.rate([team1, team2])
# print(model.predict_win([team1, team2]))


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

df = pd.read_csv('./data/pmu2016_cas.csv')
mu = {'F. NIVARD':52.5001247052428,'VERNOUILLET':25.0, 'VOSS RINGEAT':25.0, 'G. ROIG-BALAGUER':5.35705378196938}
sg = {'F. NIVARD':6.16190376200572,'VERNOUILLET':8.33333333333333, 'VOSS RINGEAT':8.33333333333333, 'G. ROIG-BALAGUER':6.16190376200572}
df = skills.calc_oskill(df, mu=mu, sg=sg)
df.to_csv('./data/pmu2016_cas_os.csv', index=False)

# df = pd.read_csv('./data/pmu2016cc_os.csv')
# result = df[df.ch_dernierRapportDirect_rapport_1 > 0].groupby(['aid_cr', 'ch_nom_1']).first().reset_index()
# print(len(result))
# result['OS_R'] = result.groupby('aid_cr')['OS_ORD_1'].rank(ascending=False)
# df = result[result.OS_R == 1.0]
# print(df[['ch_dernierRapportDirect_rapport_1','OS_ORD_1']].describe())

