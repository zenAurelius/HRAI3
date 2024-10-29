import requests
import json
from datetime import datetime, timedelta
import time
import pandas as pd
import flatdict


cr_k=['numReunion', 'numOrdre', 'heureDepart', 'libelleCourt', 'montantPrix', 'parcours', 'distance', 'distanceUnit', 'corde', 'discipline', 'specialite', 'categorieParticularite', 'conditionSexe', 'nombreDeclaresPartants', 'grandPrixNationalTrot', 'numSocieteMere', 'montantTotalOffert', 'montantOffert1er', 'montantOffert2eme', 'montantOffert3eme', 'montantOffert4eme', 'montantOffert5eme', 'numCourseDedoublee', 'dureeCourse', 'hippodrome_codeHippodrome']
ch_k = ["nom","numPmu","age","sexe","race","statut","oeilleres","proprietaire","entraineur","deferre","driver","driverChange","robe_code","indicateurInedit","musique","nombreCourses","nombreVictoires","nombrePlaces","nombrePlacesSecond","nombrePlacesTroisieme","gainsParticipant_gainsCarriere","gainsParticipant_gainsVictoires","gainsParticipant_gainsPlace","gainsParticipant_gainsAnneeEnCours","gainsParticipant_gainsAnneePrecedente","nomPere","nomMere","ordreArrivee","jumentPleine","engagement","supplement","handicapDistance","poidsConditionMonteChange","tempsObtenu","reductionKilometrique","dernierRapportDirect_rapport","dernierRapportDirect_indicateurTendance","dernierRapportDirect_permutation","dernierRapportDirect_favoris","dernierRapportDirect_grossePrise","dernierRapportReference_rapport","dernierRapportReference_typeRapport","dernierRapportReference_indicateurTendance","dernierRapportReference_permutation","dernierRapportReference_favoris","dernierRapportReference_grossePrise","eleveur","allure","avisEntraineur"]


'''
    GET RACE DATA
'''
def get_race_data(date):
    url = f"https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{date}?meteo=true&specialisation=INTERNET"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.content)["programme"]
        return data
    else:
        print(f"Error fetching data for date {date}: {response.status_code}")
        return None
    
def get_rapport_data(d,r,c):
    url = f'https://online.turfinfo.api.pmu.fr/rest/client/62/programme/{d}/R{r}/C{c}/rapports-definitifs?specialisation=INTERNET&combinaisonEnTableau=true'
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        print(f"Error fetching data for date {d}R{r}C{c}: {response.status_code}")
        return None
    
'''
    GET PARTICIPANTS DATA
'''
def get_participants_data(course, date):
    url = f"https://online.turfinfo.api.pmu.fr/rest/client/62/programme/{date}/R{course['cr_numReunion']}/C{course['cr_numOrdre']}/participants?specialisation=INTERNET"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.content)
        return data.get('participants')
    else:
        print(f"Error fetching data for date {date}: {response.status_code}")
        return None

'''
PROCESS PARTICIPANTS DATA
'''
def process_participants_data(race, participants,datas):
    flatted = []
    for p in participants:
        pf = flatdict.FlatDict({'ch':p}, delimiter="_")
        flatted.append(pf)
        # init à vide les nouvelles clés
        n = len(list(datas.items())[0][1])
        for kc, vc in pf.items():
            if kc not in datas:
                datas[kc] = [None for i in range(n)]
    # pour chaque participant, ajoute à datas les valeurs pour le participant et la course
    for p in flatted :
        for k,v in datas.items():
            if k.startswith('cr_'):
               v.append(race.get(k, None)) 
            if k.startswith('ch_'):
                v.append(p.get(k, None))

