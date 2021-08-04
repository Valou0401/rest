#!/usr/bin/python3

import json 
import sys
import urllib
import requests
import os
import configparser
import jenkins
import tempfile
import xml.etree.ElementTree as ET
import argparse

# IMPORT CONFIG

config = configparser.ConfigParser()
config.read('/sources/config')
#config.read('config')

class jenkinsConf():

	def getUrl(self):
		return config['JENKINS']['ipv4_jenkins']
		
	def getToken(self):
		return config['JENKINS']['jenkins_api_token']
		
	def getUser(self):
		return config['JENKINS']['jenkins_user']
		
	def getPasswd(self):
		return config['JENKINS']['jenkins_passwd']
		
	def getGitlabName(self):
		return config['JENKINS']['gitlab_server_name_in_jenkins']
		
		

class gitlabConf():

	def getUrl(self):
		return config['GITLAB']['ipv4_gitlab']
		
	def getToken(self):
		return config['GITLAB']['gitlab_api_token']
		
	def getUser(self):
		return config['GITLAB']['gitlab_user']
		
	def getPasswd(self):
		return config['GITLAB']['gitlab_passwd']


# GITLAB

def get_project_id(projectName):
	r = requests.get('http://'+gitlabConf().getUrl()+'/api/v4/projects?name='+projectName, auth=(gitlabConf().getUser(),gitlabConf().getPasswd()), headers={'PRIVATE-TOKEN': gitlabConf().getToken()})
  
	for i in r.json():
		if i['name'] == projectName : 
			id = i['id']
	return id
  

def create_gitlab_project(projectName):
	r = requests.post('http://'+gitlabConf().getUrl()+'/api/v4/projects?name='+projectName+'&visibility=public', auth=(gitlabConf().getUser(),gitlabConf().getPasswd()), headers={'PRIVATE-TOKEN': gitlabConf().getToken()})
	return r.json()	


def delete_gitlab_project(projectName):
	id = get_project_id(projectName)
	r = requests.delete('http://'+gitlabConf().getUrl()+'/api/v4/projects/'+str(id), auth=(gitlabConf().getUser(),gitlabConf().getPasswd()), headers={'PRIVATE-TOKEN': gitlabConf().getToken()})
	return r


#JENKINS

def config_jenkins():
	server = jenkins.Jenkins('http://'+jenkinsConf().getUrl(), username=jenkinsConf().getUser(), password=jenkinsConf().getToken())
	user = server.get_whoami()
	version = server.get_version()
	print('Hello %s from Jenkins %s' % (user['fullName'], version))
	return server
  

def run_jenkins_build(projectName,branchName):
	os.system('curl --request POST -I -u '+jenkinsConf().getUser()+':'+jenkinsConf().getToken()+' http://'+jenkinsConf().getUser()+':'+jenkinsConf().getPasswd()+'@'+jenkinsConf().getUrl()+'/job/'+projectName+'/job/'+branchName+'/build?delay=0sec')
	return 0
  
def delete_jenkins_project(projectName):
	server = config_jenkins()
	if server.get_job_name(projectName)==projectName:
		server.delete_job(projectName)
		print('job removed')
	return 0
  
def create_blank_job(projectName):
	server = config_jenkins()
	if server.get_job_name(projectName)==projectName:
		print('Name already used')
	else:
		server.create_job('test',jenkins.EMPTY_CONFIG_XML)
		print('job created')
	return 0
    

def xml_generator(projectName):
	tree = ET.parse('/sources/xml_config')
	#tree = ET.parse('xml_config')
	root = tree.getroot()
	for i in root.iter('credentialsId'):
		i.text = ('apidentification')
	for i in root.iter('serverName'):
		i.text = (jenkinsConf().getGitlabName())
	for i in root.iter('projectOwner'):
		i.text = (gitlabConf().getUser())
	for i in root.iter('projectPath'):
		i.text = ('root/'+projectName)
	for i in root.iter('sshRemote'):
		i.text = ('git@'+gitlabConf().getUrl()+':root/'+projectName+'.git')
	for i in root.iter('httpRemote'):
		i.text = ('http://'+gitlabConf().getUrl()+'/root/'+projectName+'.git')
	for i in root.iter('projectId'):
		i.text = (str(get_project_id(projectName)))

		
	tree.write(projectName+'_config.xml')
	return 0
	

def create_job(projectName):
	create_credential()
	xml_generator(projectName)
	
	os.system("CRUMB="+"$"+"(curl -s "+"'http://'"+jenkinsConf().getUrl()+"'/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,'+':'+',//crumb)' -u "+jenkinsConf().getUser()+":"+jenkinsConf().getToken()+")")
	os.system("curl -s -XPOST "+"'http://'"+jenkinsConf().getUrl()+"'/createItem?name='"+projectName+" -u "+jenkinsConf().getUser()+":"+jenkinsConf().getToken()+" --data-binary @"+projectName+"_config.xml -H "+"'Content-Type:text/xml'")
	print('Job created')
	os.system('rm '+projectName+'_config.xml')
	return 0


def create_credential():
	os.system("CRUMB="+"$"+"(curl -s "+"'http://'"+jenkinsConf().getUrl()+"'/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,'+':'+',//crumb)' -u "+jenkinsConf().getUser()+":"+jenkinsConf().getToken()+")")
	os.system("curl -s -XPOST \'http://"+jenkinsConf().getUser()+":"+jenkinsConf().getToken()
+"@"+jenkinsConf().getUrl()+"/credentials/store/system/domain/_/createCredentials\' --data-urlencode \'json={\"\": \"0\",\"credentials\": {\"scope\": \"GLOBAL\",\"id\": \"apidentification\",\"username\": \""+gitlabConf().getUser()+"\",\"password\": \""+gitlabConf().getPasswd()+"\",\"description\": \"api credential\",\"$class\": \"com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl\"}}\' ")
	return 0
	


def make_parser():
	parser = argparse.ArgumentParser(prog='COMMANDS')
	subparsers = parser.add_subparsers(dest='command', help='sub-command')
	
	
	lparser = subparsers.add_parser('local-push', help = 'Push ST_IntegrationLibrary in Gitlab Local')
	lparser.add_argument('projectName',type=str, help='the name of the project')
	
	gparser = subparsers.add_parser('delete-gitlab', help = 'Delete Gitlab project')
	gparser.add_argument('projectName',type=str, help='the name of the project')
	
	jparser = subparsers.add_parser('delete-jenkins', help = 'Delete Jenkins project')
	jparser.add_argument('projectName',type=str, help='the name of the project')
	
	rparser = subparsers.add_parser('run', help = 'Run job on Jenkins')
	rparser.add_argument('projectName',type=str, help='the name of the project')
	rparser.add_argument('branchName',type=str, help='the name of the bra,ch')

	uparser = subparsers.add_parser('upload', help = 'Upload Jenkins project from Gitlab')
	uparser.add_argument('projectName',type=str, help='the name of the project')
	
	cparser = subparsers.add_parser('create-gitlab', help = 'Create Gitlab project')
	cparser.add_argument('projectName',type=str, help='the name of the project')
	
	args = parser.parse_args()
	print(args.command)
	

	if args.command=='delete-gitlab':
		delete_gitlab_project(args.projectName)
	if args.command=='delete-jenkins':
		delete_jenkins_project(args.projectName)
	if args.command=='run':
		run_jenkins_build(args.projectName,args.branchName)
	if args.command=='upload':
		create_job(args.projectName)
	if args.command=='create-gitlab':
		create_gitlab_project(args.projectName)



make_parser()



























