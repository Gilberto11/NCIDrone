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

gps_type = vehicle.parameters['GPS_TYPE']7
#setting gps param type to 3 = MTK
vehicle.parameters['GPS_TYPE']=3
gps_type = vehicle.parameters['GPS_TYPE']
#if statement checkiong if gps type is not equal to 4 then to set it to 4MTK19
if vehicle.parameters['GPS_TYPE']!=4:
	vehicle.parameters['GPS_TYPE']=4
	gps_type = vehicle.parameters['GPS_TYPE']


print("GPS_TYPE param value is %s"%str(gps_type))

