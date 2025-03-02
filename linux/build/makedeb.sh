#!/bin/bash
#yum install dpkg
cd "$(dirname "$0")"
set -x 
RELEASE=$1
PLATFORM=$2
BRANCH=$3
INPUT=../$PLATFORM
VERSION=$(cat ../../VERSION${BRANCH}.md)
DEPLOY=../../deploy
NAME="entermediadb${BRANCH}-${VERSION}-${RELEASE}"
DOWNLOAD=
TMPDEST=$DEPLOY/$NAME
REPO=/home/ec2-user/workspace/drive/emdev/repo
rm -rf $DEPLOY

mkdir -p $DEPLOY/$NAME
cp -rp ../usr $DEPLOY/$NAME
cp -rp ../debian/DEBIAN $DEPLOY/$NAME

#Download war
if [[ "$BRANCH" == "_dev" ]] ; then
	DOWNLOAD="dev_"
elif [[ "$BRANCH" == "_em9" ]] ; then
	DOWNLOAD="em9_"
elif [[ "$BRANCH" == "_em9dev" ]] ; then
	DOWNLOAD="em9dev_"
fi

# qt-faststart comes with libav-tools
# cp -rp ../$PLATFORM/qt-faststart ${TMPDEST}/usr/bin

wget  -N  http://dev.entermediadb.org/jenkins/job/${DOWNLOAD}demoall/lastSuccessfulBuild/artifact/deploy/ROOT.war -O /tmp/ROOT.WAR >/dev/null 2>&1


mkdir -p ${TMPDEST}/usr/share/entermediadb/webapp
unzip  /tmp/ROOT.WAR -d ${TMPDEST}/usr/share/entermediadb/webapp > /dev/null
chmod 755 ${TMPDEST}/usr/share/entermediadb/webapp/WEB-INF/bin/linux/exiftoolthumb.sh


sed "s/{{RELEASE}}/${RELEASE}/g;s/{{VERSION}}/${VERSION}/g;" $INPUT/DEBIAN/control.template >$DEPLOY/$NAME/DEBIAN/control

dpkg --build ${TMPDEST}

cd ../../deploy

#cp ${NAME}.deb $REPO/apt/pool/main/${NAME}_i386.deb
#cp ${NAME}.deb $REPO/apt/pool/main/${NAME}_amd64.deb

# all is all you need
cp ${NAME}.deb $REPO/apt/pool/main/${NAME}_all.deb

#Upload it to repo
bash /home/ec2-user/workspace/drive/emdev/repo/makeapt.sh
#/home/ec2-user/workspace/insync-portable/insync-portable force_sync $REPO/apt
