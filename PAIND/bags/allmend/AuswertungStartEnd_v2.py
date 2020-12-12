# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 20:34:44 2020

@author: Fabian Bienz
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import csv


os.makedirs('plots', exist_ok=True)
csvfile = open('PAIND_Feldversuche_StartEnd.csv', 'w', newline='')
spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Place', 'Neigungswinkel IMU', 'Neigungswinkel LEICA', 'Differenz'])

print ("Base Folder Path")
baseFolderPath = input()
print ("Place Number")
placeNumber = input()

##Grenzen definieren (Daten Trimmen)
print ("Enter lower limit")
n = input()

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
    
    
    
    ##Einlesen: Prisma Position oben
    aboveX=leicaPosAboveStart["field.point.x"]
    aboveY=leicaPosAboveStart["field.point.y"]
    aboveZ=leicaPosAboveStart["field.point.z"]
    
    
    aboveX=aboveX[int(n) :]
    aboveY=aboveY[int(n) :]
    aboveY=aboveY[int(n) :]
    
    
    aboveX=aboveX.mean()
    aboveY=aboveY.mean()
    aboveZ=aboveZ.mean()
    aboveM=[aboveX,aboveY, aboveZ]
    #print(aboveM)
    
    ##Einlesen: Prisma Position unten
    
    bottomX=leicaPosBottomStart["field.point.x"]
    bottomY=leicaPosBottomStart["field.point.y"]
    bottomZ=leicaPosBottomStart["field.point.z"]
    
    
    bottomX=bottomX[int(n) :]
    bottomY=bottomY[int(n) :]
    bottomY=bottomY[int(n) :]
    
    
    bottomX=bottomX.mean()
    bottomY=bottomY.mean()
    bottomZ=bottomZ.mean()
    bottomM=[bottomX,bottomY, bottomZ]
    #print(aboveM)
    
    #Einlesen: IMU-Daten oben
    
    aboveRollX=imuAngleAboveStart["field.angular_velocity.z"]
    abovePitchY=imuAngleAboveStart["field.angular_velocity.y"]
    aboveYawZ=imuAngleAboveStart["field.angular_velocity.x"]
    aboveAngle=[aboveRollX, abovePitchY, aboveYawZ]
    #print(aboveAngle)
    
    #Einlesen: IMU-Daten unten
    
    bottomRollX=imuAngleBottomStart["field.angular_velocity.z"]
    bottomPitchY=imuAngleBottomStart["field.angular_velocity.y"]
    bottomYawZ=imuAngleBottomStart["field.angular_velocity.x"]
    bottomAngle=[bottomRollX, bottomPitchY, bottomYawZ]
    #print(bottomAngle)
    
    ##Berechnungen:
    
    #Normalenvektor Messebene
    eM=np.subtract(aboveM,bottomM)
    
    #Normalenvektor Referenzebene:
    eZ=[0,0,1]
    
    alphaRadLeica=np.arccos(np.dot(eZ,eM)/(np.linalg.norm(eM)*np.linalg.norm(eZ)))
    alphaDegLeica=np.degrees(alphaRadLeica)
    
    #Median IMU-Daten oben&unten
    bottomRollXmed=bottomRollX.median()
    bottomPitchYmed=bottomPitchY.median()
    bottomYawZmed=bottomYawZ.median()
    bottomAngleMedian=[bottomRollXmed, bottomPitchYmed, bottomYawZmed]
    
    aboveRollXmed=aboveRollX.median()
    abovePitchYmed=abovePitchY.median()
    aboveYawZmed=aboveYawZ.median()
    aboveAngleMedian=[aboveRollXmed, abovePitchYmed, aboveYawZmed]
    
    #Mittelwert der beiden Mediane, falls leiche Positionsänderung beim Verschieben
    meanRollX=np.mean([aboveRollXmed,bottomRollXmed])
    meanPitchY=np.mean([abovePitchYmed,bottomPitchYmed])
    meanYaw=np.mean([aboveYawZmed,bottomYawZmed])
    
    meanAngleImu=[meanRollX, meanPitchY, meanYaw]
    
    #Gesamtwinkel des IMU: Achtung! Winkel sind bereits in Degree, zuerst wieder in RAd umrechnen!
    alphaRadImu=np.arccos(np.cos(np.radians(meanRollX))*np.cos(np.radians(meanPitchY)))
    alphaDegImu=np.degrees(alphaRadImu)
    
    #Ausgabe
    print(placeNumber+"_"+str(i)+"_Start")
    print("Gesamt-Neigungswinkel IMU_Start\n"+str(alphaDegImu))
    print("Gesamt-Neigungswinkel LEICA_Start\n" +str(alphaDegLeica))
    print("Differenz Start\n" +str(abs(alphaDegImu-alphaDegLeica))+"\n")
    
    #spamwriter.writerow(['Place', 'Neigungswinkel IMU', 'Neigungswinkel LEICA', 'Differenz'])
    spamwriter.writerow([placeNumber+"_"+str(i)+"_Start", alphaDegImu, alphaDegLeica, abs(alphaDegImu-alphaDegLeica)])
    
    ##Einlesen: Prisma Position oben
    
    aboveX=leicaPosAboveEnd["field.point.x"]
    aboveY=leicaPosAboveEnd["field.point.y"]
    aboveZ=leicaPosAboveEnd["field.point.z"]
    
    
    aboveX=aboveX[int(n) :]
    aboveY=aboveY[int(n) :]
    aboveY=aboveY[int(n) :]
    
    
    aboveX=aboveX.mean()
    aboveY=aboveY.mean()
    aboveZ=aboveZ.mean()
    aboveM=[aboveX,aboveY, aboveZ]
    #print(aboveM)
    
    ##Einlesen: Prisma Position unten
    
    bottomX=leicaPosBottomEnd["field.point.x"]
    bottomY=leicaPosBottomEnd["field.point.y"]
    bottomZ=leicaPosBottomEnd["field.point.z"]
    
    
    bottomX=bottomX[int(n) :]
    bottomY=bottomY[int(n) :]
    bottomY=bottomY[int(n) :]
    
    
    bottomX=bottomX.mean()
    bottomY=bottomY.mean()
    bottomZ=bottomZ.mean()
    bottomM=[bottomX,bottomY, bottomZ]
    #print(aboveM)
    
    #Einlesen: IMU-Daten oben
    
    aboveRollX=imuAngleAboveEnd["field.angular_velocity.z"]
    abovePitchY=imuAngleAboveEnd["field.angular_velocity.y"]
    aboveYawZ=imuAngleAboveEnd["field.angular_velocity.x"]
    aboveAngle=[aboveRollX, abovePitchY, aboveYawZ]
    #print(aboveAngle)
    
    #Einlesen: IMU-Daten unten
    
    bottomRollX=imuAngleBottomEnd["field.angular_velocity.z"]
    bottomPitchY=imuAngleBottomEnd["field.angular_velocity.y"]
    bottomYawZ=imuAngleBottomEnd["field.angular_velocity.x"]
    bottomAngle=[bottomRollX, bottomPitchY, bottomYawZ]
    #print(bottomAngle)
    
    ##Berechnungen:
    
    #Normalenvektor Messebene
    eM=np.subtract(aboveM,bottomM)
    
    #Normalenvektor Referenzebene:
    eZ=[0,0,1]
    
    alphaRadLeica=np.arccos(np.dot(eZ,eM)/(np.linalg.norm(eM)*np.linalg.norm(eZ)))
    alphaDegLeica=np.degrees(alphaRadLeica)
    
    #Median IMU-Daten oben&unten
    bottomRollXmed=bottomRollX.median()
    bottomPitchYmed=bottomPitchY.median()
    bottomYawZmed=bottomYawZ.median()
    bottomAngleMedian=[bottomRollXmed, bottomPitchYmed, bottomYawZmed]
    
    aboveRollXmed=aboveRollX.median()
    abovePitchYmed=abovePitchY.median()
    aboveYawZmed=aboveYawZ.median()
    aboveAngleMedian=[aboveRollXmed, abovePitchYmed, aboveYawZmed]
    
    #Mittelwert der beiden Mediane, falls leiche Positionsänderung beim Verschieben
    meanRollX=np.mean([aboveRollXmed,bottomRollXmed])
    meanPitchY=np.mean([abovePitchYmed,bottomPitchYmed])
    meanYaw=np.mean([aboveYawZmed,bottomYawZmed])
    
    meanAngleImu=[meanRollX, meanPitchY, meanYaw]
    
    #Gesamtwinkel des IMU: Achtung! Winkel sind bereits in Degree, zuerst wieder in RAd umrechnen!
    alphaRadImu=np.arccos(np.cos(np.radians(meanRollX))*np.cos(np.radians(meanPitchY)))
    alphaDegImu=np.degrees(alphaRadImu)
    
    #Ausgabe
    print(placeNumber+"_"+str(i)+"_End")
    print("Gesamt-Neigungswinkel IMU_End\n"+str(alphaDegImu))
    print("Gesamt-Neigungswinkel LEICA_End\n" +str(alphaDegLeica))
    print("Differenz End\n" +str(abs(alphaDegImu-alphaDegLeica))+"\n")

    #spamwriter.writerow(['Place', 'Neigungswinkel IMU', 'Neigungswinkel LEICA', 'Differenz'])
    spamwriter.writerow([placeNumber+"_"+str(i)+"_End", alphaDegImu, alphaDegLeica, abs(alphaDegImu-alphaDegLeica)])
    
csvfile.close()
    
