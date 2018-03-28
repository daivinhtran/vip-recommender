import paramiko
import datetime

with open('password.txt') as f:
	for line in f:
		pw = line

with open('host.txt') as f:
	for line in f:
		host = line

with open('username.txt') as f:
	for line in f:
		username = line

print("ssh-ing into " + username + "@" + host)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh.connect(host, username=username, password=pw)
print("----------------------------")

print("gathering queue statistic")
print("executing qstat ...")
print("----------------------------")

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('qstat -q')
current_time = datetime.datetime.now()
new_file = open(str(current_time), 'w')

queues = {}

for line in iter(ssh_stdout.readline, ""):
	spl = line.split()
	if len(spl) > 1 and (spl[0] == 'joe' or spl[0] == 'joeforce'):
		print(spl[0] + " is having " + spl[6] + " waiting")
		queues[spl[0]] = int(spl[6])
	new_file.write(line)

best_queue = None

for queue in queues:
	if best_queue is None:
		best_queue = queue
	else:
		if queues[best_queue] > queues[queue]:
			best_queue = queue

print("----------------------------")

print("The recommended queue is : " + best_queue)


new_file.close()

