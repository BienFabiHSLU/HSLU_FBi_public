# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 20:34:44 2020

@author: Fabian Bienz
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import csv


    
print ("Base Folder Path")
baseFolderPath = input()
print ("Place Number")
placeNumber = input()



for i in range (1,6):
        
    #Einlesen Start
    leicaPosBottomStart = pd.read_csv(baseFolderPath+"/LEICA_"+placeNumber+"_"+str(i)+"_start_u.bag.txt")
    leicaPosAboveStart = pd.read_csv(baseFolderPath+"/LEICA_"+placeNumber+"_"+str(i)+"_start_o.bag.txt")
    imuAngleBottomStart = pd.read_csv(baseFolderPath+"/IMU_"+placeNumber+"_"+str(i)+"_start_u.bag.txt")
    imuAngleAboveStart = pd.read_csv(baseFolderPath+"/IMU_"+placeNumber+"_"+str(i)+"_start_o.bag.txt")
    print("done")
    
    #Einlesen Drive
    leicaPosDrive = pd.read_csv(baseFolderPath+"/LEICA_"+placeNumber+"_"+str(i)+"_drive.bag.txt")
    fileImuAngleDrive = baseFolderPath+"/IMU_"+placeNumber+"_"+str(i)+"_drive.bag.txt"
    fileNameImuAngleDrive = os.path.basename(fileImuAngleDrive)
    imuAngleDrive = pd.read_csv(fileImuAngleDrive)
    print("done")
    
    #Einlesen End
    leicaPosBottomEnd = pd.read_csv(baseFolderPath+"/LEICA_"+placeNumber+"_"+str(i)+"_end_u.bag.txt")
    leicaPosAboveEnd = pd.read_csv(baseFolderPath+"/LEICA_"+placeNumber+"_"+str(i)+"_end_o.bag.txt")
    imuAngleBottomEnd = pd.read_csv(baseFolderPath+"/IMU_"+placeNumber+"_"+str(i)+"_end_u.bag.txt")
    imuAngleAboveEnd = pd.read_csv(baseFolderPath+"/IMU_"+placeNumber+"_"+str(i)+"_end_o.bag.txt")
    print("done")
    
    ##Drive Columns auslesen
    #IMU Drive
    driveRollX=imuAngleDrive["field.angular_velocity.z"]
    drivePitchY=imuAngleDrive["field.angular_velocity.y"]
    driveYawZ=imuAngleDrive["field.angular_velocity.x"]

    driveAngle=np.array([driveRollX, drivePitchY, driveYawZ])
    print(driveAngle)
      
    
    
    
    #Verlauf plotten X  
    plt.plot(driveRollX)
    plt.title("Roll Angle  " +placeNumber+"_"+str(i)+"_"+"Drive")
    #plt.axis([0,len(alphaDegImuDrive),0,3.5])
    plt.xlabel('Index')
    plt.ylabel('Roll X [°]')    
    plt.savefig("plots/Roll Angle " +placeNumber+"_"+str(i)+"_"+"Drive.png")
    plt.show()
    
    #Verlauf plotten X  
    plt.plot(drivePitchY)
    plt.title("Pitch Angle  " +placeNumber+"_"+str(i)+"_"+"Drive")
    #plt.axis([0,len(alphaDegImuDrive),0,3.5])
    plt.xlabel('Index')
    plt.ylabel('Pitch Y [°]')    
    plt.savefig("plots/Pitch Angle " +placeNumber+"_"+str(i)+"_"+"Drive.png")
    plt.show()
    
  
    
   
    
      
    v=1.42 ##[km/h]
    


 

    
    
