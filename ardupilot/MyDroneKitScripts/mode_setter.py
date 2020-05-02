#DEPENDENCIES

from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse


#FUNCTIONS

def connectMyCopter():

	parser = argparse.ArgumentParser(description='commands')
	parser.add_argument('--connect')
	args = parser.parse_args()

	connection_string = args.connect

	if not connection_string:
		import dronekit_sitl
		sitl = dronekit_sitl.start_default()
		connection_string = sitl.connection_string()

	vehicle = connect(connection_string,wait_ready=True)

	return vehicle

#MAIN EXECUTABLE

vehicle = connectMyCopter()

#there are pre conditions for the drone to arm so this while loop check those conditions, the code will only progress once those conditions are checked
while vehicle.is_armable!=True:
	print("Waiting for vehicle to become armable.")
	#loops every second until the drone is armable
	time.sleep(1)
print("Vehicle is now armable")
#changing the flight mode to GUIDED
vehicle.mode = VehicleMode("GUIDED")
# wating for ardupilot to change the fligh mode to guided
while vehicle.mode!='GUIDED':
	print("Waiting for drone to enter GUIDED flight mode")
	#keep looping through every second until ardupilot set flight mode to guided, 
	time.sleep(1)
	#if ardupilot changed to guided print the message below
print("Vehicle now in GUIDED MODE. Have fun!!")
#request to ardupilot for setting the drone to arm as now it is in the correct flight mode
vehicle.armed = True
#It takes time for sending the request to ardupilot, and get the response, so the below code prevents the script to stop until the request
#to ardupilot process the requests sent then it turns on the motors.
while vehicle.armed==False:
	print("Waiting for vehicle to become armed.")
	time.sleep(1)
print("Look out! Virtual props are spinning!!")

