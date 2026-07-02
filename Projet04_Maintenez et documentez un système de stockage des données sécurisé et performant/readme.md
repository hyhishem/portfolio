# DataSoluTech: migration des données médicales de patients (V1.3)

## 1. Context et details

Dans la version précédente V0.1, nous avons développé un script permettant de nettoyer un fichier CSV contenant des données médicales. La V0.2 ajoute une étape : la migration des données nettoyées vers une base MongoDB, avec la possibilité de les visualiser dans Mongo Express. Dans la version V0.3 l'ensemble des services sont conteneurisé sans automatisation. 

Cette version comprend :

1. Un fichier docker-compose.yml avec :
- Python,
    - Installe les dépendances
    - Exécute un script pour créer différents utilisateurs Mongo définis via les variables d'environnement. 
- MongoDB, avec un volume persistant pour stocker les données. 
- Mongo Express pour visualiser et administrer les bases MongoDB via une interface web
- Un réseau pour permettre la communication entre les conteneurs.

2. Un script principal utilisant plusieurs fonctions : 
   - Gestion interactive et automatisée des bases de données et collections MongoDB. 
   - Création et gestion des clés pour structurer les documents. 
   - Nettoyage et transformation des données avant insertion pour garantir la cohérence et l'intégrité
   - Insertion manuelle de documents ou migration automatisée depuis des fichiers CSV. 

## 2. Prérequis
Avant de pouvoir utiliser ce projet, assurez-vous d'avoir installé les éléments suivants :

- **Docker** et **Docker Compose** : pour déployer les conteneurs MongoDB, Python et Mongo Express. 
  - [Installer Docker](https://docs.docker.com/desktop/) 
  - [Installer Docker Compose](https://docs.docker.com/compose/install/)

- **Git** : pour cloner le dépôt et gérer les versions. 
  - [Installer Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

## 3. Authentification et rôles 

Trois comptes sont crées :

- admin pour la gestion complète. Mot de passe admin123
- rw pour l'ecriture et la lecture.  Mot de passe rw123
- read en lecture seule. Mot de passe read123

L'acces à Mongo Express est possible sur http://localhost:8081

- Identifiant mongo express: admin
- Mot de passe mongo express: pass


## 4. Installation avec Docker et Docker-compose 

Pour déployer l'environnement complet avec MongoDB, Mongo Express et le conteneur Python : 

 ```bash
 $ docker-compose up -d
 ```
Cette commande :
- Télécharge les images nécessaires (MongoDB, Mongo Express, Python).
- Crée et démarre les conteneurs dans le réseau défini.
- Monte les volumes pour la persistance des données et le partage des scripts et CSV.
- Exécute automatiquement le script Python pour créer les utilisateurs MongoDB et installer les dépendances.

## 5. Utilisation

Avant l'utilisation verifier que les service python et mongo-express sont demarré. Si ce n'est pas le cas utiliser cette commande 

```bash
$ docker start python mongo-express 
```

Ce programme permet d'automatiser la migration depuis un fichier CSV vers MongoDB ou de réaliser des actions CRUD . Les arguments disponible sont :

--csv : chemin vers le fichier CSV.

--db : nom de la base MongoDB.

--collection : nom de la collection cible.

--user / --password : identifiants MongoDB.

--pas_vider_col : optionnelle, vide la collection avant insertion par defaut, ajouter pour ne pas vider la collection.

--crud : Action CRUD: c -Create  r -Read  u -Update ou d -Delete

--nom : Valeur pour la clé Name

--age : Valeur pour la clé Age

--new_nom : Nouvelle valeur pour la clé Name

--new_age : Nouvelle valeur pour la clé Age


#### 5.1. Migration du fichier CSV:

Pour réaliser la migration du fichier dataset.csv vers Mongodb vous pouvez utiliser :

 ```bash
docker exec -it python python3 /app/main_script.py --csv /data/dataset.csv --db health_data --collection patients --user rw  --password rw123
 ```

#### 5.2. Operation CRUD :


 - READ: Recherche du patient "Nom Prenom" dans la collection patients
 
 ```bash
docker exec -it python python3 /app/main_script.py --db health_data --collection patients  --user rw  --password rw123 --crud r --nom "Nom Prenom" 
 ```
 
 - CREATE: Création du patient "Nom Prenom" agé de 38ans
 
 ```bash
docker exec -it python python3 /app/main_script.py --db health_data --collection patients  --user rw  --password rw123 --crud c --nom "Nom Prenom" --age 38
 ```

 - READ: Mise en évidence de la présence du patient "Nom Prenom"  dans la collection patients
 
 ```bash
docker exec -it python python3 /app/main_script.py --db health_data --collection patients  --user rw  --password rw123 --crud r --nom "Nom Prenom" 
 ```


 - Update: Modification de l'age du patient "Nom Prenom" 
 
 ```bash
docker exec -it python python3 /app/main_script.py --db health_data --collection patients  --user rw  --password rw123 --crud u --nom "Nom Prenom" --age 38 --new_age 40
 ```

 - READ: Verification de la modification de l'age du patient "Nom Prenom"  dans la collection patients
 
 ```bash
docker exec -it python python3 /app/main_script.py --db health_data --collection patients  --user rw  --password rw123 --crud r --nom "Nom Prenom" 
 ```

 - DELETE: Suppression du patient "Nom Prenom" 
 
 ```bash
docker exec -it python python3 /app/main_script.py --db health_data --collection patients  --user rw  --password rw123 --crud d --nom "Nom Prenom" 
 ```



