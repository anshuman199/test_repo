#!/usr/bin/env python
#*********************************************************************************************************
#   This code is exclusive property of [DB Research Inc.]                                            	 *
#   [DB Research Inc.] preserves all the copyrights to sell,                                         	 *
#   distribute,license, use, deploy, develop and modify this code as per its requirements.           	 *
#   Licensee is not supposed to modify,distribute or copy this code.                                 	 *
#   Licensees rights are restricted to the use of this as a part of his/her product and              	 *
#   distribute as a part of his/her product unless otherwise exclusively waved by a written          	 *
#   contract authorized by [DB Research Inc.]                                                        	 *
#   Manhattan is the trademark to be displayed with every bundling of this source by the licensee.   	 *
#   Code has been only exposed to development vendor DBResearchinc/DBR and its staff legally binds   	 *
#   under NDA and Non-compete as per Minnesota USA Jurisdiction and US copyright law.                	 *
#*********************************************************************************************************
#                   Copyright:: 2019, DB Research Inc, All Rights Reserved.                          	 *
#*********************************************************************************************************
import os, sys, threading, errno, socket, subprocess, json, urllib, datetime, time, shutil

global JREVERSION
global DOCKERTOOLVERSION
global AERROR
global ASUCCESS

AERROR = 1
ASUCCESS = 0
#---------------------------------------------------------------------------------------------------------
# Variables
#---------------------------------------------------------------------------------------------------------
JREVERSION = "1.8.0_131"
DOCKERTOOLVERSION = "17.10.0"
MANHATTANVERSION = "1.3.0"
DCOMPOSEVERSION = "1.22.0"
PRODUCTNAME = "Manhattan"
SERVICECOUNT = 9

SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
BASEPATH = os.path.abspath(os.path.join(SCRIPTPATH, os.pardir))
WAITFORITPATH = os.path.abspath(os.path.join(BASEPATH, os.pardir)) + "/current/shareddata/utility/waitforit"
#---------------------------------------------------------------------------------------------------------
# Function Name   : printHeader
# Purpose         : Function for print the Logo of DB Research Inc.
#---------------------------------------------------------------------------------------------------------
def printHeader():
	header = """
 Welcome to Manhattan product by DB Research Inc.

   \33[33m###\33[0m                       \33[33m###\33[0m
  \33[33m#\33[0m             \33[32m# #\33[0m             \33[33m#\33[0m
  \33[33m#\33[0m             \33[32m# #\33[0m             \33[33m#\33[0m    \33[32m# # # # #\33[0m
  \33[33m#\33[0m             \33[32m# #\33[0m             \33[33m#\33[0m    \33[32m#        #\33[0m
 \33[33m#\33[0m              \33[32m# #\33[0m              \33[33m#\33[0m   \33[32m#        #  # # # #   # # #   # # # #  # # # #  # # # #    # # #  #     #\33[0m
\33[33m#\33[0m     \33[32m# # # # # # # # # # # #\33[0m     \33[33m#\33[0m  \33[32m# # # # #   #        #        #        #     #  #      #  #       #     #\33[0m
 \33[33m#\33[0m   \33[32m#          # #          #\33[0m   \33[33m#\33[0m   \33[32m# # #       # # # #   # # #   # # # #  # # # #  # # # #   #       # # # #\33[0m
  \33[33m#\33[0m  \33[32m#          # #          #\33[0m  \33[33m#\33[0m    \33[32m#     #     #              #  #        #     #  # ##_     #       #     #\33[0m
  \33[33m#\33[0m   \33[32m# # # # # # # # # # # #\33[0m   \33[33m#\33[0m    \33[32m#       #   # # # #   # # #   # # # #  #     #  #    -#    # # #  #     #\33[0m
  \33[33m#\33[0m                             \33[33m#\33[0m
   \33[33m###\33[0m                       \33[33m###\33[0m

 #  Copyright:: 2019, All Rights Reserved  #
"""
	print (""+header+"")
#---------------------------------------------------------------------------------------------------------
# Function Name   : keyboardExceptionMessage
# Purpose         : Function will through the keyboard  exception message when user pressed the CTRL-C.
#---------------------------------------------------------------------------------------------------------
def keyboardExceptionMessage():
	print ("\n\33[33mInterruption: User pressed the CTRL-C\n\33[0m")
	sys.exit(AERROR)
