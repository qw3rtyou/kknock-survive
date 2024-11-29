FROM php:7.4-apache

COPY php.ini /usr/local/etc/php/

COPY src /var/www/html/

COPY flag /tmp/

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 775 /var/www/html
