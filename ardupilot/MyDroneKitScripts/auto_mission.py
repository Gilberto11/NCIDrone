#DEPENDENCIES
#also importing Command from drone kit in order to execute the arduplito commands
from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException,Command
import time
import socket
import exceptions
import math
import argparse
from pymavlink import mavutil
#FUNCTIONS
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

	return vehicle
#function for the drone to take off to a specified altitude
def arm_and_takeoff(targetHeight):
	#condition for the drone to arm, if not flight mode guided keep looping until flight mode is set to guided by ardupilot
	while vehicle.is_armable!=True:
		print("Waiting for vehicle to become armable.")
		time.sleep(1)
	print("Vehicle is now armable")
	`#requesting ardupilot to change flight mode to guided
	vehicle.mode = VehicleMode("GUIDED")
	#while loop waiting for ardupilot response, loop keeps going until the reponse with the request made is true
	while vehicle.mode!='GUIDED':
		print("Waiting for drone to enter GUIDED flight mode")
		time.sleep(1)
	print("Vehicle now in GUIDED MODE. Have fun!!")
	#while loop to ensure that the script does not time out as it takes time for the request and response from ardupilot to be processed
	vehicle.armed = True
	while vehicle.armed==False:
		print("Waiting for vehicle to become armed.")
		time.sleep(1)
	print("Look out! Virtual props are spinning!!")

	vehicle.simple_takeoff(targetHeight) ##meters
	#while armed fly takeoff to the specified altitude, target is reached as long it reaches 95% of the final goal at least
	while True:
		print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt>=.95*targetHeight:
			break
		time.sleep(1)
	print("Target altitude reached!!")

	return None

#MAIN EXECUTABLE

vehicle = connectMyCopter()

##Command template
#Command(0,0,0,FrameOfReference,MAVLinkCommand,CurrentWP,AutoContinue,param1,param2,param3,param4,param5,parm6,param7)
#creating the waypoint object that is the home location of the drone before it takes off
wphome=vehicle.location.global_relative_frame

##List of commands
cmd1=Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,wphome.lat,wphome.lon,wphome.alt)
cmd2=Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,44.501375,-88.062645,15)
cmd3=Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,44.501746,-88.062242,10)
cmd4=Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,0,0,0,0,0,0,0,0,0)

##Donload current list of commands FROM the drone we're connected to
cmds = vehicle.commands
cmds.download()
cmds.wait_ready()

##Clear the current list of commands
cmds.clear()

##Add in our new commands
cmds.add(cmd1)
cmds.add(cmd2)
cmds.add(cmd3)
cmds.add(cmd4)

##Upload our commands to the drone
vehicle.commands.upload()

arm_and_takeoff(10)

print("After arm and takeoff")
vehicle.mode = VehicleMode("AUTO")
while vehicle.mode!="AUTO":
	time.sleep(.2)

while vehicle.location.global_relative_frame.alt>2:
	print("Drone is executing mission, but we can still run code")
	time.sleep(2)


