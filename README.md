# Installations Sportives des Pays de la Loire

L'objectif est de développer une application manipulants des données relatives aux installations sportives de la région Pays de la Loire.

Les données sont issues de [http://data.paysdelaloire.fr](http://data.paysdelaloire.fr). 

Trois jeux de données sont à récupérer, au format CSV : 

* [Installations](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-fiches-installations)
* [Equipements](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-fiches-equipements)
* [Activités](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-activites-des-fiches-equ)

## Quelques conseils

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

