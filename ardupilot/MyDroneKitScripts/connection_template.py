#Import required dependices

from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse


#Creating a function to connect the drone(copter)

def connectMyCopter():

	#creating a parse object
	parser = argparse.ArgumentParser(description='commands') 
	#using --connect to allow to call the drone ip address
	parser.add_argument('--connect')
	#capture the value and saving into the variable args
	args = parser.parse_args()

	#grabs the value of --connect and save into the variable connection_string
	connection_string = args.connect
	#if connection_string is not populated then import drone kit sitl
	if not connection_string:
		import dronekit_sitl
		#import and start a new sitl drone from my python scripts
		sitl = dronekit_sitl.start_default()
		#offer the option to populate the ip and port manually so either way there will be an IP address so a new SITL drone does not have 
		#to be launched everytime when testing a script
		connection_string = sitl.connection_string()

	#connect function that takes ip address as input and wait until it returns true
	vehicle = connect(connection_string,wait_ready=True)
	#return the vehicle object
	return vehicle



##########MAIN EXECUTABLE###########

vehicle = connectMyCopter()
