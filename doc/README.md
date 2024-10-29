# HRAI 3

## SCRAP

enter : **scrap_result_year(y)**, y = une année
loop par jour (date) :
- **get_race_data** : https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{date}
- **process_programme_data** : pour chaque réunion récupère données météo, pour chaque course récupère les données sous forme de dict plat, et appel get_participants_data / process_participants_data
- **get_participants_data** : https://online.turfinfo.api.pmu.fr/rest/client/62/programme/{date}/R{course['cr_numReunion']}/C{course['cr_numOrdre']}/participants?specialisation=INTERNET
- **process_participants_data** : Pour chaque participant, ajoute les données de la participations + celle de la course (qui contienne déjà les données météo de la réunion)
- ecrit le fichier pmu{y}.csv

enter : **scrap_rapport(file)**
- Récupère une liste d'id de course unique à partir du fichier des participations
- pour chaque course
  - extrait les données course / réunion / date de l'id de course
  - appel get_rapport_data :https://online.turfinfo.api.pmu.fr/rest/client/62/programme/{d}/R{r}/C{c}/rapports-definitifs?specialisation=INTERNET&combinaisonEnTableau=true
  - pour chaque type de pari / pour chaque rapport : extrait libellé, combinaison et dividende pour 1 euro
  
## COMBINE

- **clean** : à partir du brut de scrap : met à jor id cr et participation, format date, estPlace, estGagnant, etc...
- **un_vs_un** : combine en 1 vs 1 tout les participants d'une même courses. 

## ELO1

## EVALUATE

