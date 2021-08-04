#!/usr/bin/python3

import os
import argparse
from pathlib import Path
import shutil

def make_parser():
	parser = argparse.ArgumentParser(prog='COMMANDS')
	subparsers = parser.add_subparsers(dest='command', help='sub-command')
	
	
	lparser = subparsers.add_parser('local-push', help = 'Push ST_IntegrationLibrary in Gitlab Local')
	lparser.add_argument('projectName',type=str, help='the name of the project')
	lparser.add_argument('branchName',type=str, help='the name of the branch')
	lparser.add_argument('-p, --project-path', dest = 'project_path', default = '.', required =False, help='Path to the project')
	
	gparser = subparsers.add_parser('delete-gitlab', help = 'Delete Gitlab project')
	gparser.add_argument('projectName',type=str, help='the name of the project')
	
	jparser = subparsers.add_parser('delete-jenkins', help = 'Delete Jenkins project')
	jparser.add_argument('projectName',type=str, help='the name of the project')
	
	rparser = subparsers.add_parser('run', help = 'Run job on Jenkins')
	rparser.add_argument('projectName',type=str, help='the name of the project')
	rparser.add_argument('branchName',type=str, help='the name of the branch')

	uparser = subparsers.add_parser('upload', help = 'Upload Jenkins project from Gitlab')
	uparser.add_argument('projectName',type=str, help='the name of the project')
	
	args = parser.parse_args()
	print(args.command)
	
	if args.command=='delete-gitlab':
		os.system('docker exec -i api-server python3 /sources/remote.py delete-gitlab '+args.projectName)
	if args.command=='delete-jenkins':
		os.system('docker exec -i api-server python3 /sources/remote.py delete-jenkins '+args.projectName)
	if args.command=='run':
		os.system('docker exec -i api-server python3 /sources/remote.py run '+args.projectName+' '+args.branchName)
	if args.command=='upload':
		os.system('docker exec -i api-server python3 /sources/remote.py upload '+args.projectName)




	if args.command=='local-push':
		
		directory = os.getcwd()+'/sources'
		print(directory)
		projectPath= args.project_path
		print(projectPath)
		projectName=args.projectName
		branchName=args.branchName
		
		os.system('git config --global user.name "Administrator"')
		os.system('git config --global user.email "admin@example.com"')

		#remove old version
		os.system('rm -r -f '+directory+'/temp-repo')
		#create new repository

		os.system('mkdir '+directory+'/temp-repo')

		os.system('cd '+directory+'/temp-repo; git init; git checkout -b '+branchName)
		
		os.system('cd '+projectPath+'; git commit --dry-run --short > '+directory+'/files.txt')
		os.system('cp -r '+projectPath+'/* '+directory+'/temp-repo/')

		#copy files 

		list=[]
		file=open("sources/files.txt","r")

		for l in file:
			if l.startswith('?? ')==True:
				#print (l[3:])
				list.append(l[3:-1])

		print (list)

		for i in list:
			os.system('rm -r -f '+directory+'/temp-repo/'+i)		
		
		#push on Gitlab local
		os.system('docker exec -i api-server python3 /sources/remote.py delete-gitlab '+projectName)
		os.system('docker exec -i api-server python3 /sources/remote.py create-gitlab '+projectName)
		
		os.system('cd '+directory+'/temp-repo; git remote rm origin; git remote add origin http://172.19.0.4/root/'+projectName+'.git; git add .; git commit -m "New version test"; git push -u origin '+branchName)

make_parser()

