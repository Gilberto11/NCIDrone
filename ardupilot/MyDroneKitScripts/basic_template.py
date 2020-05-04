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
#taking the code I did on the arm and take off script and passing the target height variable
def arm_and_takeoff(targetHeight):
	#checking if the vehicle is armable
	while vehicle.is_armable!=True:
		print("Waiting for vehicle to become armable.")
		time.sleep(1)
	print("Vehicle is now armable")
	#setting the vehicle to guided mode
	vehicle.mode = VehicleMode("GUIDED")
	#checking if the flight mode is set to guide as a condition for the vehicle to arm
	while vehicle.mode!='GUIDED':
		print("Waiting for drone to enter GUIDED flight mode")
		time.sleep(1)
	print("Vehicle now in GUIDED MODE. Have fun!!")
	#requesting ardupilot to arm the drone
	vehicle.armed = True
	while vehicle.armed==False:
		print("Waiting for vehicle to become armed.")
		time.sleep(1)
	print("Look out! Virtual props are spinning!!")
	#at this stage the drone is armed from here we set the height target

	vehicle.simple_takeoff(targetHeight) ##meters

	while True:
		#printing the current altitude by accessing the vehicle.location attribute relative to the frame
		print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
		#setting a goal for the drone such as if the current vehicle altitude is greater or equal of the target height then 95% then break out of the loop
		if vehicle.location.global_relative_frame.alt>=.95*targetHeight:
			break
			#set to print it every second
		time.sleep(1)
	print("Target altitude reached!!")

	return None


#MAIN EXECUTABLE

vehicle = connectMyCopter()
#setting the height to 10 meters
arm_and_takeoff(10)

