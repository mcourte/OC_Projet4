# Application pour gérer les tournois d'Echecs 

## Etape 1 : Télécharger le code

Cliquer sur le bouton vert "<> Code" puis sur Download ZIP.  
Extraire l'ensemble des éléments dans le dossier dans lequel vous voulez stockez les datas qui seront téléchargées.  

## Etape 2 : Installer Python et ouvrir le terminal de commande

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

Ouvrir le terminal de commande :  
Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

## Etape 3 : Création de l'environnement virtuel

Se placer dans le dossier où l'on a extrait l'ensemble des documents grâce à la commande ``cd``  
Exemple :
```
cd home/magali/OpenClassrooms/Formation/Projet_4
```


Dans le terminal de commande, executer la commande suivante :
```
python3 -m venv env
```


Activez l'environnement virtuel
```
source env/bin/activate
```
> Pour les utilisateurs de Windows, la commande est la suivante : 
> ``` env\Scripts\activate.bat ```

## Etape 4 : Télécharger les packages nécessaires au bon fonctionnement du programme

Dans le terminal, taper la commande suivante :
```
pip install -r requierements.txt
```

## Etape 5 : Lancer le programme

Taper la commande suivante :
```
python3 main.py
```

## Etape 6 : Utilisation du programme

Pour comprendre le fonctionnement du programme et savoir comment l'utiliser , le document " Utilisation " est à votre disposition.

## Etape 7 : Vérification Flake8

Dans le terminal, taper la commande suivante :
```
flake8 --format=html --htmldir=flake-report
```

