
#!/bin/bash
# Shell script to install deb package dependencies as well as python package
# dependencies for dataservice.

# if any proxy server
#PROXY=""
# file to store the generated password
DB_PASS_FILE="db_pass.txt"

if [[ `id -u` -ne 0 ]]; then
  echo "You have to execute this script as super user!"
  exit 1;
fi

# Update the packages
echo "Updating package cache.."
apt-get -y update
if [[ $? -ne 0 ]]; then
  echo "Updating package cache failed!"
  exit 1;
fi

echo "Installing MySQL database.."
if [ ! -f $DB_PASS_FILE ]; then
  # generate a random password for the database and store it in the $DB_PASS_FILE
  # file
#  DBPASS=$(date +%s | sha256sum | head -c 32)
  DBPASS="root"
  echo $DBPASS > $DB_PASS_FILE
fi

# Install MySQL Server in a Non-Interactive mode.
echo "mysql-server mysql-server/root_password password $DBPASS" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password $DBPASS" | sudo debconf-set-selections
apt-get install -y mysql-server
if [[ $? -ne 0 ]]; then
  echo "FATAL: MySQL installation failed!"
  exit 1;
fi

# Install pre-requsite dependencies: python-dev, mysqld-dev, setuptools,
# apache, mod_wsgi etc.
echo "Installing pre-requisite dependencies.."
apt-get install -y python-dev libmysqld-dev python-setuptools apache2 libapache2-mod-wsgi
if [[ $? -ne 0 ]]; then
  echo "FATAL: Installing pre-requisite dependencies failed!"
  exit 1;
fi

echo "Enabling the mod WSGI on apache"
a2enmod wsgi
if [[ $? -ne 0 ]]; then
  echo "FATAL: Unable to enable mod wsgi!"
  exit 1;
fi

# Installing python dependencies
echo "Installing dependencies.."
#export http_proxy=$PROXY
#export https_proxy=$PROXY
#python setup.py install
pip install Flask Flask-SQLAlchemy oursql requests flask-cors flask-testing
if [[ $? -ne 0 ]]; then
  echo "FATAL: Installation failed!"
  exit 1;
fi

exit 0
