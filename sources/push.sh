#!/bin/bash

DIR=$(dirname $(readlink -f $0))
echo $DIR

git config --global user.name "Administrator"
git config --global user.email "admin@example.com"

#remove old version
rm -r -f $DIR/temp-repo
#create new repository

mkdir temp-repo

pushd $DIR/temp-repo
git init
popd

echo "Path  of the repo"
#read repoPath
repoPath= "~/Documents/CT_DOCKEEN-eden_offline"

echo "Project name"
#read projectName
projectName= "CT_DOCKEEN-eden_offline"

echo "Branch name"
#read branchName
branchName= "master"


pushd $repoPath
git remote add origin2 $DIR/temp-repo/
git push -u origin2 $branchName
git remote rm origin2
popd

pushd $DIR/temp-repo
git checkout $branchName
popd

pushd $repoPath
git commit --dry-run --short > $DIR/files.txt
popd

python3 cp-file.py


pushd $DIR/temp-repo/
git remote rm origin
git remote add origin http://172.19.0.4/root/$projectName.git
git add .
git commit -m "New version test"
git push -u origin $branchName
popd




