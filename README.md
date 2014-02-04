Moi, candidat
=============

http://moi-candidat.atelierdeselections.fr/

Projet réalisé dans le cadre de l'iniciative citoyenne [Atelier des élections](http://atelierdeselections.fr/) le 1er et 2 Février 2014 à Nantes et en cours de développement.

Instalation
-----------

    $ git clone git@github.com:atelierdeselections/moi-candidat.git
    $ cd moi_candidat
    $ virtualenv virtenv
    $ source virtenv/bin/activate
    $ pip install -r requirements.txt
    $ python moi_candidat/manage.py syncdb  # il faut répondre "yes" à la question du superuser
    $ python moi_candidat/manage.py loaddata sample_data  # load sample data
    $ python moi_candidat/manage.py runserver

Dans votre navigateur web l'URL http://127.0.0.1:8000/ devrait afficher le front-end du site
et http://127.0.0.1:8000/admin/ devrait afficher le back-end.