'''
PROCESS PROGRAMME DATA :
'''   
def process_programme_data(programme, date, datas):
    for reunion in programme["reunions"]:
        flatraces = []
        flatmeteo = {}
        # il n'y a des données météo que au niveau réunion
        # on utilise FlatDict pour avoir un dict avec un seul niveau de profondeur
        if "meteo" in reunion :
            # en passant à FlatDict un dict à une clé "cr" et toute les données dedans, 
            # ça rajoute automatiquement cr_ devant toutes les clés "brutes"
            flatmeteo = flatdict.FlatDict({'cr':reunion["meteo"]}, delimiter="_")
        for course in reunion["courses"]:
            if course["discipline"] == 'ATTELE' :
                # on utilise FlatDict pour avoir un dict avec un seul niveau de profondeur
                cf = flatdict.FlatDict({'cr':course}, delimiter="_")
                # on ajoute les données météo de la réunion a chaque courses
                cf = dict(cf, **flatmeteo);
                flatraces.append(cf)
                # ici c'est pour traiter le cas où on découvre une nouvelle clé, il faut remplir les données
                # de cette clé pour les entrées précédentes pour qu'à la fin chaque clé à le même nombre de valeurs
                if datas :
                    n = len(list(datas.items())[0][1])
                else:
                    n=0
                # n est le nombre d'entrée précédente
                for kr, vr in cf.items():
                    # si la clé n'était pas dans les données, on commence par la créé a vide pour chaque course précédente
                    if kr not in datas:
                        datas[kr] = [None for i in range(n)]
        # 
        for c in flatraces:
            participants = get_participants_data(c, date)
            if participants:
                process_participants_data(c, participants,datas)
                

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def scrap_result_year(y):
    # Iterate over dates from 01012014 to 06062024
    start_time = time.time()
    start_date = datetime(y, 1, 1)
    end_date = datetime(y+1, 1, 1)

    filename = f'pmu{y}'

    datas = {}
    chunk = 100
    c_chunk = 0
    n_chunk = 0

    for date in daterange(start_date, end_date):
        c_chunk += 1
        date_str = date.strftime("%d%m%Y")
        print(date_str)
        race_data = get_race_data(date_str)
        if race_data:
            process_programme_data(race_data, date_str, datas)
        if c_chunk > chunk and datas :
            n_chunk += 1
            # DEBUG : pour verifier que chaque clé à le bon nombre de valeur
            for k,v in datas.items():
                print(k + ' : ' + str(len(v)))
            df = pd.DataFrame(datas)
            df.to_csv(f'./data/{filename}_{n_chunk}.csv', index=False)
            datas = {}
            c_chunk = 0
            df = None


    df = pd.DataFrame(datas)
    df.to_csv(f'./data/{filename}_{n_chunk+1}.csv', index=False)

    dfs = []
    for nc in range(n_chunk+1):
        dfs.append(pd.read_csv(f'./data/{filename}_{nc+1}.csv'))
    df = pd.concat(dfs)

    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    df.to_csv(f'./data/{filename}.csv', index=False)


def scrap_rapport(file):
    df=pd.read_csv(f'./data/{file}.csv')
    
    crs = df.aid_cr.unique()
    datas = {}
    for cr in crs:
        if datas :
            n = len(list(datas.items())[0][1])
        else:
            datas['aid_cr'] = []
            n=0
        datas['aid_cr'].append(cr)
        print(cr)
        dt = f'{cr[4:6]}{cr[2:4]}20{cr[0:2]}'
        donnee = get_rapport_data(dt,int(cr[7:9]),int(cr[10:12]))
        row = {}
        for d in donnee:
            for i,rp in enumerate(d['rapports']):
                kr = f"{d['typePari']}_{i}_combinaison"
                if kr not in datas:
                    datas[kr] = [None for i in range(n)]
                row[kr]=rp['combinaison']
                
                kr = f"{d['typePari']}_{i}_libelle"
                if kr not in datas:
                    datas[kr] = [None for i in range(n)]
                row[kr]=rp['libelle']
                
                kr = f"{d['typePari']}_{i}_dividende"
                if kr not in datas:
                    datas[kr] = [None for i in range(n)]
                row[kr]=float(rp['dividendePourUnEuro'])/100
        
        for k,v in datas.items():
            if k != 'aid_cr' :
                datas[k].append(row.get(k, None))

    rap = pd.DataFrame(datas)
    rap.to_csv(f'./data/{file}_rap.csv', index=False)

#scrap_rapport('pmu2016cc_os')
scrap_result_year(2017)
