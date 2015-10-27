import time

while(1):
	userInput = raw_input()
	cleanID = userInput[1:3] + '-'
	cleanID += userInput[3:6] + '-'
	cleanID += userInput[6:10]
	authFile = file('id_data.txt')
	accessAllowed = False
	for line in authFile:
		if cleanID in line:
			accessAllowed = True
	currentTime = time.strftime('%H:%M:%S')
	if accessAllowed == True:
		#continue to keypad function
	logLine = 'Log attempt at: ' + currentTime + ' by ' + cleanID + '. User allowed access: ' + str(accessAllowed) + '.\n'
	logFile = open('log.txt','a')
	logFile.write(logLine)
	logFile.close()

