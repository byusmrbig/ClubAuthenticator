import time
import logging
import RPi.GPIO as GPIO
import signal
import sys
logging.basicConfig(filename='log.txt',level=logging.INFO,format='%(asctime)s %(message)s')	# automatically log all swipe attempts in this format

def signal_handler(signal, frame):		# a function to handle keyboard interrupts (hopefully not needed after implementation)
	print '\nExiting program...'		# display exit message
	sys.exit(0)				# gracefully exit the current program

class authenticator:
	ACCESS_DENIED = 'Denied'	# constant used for access denial
	ACCESS_GRANTED = 'Granted'	# constant used for standard entry
	ADMIN_ACCESS = 'Admin Use'	# constant used for administrative access
	led = 26			# defines GPIO port 26 for the LED 

	def cleanInput(self, cardID):		# cleans the input provided by the card reader
		cleanID = cardID[1:3] + '-'	# grab digits 1 to 2 of the card input (base 0)
		cleanID += cardID[3:6] + '-'	# append digits 3 to 5 of the card input onto the sanitized input
		cleanID += cardID[6:10]		# append digits 6 to 9 of the card input onto the sanitized input
		return cleanID			# return the sanitized student ID in the form of **-***-****

	def cardAuthCheck(self, sanitizedCardID):			# verifies whether or not swipped user is allowed entry
		authFile = file('id_data.txt')				# pulls authorized users from id_data.txt
		superFile = file('super_data.txt')			# pulls super users from super_data.txt
		accessAllowed = self.ACCESS_DENIED			# automatically sets access to 'Denied'
		for line in authFile:					# for every student ID listed in id_data.txt
			if sanitizedCardID in line:			# if the provided input is the ID on the current line
				accessAllowed = self.ACCESS_GRANTED	# set access to 'Granted'
		for line in superFile:					# for every user ID listed in super_data.txt
			if sanitizedCardID in line:			# if the provided input is the ID on the current line
				accessAllowed = self.ADMIN_ACCESS	# set access to 'Admin Use'
		return accessAllowed					# return the swipper's access level

	def swipeLog(self, userID, authAccessCode):						# logs the card swipe to the system logs
		currentTime = time.strftime('%H:%M:%S')						# grabs the current date
		logging.info('Swipe attempt by ' + userID + '. User access: ' + authAccessCode)	# log the time, user ID, and auth result to log.txt

	def GPIOprep(self):			# preps all needed GPIO on the Pi
		GPIO.setmode(GPIO.BCM)		# set up GPIO pins
		GPIO.setwarnings(False)		# disable GPIO warnings
		GPIO.setup(self.led, GPIO.OUT)	# set the LED port to output

	# def keypadResult:
		# check GPIO ports for input character, and get them one at a time
		# set timer for time entered function (30 or so seconds, after users has swipped; exits and returns null)
		# set timer for time since last key stroke (5 or so seconds; exits if user doesn't keep hitting keys)
		# 
	
	# def getKeys(self):
		# giant elif chain that listens for keys and returns a single char

	def main(self):								# the main function
		signal.signal(signal.SIGINT, signal_handler)			# prepare to handle keyboard interrupts
		while(1):							# run access input indefinitely
			self.GPIOprep()						# prep the GPIO
			userInput = raw_input()					# wait for the user to swipe their card
			cleanedSwipeInput = self.cleanInput(userInput)		# convert the card input into a human-readable input
			swipeResult = self.cardAuthCheck(cleanedSwipeInput)	# determine if person swipping card is authorized to enter
			self.swipeLog(cleanedSwipeInput, swipeResult)		# log the card swipe
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

if __name__ == '__main__':		# Prepare the above class to be used in order to implement object-oriented programming
	auth = authenticator()		# create a new authenticator object
	auth.main()			# run the object's 'main' function
	GPIO.cleanup()			# cleanup any left-over GPIO nonsense
