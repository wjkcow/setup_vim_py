import os
from os import path
from shutil import move

import vimCfg 
#vim is configured by the ~/.vimrc file and bundles in ~/vim file
#This program will backup current settings to ~/.vimrc_backup and ~/.vim_backup
vimrcFilePath = os.environ['HOME'] + "/.vimrc";
vimPath = os.environ['HOME'] + "/.vim";
vimBackUpPath = os.environ['HOME'] + "/.vim_backup";
vimrcBackUp = os.environ['HOME'] + "/.vimrc_backup";
#pathogenPath allow bundle to be installed into ~/.vim/Bundle.
autoloadPath = os.environ['HOME'] + "/.vim/autoload"
pathogenFile = os.environ['HOME'] + "/.vim/autoload/pathogen.vim";
BundlePath = os.environ['HOME'] + "/.vim/bundle";
git ='git clone %s %s' 

#rmdir() will remove dir and all it's content.
#CAUTION THIS FUNCTION IS DANGEROUS!
def rmdir(path):
	for root, dirs, files in os.walk(path, topdown = False):
		for name in files:
			os.remove(os.path.join(root, name));
		for name in dirs:
			os.rmdir(os.path.join(root, name));
#to backup current settings
def backup():
	#check and remove current backup
	if path.isfile(vimrcBackUp):
		os.remove(vimrcBackUp);
	if path.isdir(vimBackUpPath):
		rmdir(vimBackUpPath);
	#make back up of current settings
	if path.isfile(vimrcFilePath):
		print "Backing up .vimrc";
		move(vimrcFilePath, vimrcBackUp);
	if path.isdir(vimPath):
		print "Backing up .vim";
		move(vimPath, vimBackUpPath);
#to restore backups
def restoreBackup():
	#check and remove current settings
	if path.isfile(vimrcFilePath):
		os.remove(vimrcFilePath);
	if path.isdir(vimPath):
		rmdir(vimBackUpPath);
	#move backup settings back
	if path.isfile(vimrcBackUp):
		move(vimrcBackUp, vimrcFilePath);
	if path.isdir(vimBackUpPath):
		move(vimBackUpPath, vimPath);
#use pathogen to make 
#to install new configures
def configure():
	#make vimrc file
	vimrcFile = open(vimrcFilePath, 'w');
	#install pathogen
	pathogenUrl = "https://github.com/tpope/vim-pathogen.git";
	pathogenVimrc = [":call pathogen#infect()\n", "syntax on\n", "filetype plugin indent on\n"];
	vimrcFile.writelines(pathogenVimrc);
	os.system(git%(pathogenUrl,vimPath));
	#writting configures to vimrc files and close vimrcfile
	vimrcFile.writelines(vimCfg.vimrc);
	vimrcFile.close();
	#download and install plugins
	os.makedirs(BundlePath);
	for pluginName in vimCfg.plugin:
		os.system(git%(vimCfg.plugin[pluginName],(BundlePath + '/' + pluginName)));


#program
if path.isfile(vimrcBackUp) or path.isdir(vimBackUpPath):
	print """
Found backup file. Do you want to restore backup(Yes)
or install new configuration(No)
Note:
	Restore backup will lost current settings
	Install new configuration will lost current backup
	""";
	userInput = raw_input('(Yes/No)?: ');
	while (userInput != 'Yes' and userInput != 'No'):
			userInput = raw_input('(Yes/No)?: ');
	if userInput == 'Yes':
		restoreBackup();
	else:
		backup();
		configure();
else:
	print "No backup file found. Installing new configuration.";
	backup();
	configure();
