# Installations Sportives des Pays de la Loire

L'objectif est de développer une application manipulants des données relatives aux installations sportives de la région Pays de la Loire.

Les données sont issues de [http://data.paysdelaloire.fr](http://data.paysdelaloire.fr). 

Trois jeux de données sont à récupérer, au format CSV : 

* [Installations](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-fiches-installations)
* [Equipements](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-fiches-equipements)
* [Activités](http://data.paysdelaloire.fr/donnees/detail/equipements-sportifs-espaces-et-sites-de-pratiques-en-pays-de-la-loire-activites-des-fiches-equ)

Le langage de programmation utilisé est [Python](https://www.python.org)

Si vous souhaitez apprendre les bases du langage, rendez-vous sur le site [Open Classrooms](http://openclassrooms.com/courses/apprenez-a-programmer-en-python) !

## Lecture des données depuis les fichiers CSV

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

## Ecriture des données dans une base de données relationnelle

TODO
