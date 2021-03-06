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

os.makedirs('plots', exist_ok=True)
csvfile = open('PAIND_Feldversuche_Drive.csv', 'w', newline='')
spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Place', 'TrimSart', 'TrimEnd', 'Median', 'Mean', 'Std', 'Max', 'Min', '>5°'])

csvfile2 = open('PAIND_Drive_Outliers.csv', 'w', newline='')
spamwriter2 = csv.writer(csvfile2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter2.writerow(['Ausreisser'])
    
print ("Base Folder Path")
baseFolderPath = input()
print ("Place Number")
placeNumber = input()

#Leeres DataFrame für den gesamten Boxplot
df2=pd.DataFrame()

for i in range (1,5):
        
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
      
    
    ##Gesamtwinkel berechnen
    alphaRadImuDrive=np.arccos(np.cos(np.radians(driveRollX))*np.cos(np.radians(drivePitchY)))
    alphaDegImuDrive=np.degrees(alphaRadImuDrive)
    print(alphaDegImuDrive)
    
    #Verlauf plotten    
    plt.plot(alphaDegImuDrive)
    plt.title("Neigungswinkel: " +placeNumber+"_"+str(i)+"_"+"Drive")
    #plt.axis([0,len(alphaDegImuDrive),0,3.5])
    plt.xlabel('Index')
    plt.ylabel('Neigungswinkel alpha [°]')    
    plt.savefig("plots/Neigungswinkel: " +placeNumber+"_"+str(i)+"_"+"Drive.png")
    plt.show()
  
    
    ##Grenzen definieren (Daten Trimmen)
    print ("Enter lower limit")
    n = input()
    print ("Enter upper limit")
    m = input()

    #Untere Anz. n Messwerte aussortieren
    trimAlphaDegImuDrive=alphaDegImuDrive[int(n) :]
    #Obere Anz. m Messwerte aussortieren
    trimAlphaDegImuDrive=trimAlphaDegImuDrive[: len(trimAlphaDegImuDrive)-int(m)]
       
    print(trimAlphaDegImuDrive)
    
    #Getrimmter Verlauf plotten    
    plt.plot(trimAlphaDegImuDrive)
    plt.title("Neigungswinkel: " +placeNumber+"_"+str(i)+"_"+"Drive")
    #plt.axis([0,len(alphaDegImuDrive),0,3.5])
    plt.xlabel('Index')
    plt.ylabel('Neigungswinkel alpha [°]')    
    plt.savefig("plots/Trim_Neigungswinkel: " +placeNumber+"_"+str(i)+"_"+"Drive.png")
    #plt.show()
    
    
    ##Statistische Grössen
    
    std=np.std(trimAlphaDegImuDrive)
    print("Stadardabweichung[alpha]= " + str(std))
    median = np.median(trimAlphaDegImuDrive)
    print("Median[alpha]= " + str(median))
    mean=np.mean(trimAlphaDegImuDrive)
    print("Mittelwert[alpha]= " + str(mean))
    
    #Entspircht Max Neigungswinkel
    maxi=np.max(trimAlphaDegImuDrive)
    print("Max[alpha]=" + str(maxi))
    #Entspircht Min Neigungswinkel
    mini=np.min(trimAlphaDegImuDrive)
    print("Min[alpha]=" + str(mini))
    
    #Ausreisser Rausschreiben (outliers)
    label=placeNumber+"_"+str(i)+"_"+"Drive" 
    df = pd.DataFrame({'Data':trimAlphaDegImuDrive})
    outliers = df[np.abs(df.Data-df.Data.mean()) > (3*df.Data.std())]
    print("Ausreisser: " +str(outliers))
    
    #Werte grösser 5°
    grFive = trimAlphaDegImuDrive[trimAlphaDegImuDrive > 5] 
    print("Werte >5°: " +str(grFive))
    
    #spamwriter.writerow(['Place', 'TrimSart', 'TrimEnd', 'Median', 'Mean', 'Std', 'Max', 'Min', '>5°'])
    spamwriter.writerow([label, n, m, median, mean, std, maxi, mini, grFive])
    
    #spamwriter2.writerow(['Ausreisser'])
    spamwriter2.writerow([outliers])
    
    
    #Boxplot
    df.columns = [label]
    titleBoxplot = "Boxplot: "+placeNumber+"_"+str(i)+"_"+"Drive" 
    df.plot(kind="box", title=titleBoxplot)
    plt.ylabel('Neigungswinkel alpha [°]')
    plt.savefig("plots/Boxplot: "+placeNumber+"_"+str(i)+"_"+"Drive")
    plt.close()
    #plt.show()
    
       
    #Histogramm
    #Fausregel sqrt(n-Observationen)
    trimAlphaDegImuDrive.plot(kind="hist", edgecolor="black", bins=int(np.sqrt(len(trimAlphaDegImuDrive))))
    plt.title("Histogramm: " +placeNumber+"_"+str(i)+"_"+"Drive")     
    plt.xlabel("Neigungswinkel alpha [°]")
    plt.ylabel("Anz. Messwerte")
    plt.savefig("plots/Histogramm: " +placeNumber+"_"+str(i)+"_"+"Drive")
    plt.close()
    #plt.show()
    
    #DataFrames aus for Loop schreiben
    df2=df2.append(df)
    print(df2)
    
      
    v=1.42 ##[km/h]
    

csvfile.close()
csvfile2.close()
 
#Boxplot über alles
df2.plot(kind="box", title="Boxplot: Drive_Platz_" +placeNumber)   
plt.ylabel('Neigungswinkel alpha [°]')
plt.savefig("plots/Boxplot: Drive_Platz_" +placeNumber)
plt.show()
plt.close()
    
    
