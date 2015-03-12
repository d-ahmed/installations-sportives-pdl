# Installations Sportives des Pays de la Loire

L'objectif est de développer une application manipulants des données relatives aux installations sportives de la région Pays de la Loire.

Les données sont issues de [http://data.paysdelaloire.fr](http://data.paysdelaloire.fr). 

Trois jeux de données sont à récupérer, au format CSV : 

* [Installations](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-fiches-installations)
* [Equipements](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-fiches-equipements)
* [Activités](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-activites-des-fiches-equ)

Toutes les colonnes des fichiers CSV ne vont pas forcément nous intéresser. N'utilisez que celle que vous trouvez intéressantes ! Par exemple pour les installations, l'adresse et les coordonnées GPS sont des données facilement exploitables (affichage sur une Google Map par exemple).

Des liens existent entre les trois jeux de données : 

* une installation possède un ou plusieurs équipements
* une ou plusieurs activités peuvent être pratiquées sur un équipement donné.

![installation_equpement_activite](http://yuml.me/5f867513)

## Architecture

L'application est composée de plusieurs composants ayant chacun un rôle bien défini.

* Le composant `Admin` a pour rôle la création des tables de la base de données.
* Le composant `Import` a pour rôle le remplissage des tables de la base de données à partir des fichiers CSV.
* Le composant `Service` a pour rôle d'exposer les fonctionnalités de l'application, au travers de services REST.
* Le composant `Application web` est destinée aux internautes et a pour rôle de proposer les fonctionnalités de l'application au travers de pages web.

![architecture.png](images/architecture.png)


## Base de données

### Schéma de la base de données

Par rapport au modèle UML présenté précédemment, un des schémas possibles pour la base de données est le suivant : 

![database_model.png](images/database_model.png)

### Exemple de requête

Imaginons la quesiton suivante : "Je souhaite faire du Football dans la ville de Carquefou".

Voici une requête SQL permettant de répondre à cette question, basée sur le schéma précédent : 

```python
SELECT i.numero, i.nom, e.numero, e.nom, a.numero, a.nom
	FROM INSTALLATION i
		JOIN EQUIPEMENT e ON i.numero = e.numero_installation
		JOIN EQUIPEMENT_ACTIVITE ea ON e.numero = ea.numero_equipement
		JOIN ACTIVITE a ON ea.numero_activite = a.numero
	WHERE i.ville = 'Carquefou'
		AND a.nom LIKE '%Football%'
```

Remarques : 

* Attention à la casse ! Il est surement plus prudent de systématiquement comparer les données avec la même casse, en minuscules par exemple. En SQLite cela donnerait : `WHERE LOWER(i.ville) = carquefou'`
* La clause `a.nom LIKE '%Football%'` n'est pas performante ! Mais comme nous n'avons pas beaucoup de données cela n'est pas très important. Dans la vraie vie cela serait à proscrire !

## Quelques exemples de code

### Lecture des données depuis les fichiers CSV

Créez un ensemble de classes permettant de modéliser les concepts liés aux installations sportives. Par exemple : 

```python
class Installation:
	def __init__(self, numero, nom):
		self.numero = numero
		self.nom = nom

	def __repr__(self):
		return "{} - {}".format(self.numero, self.nom)
```

Vous pouvez ensuite créer des instances de ces classes, à partir des données issues des fichiers CSV. Par exemple : 

```python
import csv

with open('installations.csv', 'rt') as csvfile:
	installationsReader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in installationsReader:	
		inst = Installation(row[1], row[0])
		print(inst)

csvfile.close()
```

### Ecriture des données dans une base de données relationnelle

Pour pouvoir démarrer rapidement, vous pouvez utiliser la base de données embarquée [SQLite](https://docs.python.org/3/library/sqlite3.html)

Créez un script permettant d'initialiser la base de données : 

```python
import sqlite3

conn = sqlite3.connect('installations.db')

c = conn.cursor()

c.execute("DROP TABLE IF EXISTS installations")
c.execute('''CREATE TABLE installations
             (numero integer, nom text)''')

conn.commit()
conn.close()
```

Vous pouvez ensuite écrire et lire des données :

```python
import sqlite3

conn = sqlite3.connect('installations.db')

c = conn.cursor()

c.execute('''INSERT INTO installations 
	VALUES (721740002, 'Terrain de Pétanque')''')
c.execute('''INSERT INTO installations 
	VALUES (721750009, 'Ecole Publique')''')

conn.commit()

for row in c.execute('SELECT * FROM installations ORDER BY nom'):
	print(row)

conn.close()
```

L'objectif est d'insérer les données provenant des fichiers CSV.


### Exposition d'un service REST

La librairie [Bottle](http://bottlepy.org/) permet de créer facilement des services REST.

Pour faire un premier test, téléchargez le fichier `bottle.py` et placez le dans un dossier `libs` de votre projet (le dossier `libs` doit contenir un fichier vide nommé `__init__.py`).

Lien vers la version 0.12.8 : [https://raw.githubusercontent.com/bottlepy/bottle/0.12.8/bottle.py](https://raw.githubusercontent.com/bottlepy/bottle/0.12.8/bottle.py)

Voici le code permettant de faire le classique Hello World (fichier `rest-example.py`	) : 

```python
from libs.bottle import route, template, run

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
```

Lancez ensuite le programme : 

	$> python3 rest-example.py
	Bottle v0.12.8 server starting up (using WSGIRefServer())...
	Listening on http://localhost:8080/
	Hit Ctrl-C to quit.

Vous pouvez vérifier que tout va bien :

* soit via la commande `curl` : `curl -XGET http://localhost:8080/hello/world`
* soit directement dans un navigateur : http://localhost:8080/hello/world


## Quelques conseils pour le développement

### Python

Le langage de programmation utilisé est [Python](https://www.python.org), en version 3.

Si vous souhaitez apprendre les bases du langage, rendez-vous sur le site [Open Classrooms](http://openclassrooms.com/courses/apprenez-a-programmer-en-python) !

### Organisation du code

Ne mettez pas tout votre code dans le même fichier !

Utilisez la notion de [module](https://docs.python.org/3/tutorial/modules.html) pour organiser votre code correctement. Par exemple : 

* un package `model` pour les différentes classes de votre modèle de données (un module par classe).
* un package `services` pour les traitements de votre application (un module par service).

### Tests unitaires

Pensez à tester votre code !

Python propose plusieurs modules de tests unitaires : 

* [unittest](https://docs.python.org/3/library/unittest.html)
* [doctest](https://docs.python.org/3/library/doctest.html#module-doctest)

Vous pouvez par exemple commencer avec unittest en suivant [le tutoriel correspondant sur Open Classrooms](http://openclassrooms.com/courses/apprenez-a-programmer-en-python/les-tests-unitaires-avec-unittest).

### Documentation

Pensez à documenter votre code !

Python propose la notion de [docstrings](https://docs.python.org/3/tutorial/controlflow.html#documentation-strings) pour documenter votre code. Exemple : 

```python
def ma_fonction(x, y):
    """
        Ceci est la documentation de ma fonction
    """
    return ...
```
