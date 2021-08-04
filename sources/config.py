#!/usr/bin/python3

import configparser

# IMPORT CONFIG

config = configparser.ConfigParser()
config.read('config')


class jenkinsConf():

	def setUrl(self, url):
		config['JENKINS']['ipv4_jenkins'] = url
		return config['JENKINS']['ipv4_jenkins']
		
	def setToken(self, token):
		config['JENKINS']['jenkins_api_token'] = token
		return config['JENKINS']['jenkins_api_token']
		
	def setUser(self, user):
		config['JENKINS']['jenkins_user'] = user
		return config['JENKINS']['jenkins_user']
		
	def setPasswd(self, passwd):
		config['JENKINS']['jenkins_passwd'] = passwd
		return config['JENKINS']['jenkins_passwd']
		
	def setGitlabName(self, name):
		config['JENKINS']['gitlab_server_name_in_jenkins'] = name
		return config['JENKINS']['gitlab_server_name_in_jenkins']
		
		

class gitlabConf():

	def setUrl(self, url):
		config['GITLAB']['ipv4_gitlab'] = url
		return config['GITLAB']['ipv4_gitlab']
		
	def setToken(self, token):
		config['GITLAB']['gitlab_api_token'] = token
		return config['GITLAB']['gitlab_api_token']
		
	def setUser(self, user):
		config['GITLAB']['gitlab_user'] = user
		return config['GITLAB']['gitlab_user']
		
	def setPasswd(self, passwd):
		config['GITLAB']['gitlab_passwd'] = passwd
		return config['GITLAB']['gitlab_passwd']


print('Input jenkins url')
jenkins_url = input()
print('Input port')
jenkins_port = input()
jenkinsConf().setUrl(jenkins_url+':'+jenkins_port)

print('Input jenkins token')
jenkins_token = input()
jenkinsConf().setToken(jenkins_token)

print('Input jenkins user name')
jenkins_user = input()
jenkinsConf().setUser(jenkins_user)

print('Input jenkins password')
jenkins_passwd = input()
jenkinsConf().setPasswd(jenkins_passwd)

print('Input gitlab server name on jenkins')
gitlab_name = input()
jenkinsConf().setGitlabName(gitlab_name)

print('Input gitlab url')
gitlab_url = input()
print('Input port')
gitlab_port = input()
gitlabConf().setUrl(gitlab_url+':'+gitlab_port)

print('Input gitlab token')
gitlab_token = input()
gitlabConf().setToken(gitlab_token)

print('Input gitlab user name')
gitlab_user = input()
gitlabConf().setUser(gitlab_user)

print('Input gitlab password')
gitlab_passwd = input()
gitlabConf().setPasswd(gitlab_passwd)

with open ('config','w') as configfile:
	config.write(configfile)




