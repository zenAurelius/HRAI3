import pandas as pd
import numpy as np
from statistics import NormalDist

'''df = pd.read_csv('./data/volcania_p.csv')
df =df[['aid_cr', 'ch_nom_1', 'ch_driver_1', 'ch_ordreArrivee_1', 'ch_nom_2', 'ch_driver_2', 'ch_ordreArrivee_2']]
df.to_csv('./data/volcania_s.csv', index=False)'''



'''params= {'dsg':float(25/3), 'dmu':float(25), 'tau':float(25.0 / 300.0), 'beta':float(25.0 / 6.0)}
b_sg = {}
b_mu = {}'''

_normal = NormalDist()

def calc_oskill_bycr(df, os_sg, os_mu, teams_members, debug=False):
    
    # teams_member = ['pis_cheval', 'pis_driver', 'pis_entraineur']
    dsg = float(25/3)
    dmu = float(25)
    tsq = float(25.0 / 300.0) ** 2
    for i in range(1, 3):
        # init sigma / mu -ok
        for mb in teams_members:
            df[f'pff_sg_{mb}_{i}'] = df[f'{mb}_{i}'].astype(str).map(os_sg).fillna(dsg)
            df[f'pff_mu_{mb}_{i}'] = df[f'{mb}_{i}'].astype(str).map(os_mu).fillna(dmu)

            # Correct Sigma With Tau -ok
            df[f'S_SGC_{mb}_{i}'] = np.sqrt(df[f'pff_sg_{mb}_{i}'] ** 2 + tsq)

        # Sigma et Mu de chaque equipe = somme des Sigma/Mu de chaque team members -ok
        df[f'pff_sgsq_{i}'] = sum([df[f'S_SGC_{x}_{i}'] ** 2 for x in teams_members])
        df[f'S_MU_{i}'] = sum([df[f'pff_mu_{x}_{i}'] for x in teams_members])

        df[f'pff_ord_{i}'] = df[f'S_MU_{i}'] - 3 * np.sqrt(df[f'pff_sgsq_{i}'])
  
    # Calcul "C" = sqrt(somme pour toutes les equipes de Sigma^2 + beta^2) -ok
    bsq = float(25.0 / 6.0) ** 2
    c = np.sqrt(df['pff_sgsq_1'] + df['pff_sgsq_2'] + 2 * bsq)

    for i in range(1, 3):
        # Calcul "sumQ" -ok
        df[f'S_SUMQT_{i}'] = np.exp(df[f'S_MU_{i}']/c)

        #Calcul "A" -ok
        df[f'S_A_{i}'] = 1
        df.loc[df['tgf_win_1'] == 0.5, f'S_A_{i}'] = 2

    df[f'S_SUMQ_1'] = df[f'S_SUMQT_1'] + np.where(df['tgf_win_1'] >= 0.5, df[f'S_SUMQT_2'], 0)
    df[f'S_SUMQ_2'] = df[f'S_SUMQT_2'] + np.where(df['tgf_win_1'] <= 0.5, df[f'S_SUMQT_1'], 0)

    #i = 1; q = 1
    df['S_DELTA_11'] =  df['S_SUMQT_1'] / df['S_SUMQ_1'] * (1 - df['S_SUMQT_1'] / df['S_SUMQ_1']) / df['S_A_1']
    df['S_DELTA_12'] =  df['S_SUMQT_1'] / df['S_SUMQ_2'] * (1 - df['S_SUMQT_1'] / df['S_SUMQ_2']) / df['S_A_2']
    df['S_DELTA_12'] = np.where(df['tgf_win_1'] <= 0.5, df['S_DELTA_12'], 0)
    df['S_DELTA_1'] = (np.sqrt(df['pff_sgsq_1']) / c) * (df['S_DELTA_11'] + df['S_DELTA_12']) * df['pff_sgsq_1'] / c ** 2

    df['S_OMG_11'] = (1 - df['S_SUMQT_1'] / df['S_SUMQ_1']) / df['S_A_1']
    df['S_OMG_12'] = (df['S_SUMQT_1'] / df['S_SUMQ_2']) / df['S_A_2']
    df['S_OMG_12'] = np.where(df['tgf_win_1'] <= 0.5, df['S_OMG_12'], 0)
    df['S_OMG_1'] = (df['S_OMG_11'] - df['S_OMG_12']) * df['pff_sgsq_1'] / c

    for mb in teams_members:
        # Calcul des deltas après le résultat
        df[f'OS_D_MU_{mb}_1'] = (df['S_OMG_1'] * df[f'S_SGC_{mb}_1'] ** 2 / df['pff_sgsq_1'])
        df[f'OS_D_SG_{mb}_1'] = np.sqrt(np.maximum(1 - (df['S_DELTA_1'] * df[f'S_SGC_{mb}_1']**2 / df['pff_sgsq_1']), 0.01))
        # Calcul des nouvelles valeurs
        df[f'OS_N_MU_{mb}_1'] = df[f'pff_mu_{mb}_1'] + (df['S_OMG_1'] * df[f'S_SGC_{mb}_1'] ** 2 / df['pff_sgsq_1'])
        df[f'OS_N_SG_{mb}_1'] = df[f'S_SGC_{mb}_1'] * np.sqrt(np.maximum(1 - (df['S_DELTA_1'] * df[f'S_SGC_{mb}_1']**2 / df['pff_sgsq_1']), 0.01))
        # Mise à jour du dictionnaire    
        bych = df.groupby([f'{mb}_1'])
        schu = bych[f'OS_D_SG_{mb}_1'].agg("prod")*bych[f'S_SGC_{mb}_1'].agg('first')
        mchu = bych[f'OS_D_MU_{mb}_1'].agg("sum")+bych[f'pff_mu_{mb}_1'].agg('first')
        os_sg.update(schu.to_dict())
        os_mu.update(mchu.to_dict())
    
    #prob win
    y = (df['S_MU_1'] - df['S_MU_2']) / np.sqrt(df['pff_sgsq_1'] + df['pff_sgsq_2'] + 4 * bsq)
    df['pff_pwin_1'] = y.apply(lambda x : _normal.cdf(x))

    if not debug:
        to_drop = [c for c in df.columns if c.startswith('S_')]
        df.drop(to_drop, axis=1, inplace=True)
    return df.reset_index(drop=True)

def calc_oskill(df, sg={}, mu={}, teams_members=[], debug=False):
  os_sg = sg
  os_mu = mu
  bycr = df.groupby('aid_cr')
  r = bycr.apply(lambda x: calc_oskill_bycr(x,os_sg,os_mu,teams_members,debug))
  return r


