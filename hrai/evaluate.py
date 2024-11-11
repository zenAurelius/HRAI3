
import pandas as pd
import time
import numpy as np

import combine
import elo1
import skills





def pct_place(df):
    n = len(df)
    npl = len(df[df.tgb_estPlace_1])
    nga = len(df[df.tgb_estGagnant_1])
    print(f'placé {100 * npl / n:.2f}%  [{npl}/{n}] - gagnant {100 * nga / n:.2f}% [{nga}/{n}]')
    df['gain_gagnant'] = np.where(df['tgb_estGagnant_1'], df['pff_rapportDirect_1']-1, -1)
    print(f'gain gagnant = {df.gain_gagnant.sum()}')


def evaluate_indicateur(df, idname, ascending=False):
    ntot = len(df)
    # 1. evaluation brute en 1c1
    print('* evaluation brute 1c1')
    # dummy : le 1 gagne
    ntrue = len(df[(df['tgi_ordreArrivee_1'] < df['tgi_ordreArrivee_2'])])
    nfalse = len(df[(df['tgi_ordreArrivee_1'] > df['tgi_ordreArrivee_2'])])
    print(f'[dummy] true = {100 * ntrue / ntot} - false = {100 * nfalse / ntot}')  
    # cote : la plus petite cote gagne
    ntrue = 2*len(df[(df['tgi_ordreArrivee_1'] < df['tgi_ordreArrivee_2']) & (df['pff_rapportDirect_1'] < df['pff_rapportDirect_2'])])
    nfalse = 2*len(df[(df['tgi_ordreArrivee_1'] < df['tgi_ordreArrivee_2']) & (df['pff_rapportDirect_1'] > df['pff_rapportDirect_2'])])
    print(f'[cote] true = {100 * ntrue / ntot} - false = {100 * nfalse / ntot}')
    # indicateur
    ntrue = 2*len(df[(df['tgi_ordreArrivee_1'] < df['tgi_ordreArrivee_2']) & (df[f'{idname}_1'] > df[f'{idname}_2'])])
    nfalse = 2*len(df[(df['tgi_ordreArrivee_1'] > df['tgi_ordreArrivee_2']) & (df[f'{idname}_1'] > df[f'{idname}_2'])])
    print(f'[{idname}] true = {100 * ntrue / ntot} - false = {100 * nfalse / ntot}')
    
    # 2. evalutation par ordre de l'indicateur dans la course
    # filtre sur les cas avec cotes - reset (pour pouvoir calculer les gains gagnants)
    result = df[df.pff_rapportDirect_1 > 0].groupby(['aid_cr', 'pis_cheval_1']).first().reset_index()
    print('\n* evaluation meilleur de l\'indicateur')
    bycr = result.groupby('aid_cr')
    result[f'{idname}_R'] = bycr[f'{idname}_1'].rank(ascending=ascending)
    result['COTE_R'] = bycr['pff_rapportDirect_1'].rank()
    print(f'__{idname}__')
    pct_place(result[result[f'{idname}_R'] == 1.0].copy())
    print('__cote__')
    pct_place(result[result.COTE_R == 1.0].copy())

    # 3. evaluation par quartile : on prend les limites des quartiles et on mesure les perfs du premier seulement si dans le quartile
    print('\n* evaluation meilleur par quartile de l\indicateur')
    firsts = result[result[f'{idname}_R'] == 1.0]
    q4 = firsts[f'{idname}_1'].quantile([0.25,0.5,0.75])
    print(f'{idname} = {q4}')
    pct_place(firsts[firsts[f'{idname}_1'] < q4[0.25]].copy())
    pct_place(firsts[(firsts[f'{idname}_1'] > q4[0.25]) & (firsts[f'{idname}_1'] < q4[0.5])].copy())
    pct_place(firsts[(firsts[f'{idname}_1'] > q4[0.5]) & (firsts[f'{idname}_1'] < q4[0.75])].copy())
    pct_place(firsts[firsts[f'{idname}_1'] > q4[0.75]].copy()) 

    # 4. Mise à l'écart des courses les moins bien connues
    print('\n* evaluation meilleur par quartile de la moyenne des sigmma')
    result['OS_SG_M'] = bycr['pff_sgsq_1'].transform('mean')
    firsts = result[result[f'{idname}_R'] == 1.0]
    q4 = firsts['OS_SG_M'].quantile([0.25,0.5,0.75])
    print(f'sigma = {q4}')
    pct_place(firsts[firsts['OS_SG_M'] < q4[0.25]].copy())
    pct_place(firsts[(firsts['OS_SG_M'] > q4[0.25]) & (firsts['OS_SG_M'] < q4[0.5])].copy())
    pct_place(firsts[(firsts['OS_SG_M'] > q4[0.5]) & (firsts['OS_SG_M'] < q4[0.75])].copy())
    pct_place(firsts[firsts['OS_SG_M'] > q4[0.75]].copy()) 


##df[df.ch_nom_1 == 'VALEUR DANOVER'].to_csv('test.csv')

df = pd.read_csv('./data/pmu2016_os.csv')
evaluate_indicateur(df, 'pff_ord')

