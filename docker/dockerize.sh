#!/bin/bash -x

# This script takes some precautions under the assumption of a multi-client, multi-catalog data directory (ala Media128)
# NOTE: MUST RUN AS ROOT USER

CLIENT=tejidos
PORT=8589
NODE_ID=${CLIENT}${PORT}
CLUSTER_NAME=$CLIENT-cluster
EMPATH=/opt/entermediadb
# multiple catalogs, space delimited
CATALOGS=tejidos
# Is client equivalent to catalogid?
# May need to just have editable vars
CPATH=/media/clients/$CLIENT
EMDBHOME=/usr/share/entermediadb

# Export databases. Will need to change this to API calls maybe if we really need to automate it.
#for catalog in ${CATALOGS[@]}; do
#  wget -O /dev/null http://media128.com/$catalog/emshare/views/settings/events/triggers/run.html?forcerun=true&runpath=/$catalog/catalog/events/data/exportdatabase.html > /dev/null
#  sleep 10
#done

# Setup
mkdir -p $CPATH
#yum install -y docker
#rsync -azPe 'ssh -i /home/entermedia/.ssh/mediadb.pk' entermedia@mediadb13.entermediadb.net:/home/entermedia/git/entermediadb-installers/docker/firewall.sh .
#bash ./firewall.sh
#service docker restart
#rsync -azPe 'ssh -i /home/entermedia/.ssh/mediadb.pk' entermedia@mediadb13.entermediadb.net:/home/entermedia/git/entermediadb-installers/docker/entermedia . && cd entermedia
#docker build -t entermedia:latest entermedia-docker

# Copy stuff
mkdir -p $CPATH/{webapp/WEB-INF,data}
cp -rp $EMPATH/webapp/{emshare,media,theme,index.*,crossdomain.xml,_site.xconf} $CPATH/webapp/
cp -rp $EMPATH/webapp/WEB-INF/{bin,lib,base,oemounts.xml,web.xml} $CPATH/webapp/WEB-INF/
for catalog in ${CATALOGS[@]}; do
  cp -rp $EMPATH/webapp/$catalog $CPATH/webapp/
  # This will include the latest database dump.
  cp -rp $EMPATH/webapp/WEB-INF/data/{$catalog,system} $CPATH/data/
  #add empty elastic folder
  mkdir ${CPATH}/elastic
done

# Make node/server.xml and port-specific tomcat
TOMCAT=${CPATH}/tomcat${PORT}
mkdir -p $TOMCAT/logs
#cp -rp $EMDBHOME/tomcat/* $TOMCAT/
#sed "s/%PORT%/${INSTANCE_PORT}/g;s/%NODE_ID%/${CLIENT_NAME}${PORT}/g" <"${EMDBHOME}/tomcat/conf/server.xml.cluster" >"${TOMCAT}/conf/server.xml"
#sed "s/%CLUSTER_NAME%/${CLIENT_NAME}-cluster/g" <"${EMDBHOME}/conf/node.xml.cluster" >"${CPATH}/webapp/WEB-INF/node.xml"

# Fix ownership
chown -R entermedia. ${CPATH}

# Run docker container
# Delegates and ffmpeg files are COPY'd in Dockerfile
#        -v ${EMDBHOME}/conf/ffmpeg:/home/entermedia/.ffmpeg \
#        -v ${EMDBHOME}/conf/im/delegates.xml:/etc/ImageMagick-6/delegates.xml \
docker run -d --name ${CLIENT}_entermedia -p $PORT:$PORT \
	-e INSTANCE_PORT=${PORT} \
	-e CLIENT_NAME=${CLIENT} \
        -v ${CPATH}/webapp:/opt/entermediadb/webapp \
        -v ${CPATH}/data:/opt/entermediadb/webapp/WEB-INF/data \
        -v ${TOMCAT}/logs:/opt/entermediadb/tomcat/logs \
        -v ${CPATH}/elastic:/opt/entermediadb/webapp/WEB-INF/elastic \
        entermedia
echo "NOTE: now you need to add an entry for $PORT in /etc/nginx/conf.d/entermedia.conf (or whatever other redirect configuration)"
echo "Then you need to update DNS, if that is appropriate"
