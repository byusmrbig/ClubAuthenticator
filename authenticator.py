import time
import logging
import RPi.GPIO as GPIO
import signal
import sys
logging.basicConfig(filename='log.txt',level=logging.INFO,format='%(asctime)s %(message)s')	# automatically log all swipe attempts in this format

def signal_handler(signal, frame):	# a function to handle keyboard interrupts (hopefully not needed after implementation)
	print '\nExiting program...'	# display exit message
	sys.exit(0)	# gracefully exit the current program

class authenticator:
	FULL_MEMBER = 'Dues Paid and Agreement Signed'	# constant used for full member status
	PAY_DUES = 'Student Needs to Pay Dues'	# constant used for students needing to pay dues
	AGREEMENT_NEEDED = 'Member Needs to Sign the Agreement'	# constant used for members needing to sign the club agreement
	greenLED = 3	# defines GPIO port 3 for the LED
	blueLED = 5		# defines GPIO port 5 for the LED
	redLED = 7		# defines GPIO port 7 for the LED

	def cleanInput(self, cardID):	# cleans the input provided by the card reader
		cleanID = cardID[1:3] + '-'	# grab digits 1 to 2 of the card input (base 0)
		cleanID += cardID[3:6] + '-'	# append digits 3 to 5 of the card input onto the sanitized input
		cleanID += cardID[6:10]	# append digits 6 to 9 of the card input onto the sanitized input
		return cleanID	# return the sanitized student ID in the form of **-***-****

	def cardAuthCheck(self, sanitizedCardID):	# checks the membership status of the swiping student
		nonAgreement = file('needs_agreement.txt')	# pulls members who haven't signed agreements from needs_agreement.txt
		membersFile = file('full_member.txt')	# pulls full members from full_member.txt
		needsDues = self.PAY_DUES	# automatically sets status to 'Student Needs to Pay Dues'
		for line in membersFile:	# for every student ID listed in full_member.txt
			if sanitizedCardID in line:	# if the provided input is the ID on the current line
				needsDues = self.FULL_MEMBER	# set status to 'Dues Paid and Agreement Signed'
		for line in superFile:	# for every user ID listed in needs_agreement.txt
			if nonAgreement in line:	# if the provided input is the ID on the current line
				needsDues = self.AGREEMENT_NEEDED	# set status to 'Member Needs to Sign the Agreement'
		return needsDues	# return the swipper's club status

	def swipeLog(self, userID, userStatus):	# logs the card swipe to the system logs
		currentTime = time.strftime('%H:%M:%S')	# grabs the current date
		logging.info('Swipe attempt by ' + userID + '. User status: ' + userStatus)	# log the time, user ID, and auth result to log.txt

	def GPIOprep(self):	# preps all needed GPIO on the Pi
		GPIO.setmode(GPIO.BCM)	# set up GPIO pins
		GPIO.setwarnings(False)	# disable GPIO warnings
		GPIO.setup(self.greenLED, GPIO.OUT)	# set the LED port to output
		GPIO.setup(self.blueLED, GPIO.OUT)	# set the LED port to output
		GPIO.setup(self.redLED, GPIO.OUT)	# set the LED port to output

	# def keypadResult:
		# check GPIO ports for input character, and get them one at a time
		# set timer for time entered function (30 or so seconds, after users has swipped; exits and returns null)
		# set timer for time since last key stroke (5 or so seconds; exits if user doesn't keep hitting keys)
		# 
	
	# def getKeys(self):
		# giant elif chain that listens for keys and returns a single char

	def main(self):	# the main function
		signal.signal(signal.SIGINT, signal_handler)	# prepare to handle keyboard interrupts
		while(1):	# run access input indefinitely
			self.GPIOprep()	# prep the GPIO
			userInput = raw_input()	# wait for the user to swipe their card
			cleanedSwipeInput = self.cleanInput(userInput)	# convert the card input into a human-readable input
			swipeResult = self.cardAuthCheck(cleanedSwipeInput)	# determine if person swipping card is authorized to enter
			self.swipeLog(cleanedSwipeInput, swipeResult)	# log the card swipe
			if swipeResult == 'Denied':
				# break, restarting the while loop
				continue
			elif swipeResult == 'Granted':
				# keypadResult = self.getKeypadInputs()
				GPIO.output(self.led, 1)
				time.sleep(3)
				GPIO.output(self.led, 0)
			elif swipeResult == 'Admin Use':
				# begin superUserPin function
				continue

if __name__ == '__main__':	# Prepare the above class to be used in order to implement object-oriented programming
	auth = authenticator()	# create a new authenticator object
	auth.main()	# run the object's 'main' function
	GPIO.cleanup()	# cleanup any left-over GPIO nonsense
