#!/bin/sh
apt  install -y jq
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('sha384', 'composer-setup.php') === 'e21205b207c3ff031906575712edab6f13eb0b361f2085f1f1237b7126d785e826a450292b6cfd1d64d92e6563bbde02') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
mv composer.phar /usr/local/bin/composer

wget https://github.com/clue/phar-composer/releases/download/v1.4.0/phar-composer-1.4.0.phar
chmod 755 phar-composer-1.4.0.phar
mv phar-composer-1.4.0.phar /usr/bin/phar-composer.phar

composer require --dev designsecurity/progpilot
