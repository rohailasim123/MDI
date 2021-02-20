import os

time=300
dir='Verus_4G_runs'

for i in range(1,1000):
	trace = '4G_Synthetic/channel'+str(i)+".csv"
	command = "python run.py -tr "+trace
	command += " -t "+str(time)
	command += " --name "+"channel_log_{0}".format(i)
	command += " --dir "+dir 
	command += " --algo verus --tcp_probe "

	os.system(command)

