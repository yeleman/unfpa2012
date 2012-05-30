Deployment Installation
-----------------------

 Get Source Code
    mkdir -p ~/src
    mkdir -p ~/src/envs
    vim -v .bashrc
    Add to end of file:
        export WORKON_HOME=~/src/envs
        source /usr/local/bin/virtualenvwrapper.sh
    logout / login
    mkvirtualenv --system-site-packages unfpa
    sudo apt-get install libmysqlclient-dev
    pip install -r pip_requirements.txt

* Clone projet    
    git clone git://github.com/yeleman/bolibana.git
    git clone git@github.com:yeleman/unfpa2012.git

* Creation du lien symbolique dans le site-packages
    ln -s path/bolibana .

* Create MySQL DB and User
	sudo apt-get install mysql-client-core-5.5 mysql-server

* Pour la base donnée du site
	echo "grant all privileges on unfpa.* to 'unfpa'@'localhost' identified by 'unfpa' with grant option; flush privileges; create database unfpa;" | mysql -uroot -p

* Pour la base de donnée de nosmsd
	echo "grant all privileges on unfpasms.* to 'unfpasms'@'localhost' identified by 'unfpasms' with grant option; flush privileges; create database unfpasms;" | mysql -uroot -p

* Pour la creation des table
	mysql -uunfpasms -punfpasms unfpasms < ~/src/envs/unfpa/lib/python2.7/site-packages/nosmsd/contrib/nosmsd-gammu-full.sql

cp settings_local.py.example settings_local.py
cp nosmsd.conf.py.exemple nosmsd.conf.py

* Syncdb
	./manage.py syncdb
	./manage.py migrate

* Importer les fixtures
	./manage.py loaddata fixtures/site.json
	./manage.py loaddata fixtures/entity_type.json
	./manage.py loaddata fixtures/roles.json
	./manage.py loaddata fixtures/permission.json
	./manage.py loaddata fixtures/default_access.json
	./manage.py loaddata fixtures_test/Period.json

* Importer les fixtures de test 
	./manage.py loaddata fixtures_test/*.json

* tester les fixtures
	./manage.py fix_fixtures

* Creation du super user
	./manage.py createsuperuser