#---------------------------------------------------------------------------------------------------------
# Class Name      : progressBar
# Purpose         : Class for Progress bar.
#---------------------------------------------------------------------------------------------------------
class progressBar(threading.Thread):
	def __init__(self):
		try:
			threading.Thread.__init__(self)
			self.event = threading.Event()
		except Exception as e:
			pass
	def run(self):
		try:
			event = self.event # make local
			sys.stdout.write("[")
			while not event.is_set():
				sys.stdout.write("#")
				sys.stdout.flush()
				event.wait(5) # pause for 5 second
				sys.stdout.write("")
		except Exception as e:
			pass
	def stop(self):
		try:
			sys.stdout.write("] \n")
			self.event.set()
		except Exception as e:
			pass
#---------------------------------------------------------------------------------------------------------
# Function Name   : replaceString
# Purpose         : This function will be replace the string in a file with new string.
#---------------------------------------------------------------------------------------------------------
def replaceString(file,oString,nString):
	try:
		if not os.path.isfile(file):
			print ("Error on replaceString, not a regular file: "+file)
			return AERROR;
		else:
			file1=open(file,'r').read()
			file2=open(file,'w')
			m=file1.replace(oString,nString)
			file2.write(m)
	except Exception as e:
		message = "Error: Something went wrong please try again"
		exception(message, e)
		return AERROR;	
	
	return ASUCCESS;
#---------------------------------------------------------------------------------------------------------
# Function Name   : dockerLogin
# Purpose         : This function will be Login on docker hub.
#---------------------------------------------------------------------------------------------------------
def dockerLogin(confFile):
	try:
		with open(""+confFile+"") as json_file:
			data = json.load(json_file)
			for p in data['dockerhub']:
				loginUser = p['USERNAME']
				pwd = p['PWD']
				dockerHubUrl = p['URL']
				if loginUser == "": # The variable
					print("Error: Please enter user-name and password in your file '"+confFile+"'")
					return AERROR;
				else:
					print ("Trying to login on docker hub")
					store = os.system('docker login -u '+loginUser+' -p '+pwd+' >> /dev/null 2>&1')
					if store == 0:
						print("Login Succeeded")
					else:
						print("Error: Invalid credentials please check your file '"+confFile+"'")
						return AERROR;
	except ValueError as e:
		print('invalid json: %s' % e)
		return AERROR;
	except Exception as e:
		print (str(e))
		return AERROR;	
	return ASUCCESS;
#---------------------------------------------------------------------------------------------------------
# Function Name   : setup
# Purpose         : This function will be create the docker containers. 
#---------------------------------------------------------------------------------------------------------
def dockerComposeUp(basePath,logFile,showLog):
	try:
		print ("\nYou can check the log at location: \033[0;36m"+logFile+"\033[0m")
		print ("\nPlease wait a while Manhattan product is configuring. This may take a few minutes...\n")
		progressTask = progressBar()
		os.chdir(basePath)
		if (os.name == "nt"):
			if showLog in ['N', 'n', 'NO', 'no', 'No']:
				progressTask.start()
				ret = os.system("gradlew composeUp >> \""+logFile+"\" 2>&1")
			else:
				ret = os.system("gradlew composeUp")
		else:
			if showLog in ['N', 'n', 'NO', 'no', 'No']:
				progressTask.start()
				ret = subprocess.call(["./gradlew composeUp >> \""+logFile+"\" 2>&1"], stderr=subprocess.STDOUT, shell=True)
			else:
				ret = subprocess.call(["./gradlew composeUp | tee "+logFile+""], stderr=subprocess.STDOUT, shell=True)
		if (ret == AERROR):
			progressTask.stop()
			return AERROR;
	except KeyboardInterrupt:
		progressTask.stop()
		keyboardExceptionMessage()
		return AERROR;
	except Exception as e:
		progressTask.stop()
		print (str(e))
		return AERROR;
	if showLog in ['N', 'n', 'NO', 'no', 'No']:	
		progressTask.stop()	
	return ASUCCESS;
