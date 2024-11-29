FROM php:7.4-apache

COPY src /var/www/html/

COPY flag /flag

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 775 /var/www/html

