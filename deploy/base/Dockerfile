FROM dock0/arch

RUN pacman -Syuq --noconfirm && \
	pacman -Sq nginx python2-pip --noconfirm && \
	rm -f /etc/nginx/nginx.conf

