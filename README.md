Moi, candidat
=============

http://moi-candidat.atelierdeselections.fr/

Projet réalisé dans le cadre de l'iniciative citoyenne "Atelier des élections" le 1er et 2 Février 2014 à Nantes et en cours de développement.


Instalation
-----------


    $ git clone git@github.com:atelierdeselections/profilitique.git
    $ virtualenv virtenv
    $ source virtenv/bin/activate
    $ pip install -r requirements.txt
    $ cd profilitique
    $ python manage.py syncdb
    $ python manage.py runserver

