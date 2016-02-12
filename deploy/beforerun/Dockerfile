FROM webicorbase

ADD webicor.gz /srv/webicor
ADD nginx.conf /etc/nginx/nginx.conf
ADD requirements.txt /srv/requirements.txt
ADD start.sh /srv/start.sh
ADD local_settings.py /srv/webicor/local_settings.py

WORKDIR /srv

RUN /usr/bin/pip2 install -r requirements.txt

WORKDIR /srv/webicor/webicor

RUN /usr/bin/python2 manage.py collectstatic --noinput

CMD ["/bin/bash", "/srv/start.sh"]
