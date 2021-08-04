#!/bin/bash

DIR=$(dirname $(readlink -f $0))
echo $DIR

quit=0
while ((quit!=1));do
	PS3='Please enter your choice: '
	options=("Create Gitlab project" "Push local project" "Delete Gitlab project" "Create Jenkins project" "Delete Jenkins project" "Build Jenkins job" "Configure" "Quit")
	select opt in "${options[@]}"

	do
	    case $opt in
		"Create Gitlab project")
		    echo "Create Gitlab project"
		    echo "Gitlab project name : "
		    read projectName
		    docker exec -i api-server python3 /sources/remote.py -g $projectName master
		    echo "Project created! Go to http://172.19.0.4/"
		    break
		    ;;
		"Push local project")
		    echo "Push local project"
		    echo "Gitlab project path : "
		    read projectPath
		    
		    echo "Project pushed! Go to http://172.19.0.4/"
		    break
		    ;;
		"Delete Gitlab project")
		    echo "Delete Gitlab project"
		    echo "Gitlab project name : "
		    read projectName
		    docker exec -i api-server python3 /sources/remote.py --delete-gitlab $projectName master
		    echo "Project deleted!"
		    break
		    ;;
		"Create Jenkins project")
		    echo "Create Jenkins project"
		    echo "Gitlab project name to construct on Jenkins: "
		    read projectName
		    docker exec -i api-server python3 /sources/remote.py -j $projectName master
		    break
		    ;;
		"Delete Jenkins project")
		    echo "Delete Jenkins project"
		    echo "Jenkins project name : "
		    read projectName
		    docker exec -i api-server python3 /sources/remote.py --delete-jenkins $projectName master
		    break
		    ;;
		"Build Jenkins job")
		    echo "Build Jenkins job"
		    echo "Jenkins project name : "
		    read projectName
		    echo "Jenkins branch name : "
		    read branchName
		    docker exec -i api-server python3 /sources/remote.py -b $projectName $branchName
		    break
		    ;;
		"Configure")
		    echo "Configure"
		    pushd sources
		    python3 config.py
		    popd
		    break
		    ;;
		"Quit")
		    ((quit+=1))
		    break
		    ;;
		*) echo "invalid option $REPLY";;
	    esac
	done
done	
	

