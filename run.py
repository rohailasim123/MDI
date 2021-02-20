from subprocess import Popen, PIPE, call
from argparse import ArgumentParser
from multiprocessing import Process
import signal
import subprocess
import sys
import os
import threading
from time import sleep, time
import arg_parser
import context
import threading
from tqdm import tqdm

def positive_int(arg):
        arg = int(arg)
        if arg <= 0:
                raise argparse.ArgumentError('Argument must be a positive integer')
        return arg

def simpleRun():
	print args
	
	if args.algo == 'verus':
		RunVERUS()
	elif args.algo == 'modelVerus':
		RunModelVERUS()
	elif args.algo == 'copa':
		RunCopa()
	elif args.algo == 'modelCopa':
		RunModelCopa()

	print ("Finished")

	return

def RunVERUS():
	if not os.path.exists(args.dir + '/verus'):
		os.makedirs(args.dir+ "/verus")
	if not os.path.exists(args.dir + '/verus/'+str(args.name)):
		os.makedirs(args.dir+ "/verus/"+str(args.name))
	
	print("Begin " + str(args.time) + " seconds of verus transmission")
	command = "./protocols/verus-test/src/verus_server -name "+args.dir + "/verus/"+str(args.name)+" -p 60001 -t "+ str(args.time)#+" > rubbishVerus"
	print command
	pro = Popen(command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
	
	tmp = "mm-delay 20 mm-link ./"+str(args.trace)+" ./"+str(args.trace)+" --meter-all --uplink-log "+str(args.dir)+"/verus/"+str(args.name)+"/"+args.name+"-uplink.csv --downlink-log "+str(args.dir)+"/verus/"+str(args.name)+"/"+args.name+"-downlink.csv"
	print tmp

	p = Popen(tmp, stdin=PIPE,shell=True)
	p.communicate("./protocols/verus-test/src/verus_client $MAHIMAHI_BASE -p 60001\nexit\n")

	os.system("ps | pgrep -f verus_server | xargs kill -9")
	os.system("ps | pgrep -f verus_client | xargs kill -9")
	os.system("mv client_60001* "+args.dir + "/verus/"+str(args.name)+"/")

def RunModelVERUS():
	if not os.path.exists(args.dir + '/modelVerus'):
		os.makedirs(args.dir+ "/modelVerus")
	if not os.path.exists(args.dir + '/modelVerus/'+str(args.name)):
		os.makedirs(args.dir+ "/modelVerus/"+str(args.name))

	args.dir = args.dir+"/modelVerus/"
	matrix = "/home/muhammad/Desktop/MDI_2.0/verus_matrix/verus-N1000-transMatrix.csv"
	
	#starting the gmcc server
	command = "./protocols/gmcc2/src/verus_server -name "+args.dir+str(args.name)+" -p 60001 " + "-tr "+matrix+" -t "+ str(args.time) +" > rubbishmodelVerus &"
	pro = Popen(command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
	sleep(5)

	print("Begin " + str(args.time) + " seconds of Model VERUS transmission")
	command = "mm-delay 20 mm-link ./"+str(args.trace)+" ./"+str(args.trace)+" --meter-all --uplink-log "+args.dir+args.name+"-uplink.csv --downlink-log "+args.dir+args.name+"-downlink.csv"
	print command
	p = Popen(command, stdin=PIPE,shell=True)
	p.communicate("./protocols/gmcc/src/verus_client $MAHIMAHI_BASE -p 60001 -t "+ str(args.time)+ " \n exit")

	os.system("ps | pgrep -f verus_server | xargs kill -9")
	os.system("ps | pgrep -f verus_client | xargs kill -9")
	#os.system("mv client_60001* "+args.dir + "/modelVerus/"+str(args.name)+"/")

def RunCopa():
	if not os.path.exists(args.dir + '/copa'):
		os.makedirs(args.dir+ "/copa")
	if not os.path.exists(args.dir + '/copa/'+str(args.name)):
		os.makedirs(args.dir+ "/copa/"+str(args.name))

	args.dir = args.dir+"/copa/"
	
	#starting the gmcc server
	command = "./protocols/copa2/receiver &"
	pro = Popen(command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
	sleep(2)

	print("Begin " + str(args.time) + " seconds of COPA")
	command = "mm-delay 20 mm-link ./"+str(args.trace)+" ./"+str(args.trace)+" --meter-all --uplink-log "+args.dir+args.name+"-uplink.csv --downlink-log "+args.dir+args.name+"-downlink.csv"
	print command
	p = Popen(command, stdin=PIPE,shell=True)
	p.communicate("export MIN_RTT=10000 &&./protocols/copa2/sender serverip=$MAHIMAHI_BASE offduration=0 onduration=1000000000 cctype=markovian delta_conf=do_ss:auto:0.02 traffic_params=byte_switched,num_cycles=5 > info.out & \n sleep " + str(args.time) + " \n exit")

	os.system("ps | pgrep -f /copa2/sender | xargs kill -9")
	os.system("ps | pgrep -f /copa2/receiver | xargs kill -9")
	os.system("mv info.out "+args.dir+str(args.name)+"/")

def RunModelCopa():
	if not os.path.exists(args.dir + '/modelCopa'):
		os.makedirs(args.dir+ "/modelCopa")
	if not os.path.exists(args.dir + '/modelCopa/'+str(args.name)):
		os.makedirs(args.dir+ "/modelCopa/"+str(args.name))

	args.dir = args.dir+"/modelCopa/"
	matrix = "/home/muhammad/Desktop/MDI_2.0/copa_matrix/copa-N1000-transMatrix.csv"
	
	command = "./protocols/gmcc2/src/verus_server -name "+args.dir+str(args.name)+" -p 60001 " + "-tr "+matrix+" -t "+ str(args.time) +" > rubbishmodelcopa &"
	pro = Popen(command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
	sleep(5)

	print("Begin " + str(args.time) + " seconds of Model COPA transmission")
	command = "mm-delay 20 mm-link ./"+str(args.trace)+" ./"+str(args.trace)+" --meter-all --uplink-log "+args.dir+args.name+"-uplink.csv --downlink-log "+args.dir+args.name+"-downlink.csv"
	print command
	p = Popen(command, stdin=PIPE,shell=True)
	p.communicate("./protocols/gmcc2/src/verus_client $MAHIMAHI_BASE -p 60001 -t "+ str(args.time)+ " \n exit")

	os.system("ps | pgrep -f verus_server | xargs kill -9")
	os.system("ps | pgrep -f verus_client | xargs kill -9")

	os.system("ps | pgrep -f /copa2/sender | xargs kill -9")
	os.system("ps | pgrep -f /copa2/receiver | xargs kill -9")


if __name__ == '__main__':
	parser = ArgumentParser(description="Shallow queue tests")
	parser.add_argument('--dir', '-d',help="Directory to store outputs",required=True)
	parser.add_argument('--trace', '-tr',help="Cellsim traces to be used",required=True)
	parser.add_argument('--time', '-t',help="Duration (sec) to run the experiment",type=int,default=10)
	parser.add_argument('--name', '-n',help="name of the experiment",required=True)
	parser.add_argument('--algo',help="Algorithm under which we are running the simulation",required=True)
	parser.add_argument('--tcp_probe',help="whether tcp probe should be run or not",action='store_true',default=False)
	parser.add_argument('--command', '-c', help="mm-link command to run", required=False)                
	parser.add_argument('--queue', type=positive_int, help='Queue size in mahimahi')
	args = parser.parse_args()
	simpleRun()