#---------------------------------------------------------------------------------------------------------
# Function Name   : checkService
# Purpose         : This function will be check all the service and port availability of the all.
#                   components of Manhattan product
#---------------------------------------------------------------------------------------------------------
def checkService(serviceData, logPath, WAITFORITPATH):
	try:
		output = os.system("docker exec -i dbr-" + serviceData[1] + " /bin/bash -c \""+WAITFORITPATH+" dbr-" + serviceData[1] + ":" + serviceData[2] + " -t 1\" >> \""+logPath+"\" 2>&1")
		if output == 0:
			store = os.system("docker exec -i dbr-" + serviceData[1] + " /bin/bash -c \"" + serviceData[0] + " status\" >> \""+logPath+"\" 2>&1")
			if store == 0:
				return "STARTED";
	except KeyboardInterrupt:
		keyboardExceptionMessage()
		return AERROR;
	except Exception as e:
		print (str(e))
		return AERROR;
	return "FAILED";	
#---------------------------------------------------------------------------------------------------------
# Function Name   : updateServiceStatus
# Purpose         : Function will update the status of manhattan's services.
#---------------------------------------------------------------------------------------------------------
def updateServiceStatus(startedServiceList,failedServiceList):
	try:	
		for x in range(SERVICECOUNT):
			sys.stdout.write("\033[F") #back to previous line
			sys.stdout.write("\033[K") #clear line
		for k in range(len(startedServiceList)):
			if (startedServiceList[k] == "presto-coordinator" or startedServiceList[k] == "presto-worker-1" ):
				print("Service of " + startedServiceList[k] + "\t\t\t[\033[1;32;40mOK\033[0;37;40m]")
			else:
				print("Service of " + startedServiceList[k] + "\t\t\t\t[\033[1;32;40mOK\033[0;37;40m]")	
		for n in range(len(failedServiceList)):
			if (failedServiceList[n] == "presto-coordinator" or failedServiceList[n] == "presto-worker-1" ):
				print("Service of " + failedServiceList[n] + "\t\t\t\033[1;33;40mStarting...\033[0;37;40m")	
			else:
				print("Service of " + failedServiceList[n] + "\t\t\t\t\033[1;33;40mStarting...\033[0;37;40m")		
	except KeyboardInterrupt:
		keyboardExceptionMessage()
	except Exception as e:
		print (str(e))
		sys.exit(AERROR);
#---------------------------------------------------------------------------------------------------------
# Function Name   : finalServiceStatus
# Purpose         : Function will show the final status of manhattan's services.
#---------------------------------------------------------------------------------------------------------
def finalServiceStatus(startedServiceList,failedServiceList):
	try:
		for x in range(SERVICECOUNT):
			sys.stdout.write("\033[F") #back to previous line
			sys.stdout.write("\033[K") #clear line
		for k in range(len(startedServiceList)):
			if (startedServiceList[k] == "presto-coordinator" or startedServiceList[k] == "presto-worker-1" ):
				print("Service of " + startedServiceList[k] + "\t\t\t[\033[1;32;40mOK\033[0;37;40m]")
			else:
				print("Service of " + startedServiceList[k] + "\t\t\t\t[\033[1;32;40mOK\033[0;37;40m]")
		for l in range(len(failedServiceList)):	
			if (failedServiceList[l] == "presto-coordinator" or failedServiceList[l] == "presto-worker-1" ):
				print("Service of " + failedServiceList[l] + "\t\t\t[\033[1;31;40mFAILED\033[0;37;40m]")
			else:	
				print("Service of " + failedServiceList[l] + "\t\t\t\t[\033[1;31;40mFAILED\033[0;37;40m]")
	except KeyboardInterrupt:
		keyboardExceptionMessage()
	except Exception as e:
		print (str(e))
		sys.exit(AERROR);		
