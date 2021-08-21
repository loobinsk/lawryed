https://www.phillymag.com/news/2017/03/16/laura-goldman-stalker-white-house-press-pool/

Accounts and Password:
==============

Domain:
https://ua.godaddy.com/
login: i.makushinsky@gmail.com
password: Pactasuntservanda13

Digital Ocean:
login: i.makushinsky@gmail.com
password: Threedaysgrace12


Server SSH:
ip: 167.99.243.12
login: root
password: Q8gXeY8VuYJ69JGFMfXt


Google Suite (в гсюит должно без домена входить):
https://gsuite.google.com/intl/uk/features/
login: i.makushinsky@lawyerd.net
login: dmca@lawyerd.net
password: Taketheworld97


IP2.UA:
https://2ip.ua/ua/site/authentication
login:
password:
api-key:


==============
Web Site Superuser:
name: admin
email: admin@admin.net
Password:  Taketheworld97



Postgres:
login: postgres
password: 8e8gb8898h89HIUGvuFuu78ytt8t7IHgkg


PgAdmin
http://167.99.243.12:8082/pgadmin4/login?next=%2Fpgadmin4%2F
login: i.makushinsky@lawyerd.net
password: sd9h99HlnIU98867hmLJHHlH98h9


Test google mail
+044 07553 569315 (великобритания)
mmmsvittestmail@gmail.com
fewef34r343g4


Google keys create and manage:
https://linuxhint.com/google_search_api_python/
https://cse.google.com/cse/all
https://support.google.com/customsearch/answer/4513886?hl=en


Work in MS Windows!!!!
celery==4.4.0rc4

In Linux celery must set workdir
/lywerd/lawyerd



psql -c "alter user postgres with password '8e8gb8898h89HIUGvuFuu78ytt8t7IHgkg'"

CREATE DATABASE lawyerd
  WITH ENCODING = 'UTF8'
    TEMPLATE = template0;




CREATE USER lawyerd WITH ENCRYPTED PASSWORD 'MyStr0ngP@SS';


-- create user lawyerd encrypted password '8e8gb8898h89HIUGvuFuu78ytt8t7IHgkg';


sudo -u postgres psql
postgres=# create database mydb;
postgres=# create user myuser with encrypted password 'mypass';
postgres=# grant all privileges on database lawyerd to lawyerd2;



https://github.com/sindresorhus/capture-website-cli

Instal Node.js dependencies
=================
npm install --global capture-website-cli
npm install phantomjs
cd youtube_compliant_bot && npm install
https://phantomjs.org/download.html


extract to /usr/local/bin
https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
set 777 permisions!

export PHANTOMJS_BIN=/home/node_modules/.bin/phantomjs &&  export CELERY_BROKER_URL=redis://localhost:6379/1 && export DJANGO_READ_DOT_ENV_FILE=True && /home/lawyerd/venv/bin/python -m celery -A config.celery_app worker -P solo --loglevel=INFO --workdir /home/lawyerd/lawyerd/

export DJANGO_READ_DOT_ENV_FILE=True && /home/lawyerd/venv/bin/python3.7 /home/lawyerd/manage.py runserver lawyerd.net:8000 --settings=config.settings.local


lawyerd
==============

Autosubcriber html forms

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Сервис предназначен для продуктовых  компаний, которые хотят защитить свою интеллектуальную собственность.


1. Не кирилистические домены наверное придется сранивать както по особеннному
https://www.whois.com/whois/%D0%BA%D1%82%D0%BE.%D1%80%D1%84
https://github.com/ovh/cerberus-core
http://www.dnspython.org/examples.html
https://gist.github.com/amatellanes/a986f6babb9cf8556e36


2. если есть
admin-contact
то это не хостинг походу

3. если нет емейла то нужно вести ручную базу по полю
Registrar

4. жалоба на cloudflare
https://www.cloudflare.com/abuse/form
только вручную


5. сайты не http не могул лежать в cludflare и т.п.
https://whois.arin.net/rest/poc/ABUSE5250-ARIN.html



https://rdap.arin.net/registry/ip/104.27.152.151
https://search.arin.net/rdap/?query=104.27.152.151


# What's the best website screenshot capture free API?
https://www.quora.com/Whats-the-best-website-screenshot-capture-free-API

# Идеи
1. Сделать спец. отправку на CloudFlare, YooTube
https://gist.github.com/amatellanes/a986f6babb9cf8556e36

# Поиск в Google
https://code.google.com/apis/console
https://console.developers.google.com/apis/dashboard
https://cse.google.com/cse/all
завести сайт
включить глобальный поиск через: "Поиск в Интернете"

добавить хорошие сайты в исключения

Интересные ссылки:
http://www.dnspython.org/examples.html
https://github.com/m0rtem/CloudFail
https://github.com/pirate/sites-using-cloudflare

http://www.crimeflare.org:82/cfs.html
http://www.anchous.info/detect-ip-behind-cdn-cloudflare
http://ptrarchive.com/
https://stackoff.ru/nemnogo-o-cloudflare/
https://suip.biz/ru/?act=cloudfail
https://www.remoteshaman.com/news/security/methods-for-bypass-cloudflare-security-to-get-real-ip
https://hackware.ru/?p=5762



Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy lawyerd

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd lawyerd
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.




Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _mailhog: https://github.com/mailhog/MailHog



Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



