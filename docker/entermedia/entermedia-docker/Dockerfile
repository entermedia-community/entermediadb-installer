FROM centos:latest
MAINTAINER "EnterMedia" <help@entermediadb.org>
COPY resolv.conf /etc/resolv.conf
RUN yum -y install --nogpgcheck wget
RUN /usr/bin/wget -O /etc/yum.repos.d/entermedia.repo http://packages.entermediadb.org/repo/centos/7/x86_64/entermedia.repo
RUN yum -y install entermediadb_em9dev
COPY delegates.xml /etc/ImageMagick6/delegates.xml
RUN ln -s /opt/libreoffice5.0/program/soffice /usr/bin/soffice
RUN  /usr/bin/wget -O /usr/bin/entermediadb-deploy https://raw.githubusercontent.com/entermedia-community/entermediadb-installers/master/linux/usr/bin/entermediadb-deploy?reload=true
RUN chmod 755 /usr/bin/entermediadb-deploy
RUN groupadd -g 1001 entermedia
RUN useradd -ms /bin/bash entermedia -g entermedia -u 1001
COPY ffmpeg /home/entermedia/.ffmpeg
USER entermedia
ENV CLIENT_NAME=entermedia
ENV INSTANCE_PORT=8080
CMD ["/usr/bin/entermediadb-deploy"]
