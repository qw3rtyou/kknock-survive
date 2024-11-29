FROM php:8.2-apache

COPY php.ini /usr/local/etc/php/

COPY src /var/www/html/

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 775 /var/www/html

