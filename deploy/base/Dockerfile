FROM dock0/arch

RUN pacman -S --needed archlinux-keyring --noconfirm && \
	pacman -Syuq --noconfirm && \
	pacman -Sq nginx npm python2-pip --noconfirm && \
	npm install -g bower && \
	rm -f /etc/nginx/nginx.conf
