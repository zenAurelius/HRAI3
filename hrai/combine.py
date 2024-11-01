import pandas as pd
import numpy as np
from itertools import combinations, product
import time


# la fonction qui combine les participations deux à deux, appelé sur un groupby,
# le df param est l'ensemble des participations d'une course
def cartesian_product(df):
    index_combinations = list(product(df.index, repeat=2))
    result = pd.DataFrame(index_combinations, columns=['index1', 'index2'])
    result = result.merge(df, left_on='index1', right_index=True)
    result = result.merge(df, left_on='index2', right_index=True, suffixes=('_1', '_2'))
    result = result[result['index1'] != result['index2']]
    return result.reset_index(drop=True)


def un_vs_un(df):
    # regroupement par course
    grouped = df.groupby('aid_cr')
    # combinaison 1 contre 1 par le produit cartesien
    crout = grouped.apply(lambda x : cartesian_product(x))
    # reconstruit les index
    crout = crout.drop(columns=['aid_cr_1','aid_cr_2','index1','index2']).reset_index().drop(columns=['level_1'])
    # retire les colonnes en double qui concerne la course
    crout = crout.drop(columns=[x for x in list(crout) if x.startswith('cr_') and x.endswith('_2')])
    crout = crout.rename(columns={x:x[:-2] for x in list(crout) if x.startswith('cr_') and x.endswith('_1')})
    return crout

def clean(df):
    # Afficher les premières lignes du DataFrame avant la modification
    print("Avant la modification :")
    print(df.head())
    df['cr_date'] =  pd.to_datetime(df['cr_heureDepart'], unit='ms').dt.strftime("%y%m%d")
    df['ch_ordreArrivee'] = df['ch_ordreArrivee'].replace(np.nan, 11.0)
    df['aid_cr'] = df.cr_date + 'R' + df.cr_numReunion.astype(str).str.zfill(2) + 'C' + df.cr_numOrdre.astype(str).str.zfill(2)
    df['aid_pt'] = df.aid_cr + df.ch_numPmu.astype(str).str.zfill(2)
    df['ch_estplace'] = (df['ch_ordreArrivee'] < 3) | ((df['ch_ordreArrivee'] == 3) & (df['cr_nombreDeclaresPartants'] > 7))
    df['ch_estgagnant'] = (df['ch_ordreArrivee'] == 1)
    return df
  