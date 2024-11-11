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
    crout = crout.drop(columns=[x for x in list(crout) if x.startswith('r') and x.endswith('_2')])
    crout = crout.rename(columns={x:x[:-2] for x in list(crout) if x.startswith('r') and x.endswith('_1')})
    # mesure la target win (1 si gagne, 0 si perd, 0.5 si ex-aequo)
    crout['tgf_win_1'] = (np.sign(crout['tgi_ordreArrivee_2'] - crout['tgi_ordreArrivee_1']) + 1.0) / 2.0
    crout['tgf_win_2'] = (np.sign(crout['tgi_ordreArrivee_1'] - crout['tgi_ordreArrivee_2']) + 1.0) / 2.0
    return crout

def clean(df):
    '''
    A partir du fichier brut issu du scrapper, retourne un fichier "clean", avec les colonnes d'intéret arrangées et de nouvelle colonnes
    '''

    # Afficher les premières lignes du DataFrame avant la modification
    print("Avant la modification :")
    print(df.head())

    # Ne garde que les courses "arrivée", pas les "annulée"
    df = df[df.cr_categorieStatut == 'ARRIVEE'].copy()
    
    # course
    df['rfs_date'] =  pd.to_datetime(df['cr_heureDepart'], unit='ms').dt.strftime("%y%m%d")
    df['rfs_heure'] =  pd.to_datetime(df['cr_heureDepart'], unit='ms').dt.strftime("%H%M")
    df['ris_nom'] = df['cr_libelleCourt']
    df['rfi_prix'] = df['cr_montantPrix']
    df['rfi_distance'] = df['cr_distance']
    df['rfs_corde'] = df['cr_corde'].fillna('CORDE_DROITE')
    df['rfs_condSexe'] = df['cr_conditionSexe']
    df['rfi_nbPartants'] = df['cr_nombreDeclaresPartants']
    df['rfs_hippodrome'] = df['cr_hippodrome_codeHippodrome']
    df['rfs_nebulosite'] = df['cr_nebulositeCode']
    df['rff_temperature'] = df['cr_temperature'].fillna(16.0)
    df['rfi_ventForce'] = df['cr_forceVent']
    df['rfi_ventDirection'] = df['cr_directionVent']
    df['rfs_penetrometre'] = df['cr_penetrometre_intitule'].fillna('Inconnu')
    df['rfi_typePiste'] = df['cr_typePiste'].fillna('Inconnu')
    df['rff_vmoy'] = (df.cr_distance / df.cr_dureeCourse).fillna(13.0)
    df['rfb_autostart'] = df.cr_categorieParticularite.str.contains('AUTOSTART', regex=False).fillna(False)
    df['rfb_amateurs'] = df.cr_categorieParticularite.str.contains('AMATEURS', regex=False).fillna(False)

    # participation
    df['pis_cheval'] = df['ch_nom']
    df['pis_proprietaire'] = df['ch_proprietaire']
    df['pis_entraineur'] = df['ch_entraineur']
    df['pis_driver'] = df['ch_driver']
    df['pis_eleveur'] = df['ch_eleveur'].fillna('Inconnu')
    df['pfi_chAge'] = df['ch_age']
    df['pfs_chSexe'] = df['ch_sexe']
    df['pfs_chRace'] = df['ch_race']
    df['pib_partant'] = df.ch_statut == 'PARTANT'
    df['pfb_oeilleres'] = df['ch_oeilleres'] != 'SANS_OEILLERES'
    df['pfb_dvChange'] = df['ch_driverChange']
    df['pfb_chInedit'] = df['ch_indicateurInedit']
    df['pfi_chNbCourses'] = df['ch_nombreCourses']
    df['pfi_chNbVictoires'] = df['ch_nombreVictoires']
    df['pfi_chNbPlaces'] = df['ch_nombrePlaces']
    df['pfi_chNbSecond'] = df['ch_nombrePlacesSecond']
    df['pfi_chNbTroisieme'] = df['ch_nombrePlacesTroisieme']
    df['pff_chGainTotal'] = df['ch_gainsParticipant_gainsCarriere']
    df['pff_chGainVictoire'] = df['ch_gainsParticipant_gainsVictoires']
    df['pff_chGainPlace'] = df['ch_gainsParticipant_gainsPlace']
    df['pff_chGainAnnee'] = df['ch_gainsParticipant_gainsAnneeEnCours']
    df['pff_chGainAnneePrec'] = df['ch_gainsParticipant_gainsAnneePrecedente']
    df['pfb_chEstJumentPleine'] = df['ch_jumentPleine']
    df['pff_handicap'] = ((df['ch_handicapDistance'] - df['cr_distance'])/df['cr_distance'])
    df['pff_rapportDirect'] = df['ch_dernierRapportDirect_rapport']
    df['pff_tendanceDirect'] = df['ch_dernierRapportDirect_indicateurTendance'].fillna(' ')
    df['pff_permutationDirect'] = df['ch_dernierRapportDirect_permutation']
    df['pff_favorisDirect'] = df['ch_dernierRapportDirect_favoris'].fillna(False)
    df['pff_priseDirect'] = df['ch_dernierRapportDirect_grossePrise'].fillna(False)
    df['pff_rapportReference'] = df['ch_dernierRapportReference_rapport']
    df['pff_tendanceReference'] = df['ch_dernierRapportReference_indicateurTendance'].fillna(' ')
    df['pff_permutationReference'] = df['ch_dernierRapportReference_permutation']
    df['pff_favorisReference'] = df['ch_dernierRapportReference_favoris'].fillna(False)
    df['pff_priseReference'] = df['ch_dernierRapportReference_grossePrise'].fillna(False)
    df['pfs_deferre'] = df['ch_deferre']
    df['pfi_placeCorde'] = df['ch_placeCorde']
    df['pfs_ecurie'] = df['ch_ecurie']
    df['pff_txReclamation'] = df['ch_tauxReclamation']

    # targets
    df['tgi_ordreArrivee'] = df['ch_ordreArrivee'].fillna(11)
    df['tgf_tempsObtenue'] = df['ch_tempsObtenu']
    df['tgf_reductionKm'] = df['ch_reductionKilometrique']
    df['tgb_estPlace'] = (df['ch_ordreArrivee'] < 3) | ((df['ch_ordreArrivee'] == 3) & (df['cr_nombreDeclaresPartants'] > 7))
    df['tgb_estGagnant'] = (df['ch_ordreArrivee'] == 1)

    # IDs
    df['aid_re'] = df.rfs_date + 'R' + df.cr_numReunion.astype(str).str.zfill(2)
    df['aid_cr'] = df.aid_re + 'C' + df.cr_numOrdre.astype(str).str.zfill(2)
    df['aid_pt'] = df.aid_cr + 'P' + df.ch_numPmu.astype(str).str.zfill(2)

    df = df.drop(df.filter(regex='^(cr_|ch_)').columns, axis=1)

    return df
  