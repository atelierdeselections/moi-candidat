Moi, candidat
=============

http://nantes.moi-candidat.fr/

Projet réalisé dans le cadre de l'iniciative citoyenne [Atelier des élections](http://atelierdeselections.fr/) le 1er et 2 Février 2014 à Nantes et en cours de développement.

Cette application web utilise la plateforme collaborative [voxe.org](http://voxe.org/).

Instalation
-----------

Lancer depuis le terminal les commandes suivantes :

    git clone git@github.com:atelierdeselections/moi-candidat.git
    cd moi-candidat
    virtualenv virtenv
    source virtenv/bin/activate
    pip install -r requirements.txt
    python moi_candidat/manage.py syncdb --noinput
    python moi_candidat/manage.py runserver

Dans votre navigateur web l'URL http://127.0.0.1:8000/ devrait afficher le front-end du site.

Déploiement
-----------

Pour déployer le code du projet dans un environnement de production il faut faire quelques modifications spécifiques hébergeur.  
Pour faire ces modifications il faut créer un fichier appelé `local_settings.py` dans le même répertoire du fichier `settings.py` (normalement dans `moi_candidat/moi_candidat`), avec le contenu suivante :

```python
DEBUG = False
ALLOWED_HOSTS = ['.mon-domaine.fr']

STATIC_ROOT = '/absolute/path/to/moi_candidat/public/static/'
MEDIA_ROOT = '/absolute/path/to/moi_candidat/public/media/'
MEDIA_URL = '/media/'

# Un exemple de configuration avec PostgreSQL
# Voir https://docs.djangoproject.com/en/1.6/ref/settings/#std:setting-DATABASES
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'mabdd',
         'USER': 'user',
         'PASSWORD': 'pass',
         'HOST': 'localhost',
     }
}

# L'ID de l'election voir http://voxe.org/platform
# Voici l'ID pour les elections de Nantes
VOXE_ELECTION_ID = '5308832950b843643e0000c9'

```

Pour maintenir à jour les données de Voxe.org il faut ajouter une tâche cron avec la commande suivante :

```
0,30 * * * * python moi_candidat/manage.py updatevoxedata
```