#---------------------------------------------------------------------------------------------------------
# Function Name   : callCheckService
# Purpose         : This function will call the checkServic function.
#---------------------------------------------------------------------------------------------------------
def callCheckService(logPath, WAITFORITPATH):
	try:
		print("\nVerifying the services of Manhattan components\n")
		startedServiceList=[];
		failedServiceList=[];
		removeList=[];
		
		psql_service_data=['service postgresql-9.3','postgres','5432']
		cassandra_service_data=['service cassandra','cassandra','9042']
		slapd_service_data=['service slapd','openldap','389']
		hive_service_data=['service hive-server2','hive ','10000']
		presto_service_data=['/usr/lib/presto/bin/launcher','presto-coordinator','8443']
		presto_worker_service_data=['/usr/lib/presto/bin/launcher','presto-worker-1','8443']
		zeppeline_service_data=['/zeppelin-0.7.2-bin-all/bin/zeppelin-daemon.sh','zeppelin','8444']
		manhattan_service_data=['service manhattan','manhattan','8080']
		nginx_service_data=['/etc/init.d/nginx','nginx','443']
		
		service_data_list=[psql_service_data, cassandra_service_data, slapd_service_data, hive_service_data, presto_service_data, presto_worker_service_data, zeppeline_service_data, manhattan_service_data, nginx_service_data]
		
		timeOut = 1000
		timeEnd = time.time() + timeOut
		for m in range(len(service_data_list)):
			if (service_data_list[m][1] == "presto-coordinator" or service_data_list[m][1] == "presto-worker-1" ):
				print("Service of " + service_data_list[m][1] + "\t\t\t\033[1;33;40mStarting...\033[0;37;40m")
			else:
				print("Service of " + service_data_list[m][1] + "\t\t\t\t\033[1;33;40mStarting...\033[0;37;40m")
		needToCheckStatus = 'TRUE'
		while needToCheckStatus == 'TRUE':	
			failedServiceList=[];
			removeList=[];
			for i in range(len(service_data_list)):
				output = os.system("docker top dbr-" + service_data_list[i][1] + " > nul 2>&1")
				if output != 0:
					print ("\n\33[31mERROR: Something went wrong. below container is not running...\33[0m\n")
					print ("dbr-"+service_data_list[i][1]+"\n")
					sys.exit(AERROR);
				ret = checkService(service_data_list[i], logPath, WAITFORITPATH);
				if (ret == "STARTED"):
					startedServiceList.append(service_data_list[i][1])
					removeList.append(service_data_list[i])
					if (len(startedServiceList) == SERVICECOUNT):
						needToCheckStatus = "FALSE"
				elif (ret == "FAILED"):	
					failedServiceList.append(service_data_list[i][1])
					needToCheckStatus = 'TRUE'
				elif (ret == AERROR):
					return AERROR;
			updateServiceStatus(startedServiceList,failedServiceList);
			for j in range(len(removeList)):
				service_data_list.remove(removeList[j]);
			if (time.time() > timeEnd):
				needToCheckStatus = "FALSE"	
		finalServiceStatus(startedServiceList,failedServiceList);		
	except KeyboardInterrupt:
		keyboardExceptionMessage()
		return AERROR;
	except Exception as e:
		print (str(e))
		return AERROR;
	return ASUCCESS;
#---------------------------------------------------------------------------------------------------------
# Function Name   : calculateTotalTime
# Purpose         : This function will be convert seconds into minutes and hours.
#---------------------------------------------------------------------------------------------------------
def calculateTotalTime (seconds,finished=False):
	seconds = int(seconds)
	status = 'time taken by '+PRODUCTNAME+':'
	if finished == True:
		status = 'finished in'

	if seconds < 60:
		hour = 00
		minutes = 00
		
	elif seconds < 3600:
		hour = 00
		minutes = seconds // 60
		seconds = seconds - 60*minutes
	else:
		hour = seconds // 3600
		minutes = (seconds - 3600*hour) // 60
		seconds = seconds - 3600*hour - 60*minutes
	print('\n'+'Total %s %02d:%02d:%02d' % (status, hour, minutes, seconds))

	
#---------------------------------------------------------------------------------------------------------
# Function Name   : createLogDirectory
# Purpose         : Function for create the log directory.
#---------------------------------------------------------------------------------------------------------
def createLogDirectory(LOGDIR,LOGFILE):
	try:
		if not os.path.exists(LOGDIR):
			os.makedirs(LOGDIR)
		else:
			if os.path.isfile(LOGFILE):
				shutil.copy(LOGFILE, LOGDIR + "/setup-" + str(time.time()) + ".out")
	except Exception as e:
		print (str(e))
		sys.exit(AERROR);
	except KeyboardInterrupt:
		functions.keyboardExceptionMessage()
