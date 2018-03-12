### Requirements

```
Ubuntu 14.04+
Python 3.5
Django 1.9.7
```


### Installation

1. Checkout latest version

    ```
    git clone https://github.com/creativvn/shinobi_core.git
    ```
2.  Install packages

    ```
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
    echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org
    sudo apt-get install mysql-server
    sudo mysql_secure_installation
    sudo mysql_install_db
    sudo apt-get install mysql-client
    apt-get install python
    apt-get install python3-dev
    apt-get install python-mysqldb python-dev python-matplotlib python3-tk
    apt-get install python-pip
    apt-get install python-mysqldb
    apt-get install libsox-dev libmysqlclient-dev libsqlite3-dev
    apt-get install libcurl4-openssl-dev libxslt1-dev libxslt1-dev
    apt-get install python-dev libssl-dev libffi-dev
    apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev
    apt-get install memcached
    service memcached restart
    sudo easy_install greenlet
    sudo service mongod start
    ```

3. Install all dependencies:

    ```
    cd /src
    pip install virtualenv
    virtualenv --python=/usr/bin/python3 ENV
    source ENV/bin/activate
    pip3 install -r ../requirements.txt
    pip3 install git+https://github.com/MongoEngine/django-mongoengine.git
    deactivate
    ```

4. Database

    ```
  CREATE SCHEMA db_shinobi DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;

    ```

5. Init config & database

    ```
    mkdir /etc/shinobi_core
    cp /shinobi_core/settings/local.sample.env /etc/shinobi_core/config.env
    cd /src
    source ../ENV/bin/activate
    python manage.py migrate
    cd import/
    python3 import.py 1000 jsonfile/practiced_list.json test_database practiced_list -v
    ```


### More info

    - [Django edge](http://django-edge.readthedocs.org/en/latest/)
    # API

    ## Status and error code
    Please refer this link [Django rest framework status](http://www.django-rest-framework.org/api-guide/status-codes/)
    to see more about status code.

    Sample of create new migration

    python manage.py makemigrations <app_name> --empty --name=<migrate_name>

    python manage.py migrate --fake <app_name> <migration_name>
    python manage.py migrate <app_name>  <migration_name>
    python manage.py migrate --fake <app_name> 

    ## Route and end point
    [SimpleRouter](http://www.django-rest-framework.org/api-guide/routers/#simplerouter)
    7: Jenkins

        ```
        /home/jenkins/salt-call.sh "salt  'dev-api*' state.sls sourcecode.updatecode"
        /home/jenkins/salt-call.sh "salt  'dev-api*' state.sls sourcecode.dev-build"

        184.72.86.160 build.smartoffice.vn
        http://build.smartoffice.vn:8080/
        user: vmsuser
        pass: vmsRocks!
        ```

    8: GENERATE API DOCS

        Install
        ```
        npm install -g apidoc
        ```

        Run
        ```
        cd ~/vms_code
        apidoc -i src/vms_api/views/ -o src/docs/
        ```

        Document
        ```
        http://apidocjs.com/index.html#params
        ```
