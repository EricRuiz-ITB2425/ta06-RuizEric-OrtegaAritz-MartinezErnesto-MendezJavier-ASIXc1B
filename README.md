# ta06-RuizEric-OrtegaAritz-MartinezErnesto-MendezJavier-ASIXc1B


## Tasca nº1
> _Resum de la tasca:_ Hem d'aconseguir l'API-Key de la AEMET. descarregar el fitxer de la AEMET i aconseguir pujar al github la carpeta de les dades per poder treballar.


#### Procés d'Obtenció de l'API-Key
- Primer per aconseguir la key, hem anat a la web de la [AEMET](https://opendata.aemet.es/centrodedescargas/inicio).
- ![](./assets/img/APIKEY1.png)
- Després, a l'apartat _"Obtenció de l'API Key"_, li donem a sol·licitar, posem el correu, comprovem que no som un robot i li donem a sol·licitar.
- Aleshores, reps un correu amb la confirmació i et donaran la key.
- ![](./assets/img/APIKEY2.png)


#### Procés de l'Obtenció dels fitxers
- Un cop tens l'API-Key, tornes a l'inici, i entres a l'apartat _"Accés General"_.
- ![](./assets/img/METEO1.png)
- Dins, enganxes l'API-Key a l'apartat i a _"Cercar"_ cerques per _"Segle"_.
- ![](./assets/img/METEO2.png)
- Selecciona un període _"Diari"_ i li donem a _"Disponible a la web"_.
- ![](./assets/img/METEO3.png)
- Els filtres que hem utilitzat per trobar el fitxer han estat els següents:

  - **Metodo:** Regresión Rejilla
  - **Modelo:** MIROC5
  - **Escenarios:** RCP6.0
  - **Variable:** Precipitación
  - **Periodo:** 2006-2100

![](./assets/img/METEO4.png)



Un cop tinguem aquests filtres seleccionats, li donem a cercar, i descarreguem l'únic arxiu disponible.



## Tasca nº2 
> _Resum de la tasca:_ Organitzar, Analitzar i Processar les dades per fer el codi.

Per organitzar i separar els diferents passos (Revisar capçaleres, Verificar arxius, Netejar dades, documentar) hem creat diferents scripts. **(pas1.py | pas2.py | pas3.py | pas4.py)** per després ajuntar-ho tot en un mateix script (main.py):

### PAS 1: Revisar capçaleres i altres dades. _(pas1.py)_

### PAS 2: Verificar els arxius _(pas2.py)_

### PAS 3: Netejar les dades i control d'errors _(pas3.py)_

### PAS 4: Documentació | Logging _(pas4.py)_

## Tasca nº3 
> _Resum de la tasca:_ Generació de resultats (resums estadístics, gràfics i .CSV)

aaaaa
## Tasca nº4 
> _Resum de la tasca:_ Creació i publicació de la web

aaaaa
## Tasca nº5 
> _Resum de la tasca:_ Reflexió sobre el treball dels nostres companys


aaaaa
