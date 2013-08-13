#!/usr/bin/env python

import pexpect
import getopt
import sys


# Global Variables
_user =""
_password = ""
_client = ""
_environment = ""
_action = ""
_patch = ""
_actions = ['restart, shutdown, start, status, getListOfPatches, patchInstall, patchRollback, qaCheck, tuneConfig, audit'] #list of defined actions at this time
_session =""

#list of regular expressions
#variables for expect
login_credentials = '[a-z]*[@][0-9]*[.][0-9]*[.][0-9]*[.][0-9]*[\'][s][ ]password'
first_execution = '[a-z]*[@][a-zA-Z0-9]*[-][a-zA-Z0-9]*[-][a-zA-Z0-9]*[-][a-zA-Z0-9]*[\s][~]\]\$'
reason_root = 'Reason: '
#root_password = '\[sudo\] password for '+_user+':'
second_execution = '[a-z]*[@][a-zA-Z0-9]*[-][a-zA-Z0-9]*[-][a-zA-Z0-9]*[-][a-zA-Z0-9]*[\s][~]\]#'

### LIST OF CLIENTS THAT IM CURRENTLY USING
### IF YOU ARE ADDING A NEW CLIENT PLEASE USE ALL CAPITALIZED BECAUSE THAT IS THE WAY IM GETTING THEM 
### ALSO IF YOU ARE USING STAGE USE STAGING -  PRODUCTION AS PRD OR PROD - TEST FOR TST OR TS --- FULL NAMES FOR VARIABLES 
### The naming is up to you, but whatever you type in the arguments will be capitalized entirely and then searched for any of the below variables
CLIENT_PRODUCTION=['10.0.0.1','10.0.0.2'] # this is just an example

def main(argv):
    try:
        opt, args = getopt.getopt(argv, "hu:p:c:e:a:z", ["help", "user=", "password=", "client=","environment=","action=","patch="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opt:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-u", "--user"):
            global _user, root_password
            _user = str(a)
            root_password = '\[sudo\] password for '+_user+':'
        elif o in ("-p", "--password"):
            global _password
            _password = str(a)
        elif o in ("-c", "--client"):
            global _client
            _client = str(a)
        elif o in ("-e", "--environment"):
            global _environment
            _environment = str(a)
        elif o in ("-a", "--action"):
            global _action
            _action = str(a)
        elif o in ("-z", "--patch"):
        	global _patch
        	_patch = str(a)
        else:
            assert False, "ERROR: Please refer to the help, -h or --help to get the list of available options"
    validate()
    #sys.exit()

def usage():
    usage = """
    -h --help			Prints this
    -u --user			Username to log in into systems via SSH
    -p --password		Password to log in into the systems via SSH               
    -c --client			Client that you want to run this: Client Name
    -e --environment 		Environment that you want to run: Production | Staging | Test 
    -a --action (cmd)		Command that you want to run at the moment in the servers: restart, shutdown, start, status, getListOfPatches, patchInstall, patchRollback, qaCheck, tuneConfig, audit
    -i --patch 			Patch that you want to rollback or remove (optional) - if the cmd is not related to patch this option is not needed

    Order: The order is important: user, password, client, environment, action, patch
    """
    print usage

def validate():
	#debug
	"""
	print _user
	print _password
	print _client
	print _environment
	print _action
	print _patch
	"""
	global _action, _actions
	if _user == "":
		print ""
		print "ERROR: you need to enter an username. Please refer to the help."
		usage()
		sys.exit()
	elif _password == "":
		print ""
		print "ERROR: you need to enter a password. Please refer to the help."
		usage()
		sys.exit()
	elif _client == "":
		print ""
		print "ERROR: you need to define a client. Please refer to the help."
		usage()
		sys.exit()
	elif _environment == "":
		print ""
		print "ERROR: you need to define an environment . Please refer to the help."
		usage()
		sys.exit()
	elif _action in ("patchInstall", "patchRollback"):
		if _patch =="":
			print ""
			print "ERROR: when doing a patch install or rollback the patch id is required."
			sys.exit()

	if any(_action in s for s in _actions):
		run()
		


def login(serverIP):
	
    session = pexpect.spawn('ssh '+_user+'@'+serverIP)
    global _session
    _session = session
    #log in files for debug
    #this is for debug to output everything to the screen
    session.logfile = sys.stdout
    #start exchanging information to log in and become root
    
    #check if new host to add it to known_hosts
    """
    i = session.expect(['.* password:', '.* continue connecting (yes/no)?'])
    if i == 1:
        session.sendline('yes')
    else:
    """
    session.expect(login_credentials)
    session.sendline(_password)
    session.expect(first_execution)
    #i logged in, now i want to become root
    session.sendline('root')
    session.expect(reason_root)
    session.sendline('check')
    session.expect(root_password)
    session.sendline(_password)
    session.expect(second_execution)
    return session

def run():
	global _client, _action
	_client = _client.upper()+"_"+_environment.upper()
	client = eval(str(_client))
	for server in client:
		print ""
		print "=========="
		print "initializing  connection to: " +server
		
		# creating the session
		session = login(server)
		
		#executing action
		print "---- start of execution -----"
		eval(str(_action))()
		print "---- end of execution -----"

		#closing connection
		#session.close(session)
		print ""
		print "finish connection to: "+ server
		print "==========="
    
### List of functions to the executed in the server

def status():
	global _session
	session = _session
	session.sendline('ServiceController.sh services.status')
	session.expect(second_execution)	



if __name__ == "__main__":
    main(sys.argv[1:]) # [1:] slices off the first argument which is the name of the program
