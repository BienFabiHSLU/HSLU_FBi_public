# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 22:22:59 2020

@author: Simon Bienz
"""
import numpy as np
import pandas as pd

print ("Base Folder Path")
baseFolderPath= input()
print("File Imu Above")
fileImuAbove = input()
print("File Imu Bottom")
fileImuBottom = input()
print("File Leica Above")
fileLeicaAbove = input()
print("File Leica Bottom")
fileLeicaBottom = input()

##Einlesen: Prisma Position oben
#leicaPosAbove = pd.read_csv(r"C:\Users\Simon Bienz\Documents\Fabian\HSLU\HS20\PAIND\Messdaten\test.txt")
leicaPosAbove = pd.read_csv(baseFolderPath+"/"+fileLeicaAbove)
aboveX=leicaPosAbove["field.point.x"].mean()
aboveY=leicaPosAbove["field.point.y"].mean()
aboveZ=leicaPosAbove["field.point.z"].mean()

aboveM=[aboveX,aboveY, aboveZ]
#print(aboveM)

#Testdaten, generieung Position unten
#bottomX=aboveX+8.0
#bottomX=aboveX
#bottomY=aboveY+10.0
#bottomZ=aboveZ-600.0

##Einlesen: Prisma Position unten
#leicaPosBottom = pd.read_csv(r"C:\Users\Simon Bienz\Documents\Fabian\HSLU\HS20\PAIND\Messdaten\test.txt")
leicaPosBottom = pd.read_csv(baseFolderPath+"/"+fileLeicaBottom)
bottomX=leicaPosBottom["field.point.x"].mean()
bottomY=leicaPosBottom["field.point.y"].mean()
bottomZ=leicaPosBottom["field.point.z"].mean()

bottomM=[bottomX, bottomY, bottomZ]
#print(bottomM)


#Einlesen: IMU-Daten oben
#imuAngleAbove = pd.read_csv(r"C:\Users\Simon Bienz\Documents\Fabian\HSLU\HS20\PAIND\Messdaten\test.txt")
imuAngleAbove = pd.read_csv(baseFolderPath+"/"+fileImuAbove)
aboveRollX=imuAngleAbove["field.angular_velocity.z"]
abovePitchY=imuAngleAbove["field.angular_velocity.y"]
aboveYawZ=imuAngleAbove["field.angular_velocity.x"]
aboveAngle=[aboveRollX, abovePitchY, aboveYawZ]
#print(aboveAngle)

#Einlesen: IMU-Daten unten
#imuAngleBottom = pd.read_csv(r"C:\Users\Simon Bienz\Documents\Fabian\HSLU\HS20\PAIND\Messdaten\test.txt")
imuAngleBottom = pd.read_csv(baseFolderPath+"/"+fileImuBottom)
bottomRollX=imuAngleBottom["field.angular_velocity.z"]
bottomPitchY=imuAngleBottom["field.angular_velocity.y"]
bottomYawZ=imuAngleBottom["field.angular_velocity.x"]
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
print("Gesamt-Neigungswinkel IMU\n"+str(alphaDegImu))
print("Gesamt-Neigungswinkel LEICA\n" +str(alphaDegLeica))

