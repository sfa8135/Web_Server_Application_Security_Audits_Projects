FROM ubuntu:18.04
RUN apt-get update
ENV TZ=America/Rochester
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 php libapache2-mod-php
COPY vuln.php /var/www/html
RUN a2enmod ssl
CMD /etc/init.d/apache2 restart 
RUN openssl req -newkey rsa:3072 -nodes -keyout /etc/apache2/priv.pem -x509 -days 365 -out /etc/apache2/pubcert.pem \
    -subj "/C=US/ST=NY/L=Rochester/O=RIT/OU=IT Department/CN=example.com"
CMD /etc/init.d/apache2 restart
RUN rm /etc/apache2/apache2.conf
RUN rm /etc/apache2/conf-enabled/security.conf
COPY apache2.conf /etc/apache2
COPY security.conf /etc/apache2/conf-enabled
COPY mysite.conf /etc/apache2/sites-enabled
CMD /etc/init.d/apache2 start && tail -f /dev/null


EXPOSE 80
EXPOSE 443
