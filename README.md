# Application pour gérer les tournois d'Echecs 

***Compétences acquises lors de la réalisation de ce projet:***  
  
*1. Écrire un code Python robuste en utilisant la PEP 8*  
*2. Structurer le code d'un programme Python en utilisant le design pattern Model Controller View*  
*3. Utiliser la programmation orientée objet pour développer un programme Python*  

## But du projet :  

Création d'une application fonctionnement hors-ligne permettant la gestion de tournois d'échecs.  
Création de nouveaux joueurs, de tournois, création de rapports en fin de tournois ... 
  
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
pip install -r requirements.txt
```

## Etape 5 : Lancer le programme

Taper la commande suivante :
```
python3 main.py
```

## Etape 6 : Utilisation du programme

-Commencer par créer des joueurs.  
-Créer un tournoi.  
-Une fois le tournoi crée, vous pouvez "Lancer un tournoi".  
-Si vous souhaitez arrêter de rentrer les scores après un ou plusieurs rounds, vous pourrez reprendre ce tournoi depuis " Reprendre un tournoi"  
-Une fois le tournoi complet, pensez à Clôturer le tournoi.  
-Dans le menu rapport, vous trouverez une liste de rapport que vous pouvez afficher directement dans votre terminal et l'enregistrez en fichier text si vous le souhaitez.  

**Attention** : contrairement aux réelles règles d'un tournoi d'Echecs, ce programme impose un nombre pair de joueur. Dans la réalité, dans le cas avec un nombre de joueur impair, le joueur qui ne joue pas de matchs gagne 1 point.  


## Etape 7 : Vérification Flake8

Dans le terminal, taper la commande suivante :
```
flake8 --output-file=flake8-report/flake8-output.html --exclude=env
```


![Image de l'ensemble des pions d'échecs.](image/pions.jpg)