Dev
---

Docker
---
::

    $ docker-machine create --driver virtualbox default --virtualbox-disk-size "60000" --virtualbox-cpu-count "4"  --virtualbox-memory "6144"




setup
---
::



    $ sudo apt update && sudo apt upgrade -y && sudo apt-get install build-essential checkinstall && sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev libpq-dev pigz redis-server supervisor daemontools nginx gunicorn lynx mc glances htop -y \
    \
     python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip python3.7-dev npm \
	\
apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
&& \
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - \
&& sudo apt-key fingerprint 0EBFCD88 \
&& sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable" \
&& sudo apt-get update \
&& sudo apt-get install docker-ce docker-ce-cli containerd.io




    $ cd /home/ && psql -U postgres lawyerd < auto_new.sql
    $ /home/venv/bin/pip install -r /home/lawyerd/requirements/production.txt
    $ source /home/venv/bin/activate &&  pip install --upgrade pip && pip3.7 install -r /home/lawyerd/requirements/production.txt



    $ systemctl restart supervisor && systemctl status supervisor


https://computingforgeeks.com/how-to-install-pgadmin-4-on-ubuntu/


export PYTHONUNBUFFERED=1,DJANGO_SETTINGS_MODULE="config.settings.production",DATABASE_URL="postgres://postgres:8hg584g8b3b3bf49H9bvbGUIGUIkbev33@localhost:5432/lawyerd", CELERY_BROKER_URL="redis://localhost:6379/0", CELERY_RESULT_BACKEND="redis://localhost:6379/0", USE_DOCKER="False", SENTRY_DSN="https://b566074a8281474abcaeb3bb7fed3143@sentry.io/1519321" && /home/venv/bin/python3.7 /home/lawyerd/manage.py domain_check
export PYTHONUNBUFFERED=1,DJANGO_ALLOWED_HOSTS="188.225.81.176,",DJANGO_SETTINGS_MODULE="config.settings.production",DATABASE_URL="postgres://postgres:8hg584g8b3b3bf49H9bvbGUIGUIkbev33@localhost:5432/lawyerd",CELERY_BROKER_URL="redis://localhost:6379/0",CELERY_RESULT_BACKEND="redis://localhost:6379/0",USE_DOCKER="False",SENTRY_DSN="https://b566074a8281474abcaeb3bb7fed3143@sentry.io/1519321" && /home/venv/bin/python3.7 /home/lawyerd/manage.py runserver 188.225.81.176:8000

export PYTHONUNBUFFERED=1,DJANGO_SETTINGS_MODULE="config.settings.production",DATABASE_URL="postgres://postgres:8hg584g8b3b3bf49H9bvbGUIGUIkbev33@localhost:5432/lawyerd",CELERY_BROKER_URL="redis://localhost:6379/0",CELERY_RESULT_BACKEND="redis://localhost:6379/0",USE_DOCKER="False",SENTRY_DSN="https://b566074a8281474abcaeb3bb7fed3143@sentry.io/1519321" && /home/venv/bin/python3.7 /home/lawyerd/manage.py runserver 188.225.81.176:8000
export DJANGO_READ_DOT_ENV_FILE="True" && /home/venv/bin/python3.7 /home/lawyerd/manage.py runserver 188.225.81.176:8000 --settings=config.settings.production

sudo -u postgres psql -c "CREATE USER autosubscribe WITH SUPERUSER PASSWORD '8hg584g8b3b3bf49H9bvbGUIGUIkbev33';"


ALTER USER lawyerd WITH PASSWORD '8hg584g8b3b3bf49H9bvbGUIGUIkbev33';
ALTER USER lawyerd WITH SUPERUSER;t


ALTER DATABASE lawyerd OWNER TO lawyerd

ALTER USER postgres WITH PASSWORD '8hg584g8b3b3bf49H9bvbGUIGUIkbev33';


sudo -u postgres psql


\c lawyerd


update_in_progress_orders


cd /home/ && (su postgres -c 'pg_dump -U postgres lawyerd --no-owner --clean --create --no-privileges --format=p --if-exists --no-security-labels  --quote-all-identifiers --serializable-deferrable ')  | gzip -c -9 >  lawyerd_backup.sql.gzip
cd /home/ && (su postgres -c 'pg_dump -U postgres lawyerd --no-owner --clean --create --no-privileges --format=p --if-exists --no-security-labels  --quote-all-identifiers --serializable-deferrable ')  | pigz --best -f -m >  lawyerd_backup.sql.gzip



Windows BackUp for Postgres 11.5
h:/pgsql/bin/pg_dump.exe -h localhost -p 5432 -U postgres -F c -E UTF8 -Z 4 -v -f "E:\___backup_autosubscribe\lawyerd_20190824_200445819.dmp" lawyerd




Run:
export DJANGO_READ_DOT_ENV_FILE=True && /home/lawyerd/venv/bin/python3.7 /home/lawyerd/manage.py runserver 167.99.243.12:8000 --settings=config.settings.local
