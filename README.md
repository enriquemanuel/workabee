Workabee - Scripting to SSH
=======================================
My daily job consists in administering several clients servers in which in some occasions I'm doing repetitive tasks. (I work at Blackboard at this time, so everything will be related to Blackboard and MH environment)
For this reason, I have created a script that is a work in progress, at this time, it just get the service status of Blackboard.

### More Information
This script is written in Python and used within Blackboard, because there are a few things that you need to define first, I would recommend that you review it first and then start making changes. 
I have implemented a help in it, this help allows you to understand what needs to be invoked and how, but before you need to define the servers in the top part. I will later change this to an external file and hopefully will be easier, but for now, this was the easiest way to do so.
This pretty much is based on the pexpect library so if you don't have it you might need to download it and install it.
Hope you enjoy it.

### Troubleshooting
At this time the the verbosity is enabled, so if you don't want to see anything written to the screen you can disable it by commeting out this line:     
	session.logfile = sys.stdout

### Next Steps:
1. Write the output to a file
2. Write only different outputs
3. Implements new functions
4. Implement the acceptance of new hosts


#### Thanks
Thanks for using it and any comments are welcomed. I'm still developing this and trying to make my life easier, hopefully it helps you too.

#### Caution
In my login section it consists of 10 parts

1. ssh user@host
2. will wait for a response that looks like:
        
        evalenzuela@10.7.240.109's password:

3. will send the password that was given in the CLI
4. will wait for a response that looks like: 

        [evalenzuela@apcstg-100327-248287-app02 ~]$
        
5. will send the following command to become root (this is MH specific)

        root

6. will wait for a response that looks like:
        
        Reason:

7. Will insert the following text:

        check the server

8. Will wait for a response that looks like: (the username varies depending on what you entered in the CLI)

        [sudo] password for evalenzuela:  

9. Will type again the password that was given in the CLI
10. Will wait for a response that looks like:
        
        [root@apcstg-100327-248287-app02 ~]#

Note: After all of this I will execute the action that was provided in the CLI (some are MH specific, you can alter them at your request.)
Note: I'm using regular expressions for the expect, so they can be altered to match your needs.



