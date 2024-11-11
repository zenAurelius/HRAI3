import pandas as pd
import skills
from openskill.models import PlackettLuce


print("** OPEN SKILLS **")
model = PlackettLuce()
ch1 = model.rating(name='ch_1',mu=25, sigma=8.33333333)
dv1 = model.rating(name='dv_1',mu=52.5001247052428, sigma=6.16190376200572)
ch2 = model.rating(name='ch_2',mu=25, sigma=8.3333333)
dv2 = model.rating(name='dv_2',mu=5.35705378196938, sigma=6.16190376200572)
team1 = [ch1, dv1]
team2 = [ch2, dv2]
[team1, team2] = model.rate([team1, team2],ranks=[1,1])
#[team1, team2] = model.rate([team1, team2])
print(team1, team2)
print(model.predict_win([team1, team2]))

print("** PANDAS SKILLS **")
df = pd.read_csv('./data/pmu2016_t.csv')
mu = {'F. NIVARD':52.5001247052428,'VERNOUILLET':25.0, 'VOSS RINGEAT':25.0, 'G. ROIG-BALAGUER':5.35705378196938}
sg = {'F. NIVARD':6.16190376200572,'VERNOUILLET':8.33333333333333, 'VOSS RINGEAT':8.33333333333333, 'G. ROIG-BALAGUER':6.16190376200572}
df = skills.calc_oskill(df, mu=mu, sg=sg, teams_members=['pis_cheval', 'pis_driver'], debug=True)

print('- team 1 member ratings :')
print(f'S_SGC_pis_cheval_1 = {df.iloc[0].S_SGC_pis_cheval_1}')
print(f'OS_MU_pis_cheval_1 = {df.iloc[0].OS_MU_pis_cheval_1}')
print(f'S_SGC_pis_driver_1 = {df.iloc[0].S_SGC_pis_driver_1}')
print(f'OS_MU_pis_driver_1 = {df.iloc[0].OS_MU_pis_cheval_1}')
print('- team 2 member ratings :')
print(f'S_SGC_pis_cheval_2 = {df.iloc[0].S_SGC_pis_cheval_2}')
print(f'OS_MU_pis_cheval_2 = {df.iloc[0].OS_MU_pis_cheval_2}')
print(f'S_SGC_pis_driver_2 = {df.iloc[0].S_SGC_pis_driver_2}')
print(f'OS_MU_pis_driver_2 = {df.iloc[0].OS_MU_pis_cheval_2}')
print('- team_ratings :')
print(f'S_SGSQ_1 = {df.iloc[0].S_SGSQ_1}')
print(f'S_SGSQ_2 = {df.iloc[0].S_SGSQ_2}')
print(f'S_MU_1 = {df.iloc[0].S_MU_1}')
print(f'S_MU_2 = {df.iloc[0].S_MU_2}')
print(f'S_SUMQT_1 = {df.iloc[0].S_SUMQT_1}')
print(f'S_SUMQT_2 = {df.iloc[0].S_SUMQT_2}')
print(f'S_SUMQ_1 = {df.iloc[0].S_SUMQ_1}')
print(f'S_SUMQ_2 = {df.iloc[0].S_SUMQ_2}')
print(f'S_A_1 = {df.iloc[0].S_A_1}')
print(f'S_A_2 = {df.iloc[0].S_A_2}')
print(f'S_OMG_1 = {df.iloc[0].S_OMG_1}')
print(f'S_DELTA_1 = {df.iloc[0].S_DELTA_1}')

