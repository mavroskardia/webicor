FROM dock0/arch

RUN pacman -Syuq --noconfirm && \
	pacman -Sq nginx python2-pip npm --noconfirm && \
	rm -f /etc/nginx/nginx.conf && \
	npm install -g bower
