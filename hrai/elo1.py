import pandas as pd
import numpy as np


def calc_elo_bycr(df, elo, byc):
  df[f'ELO_{byc}_1'] = df[f'{byc}_1'].astype(str).map(elo).fillna(1000)
  df[f'ELO_{byc}_2'] = df[f'{byc}_2'].astype(str).map(elo).fillna(1000)
  df[f'P_D_{byc}'] = 1 / (1 + 10 ** ((df[f'ELO_{byc}_2'] - df[f'ELO_{byc}_1'])/400))
  df[f'D_ELO_{byc}'] = 20 * (df.win - df[f'P_D_{byc}']) 
  df[f'NEXT_ELO_{byc}'] = df[f'ELO_{byc}_1'] + df[f'D_ELO_{byc}'] 

  elo.update(df.groupby([f'{byc}_1'])[f'NEXT_ELO_{byc}'].agg("mean").to_dict())
  return df.reset_index(drop=True)

def calc_elo(df, byc):
  elo = {}
  df['win'] = (np.sign(df.ch_ordreArrivee_2 - df.ch_ordreArrivee_1) + 1.0) / 2.0
  bycr = df.groupby('aid_cr')
  r = bycr.apply(lambda x: calc_elo_bycr(x,elo,byc))
  return r


