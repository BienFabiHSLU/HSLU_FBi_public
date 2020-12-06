# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 20:34:48 2020

@author: Fabian Bienz
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import csv

os.makedirs('plots', exist_ok=True)
csvfile = open('PAIND_IMU_only.csv', 'w', newline='')
spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Place', 'TrimSart', 'TrimEnd', 'Median', 'Mean', 'Std', 'Max', 'Min', '>5°'])

csvfile2 = open('PAIND_IMU_only_outliers.csv', 'w', newline='')
spamwriter2 = csv.writer(csvfile2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter2.writerow(['Ausreisser'])
    
print ("Base Folder Path")
baseFolderPath = input()


      
for i in range (1,2):    
    
    #Einlesen Drive
    
    fileImuAngleDrive = baseFolderPath+"/IMU_imu_only.bag.txt"
    fileNameImuAngleDrive = os.path.basename(fileImuAngleDrive)
    imuAngleDrive = pd.read_csv(fileImuAngleDrive)
    print("done")
    
    
    
    ##Drive Columns auslesen
    #IMU Drive
    driveRollX=imuAngleDrive["field.angular_velocity.z"]
    drivePitchY=imuAngleDrive["field.angular_velocity.y"]
    driveYawZ=imuAngleDrive["field.angular_velocity.x"]

    driveAngle=np.array([driveRollX, drivePitchY, driveYawZ])
    print(driveAngle)
    
    
    #Statistische Grössen
    """
    ##Einzel-Winkel
    #np.std(driveAngle, axis=1)
    print("Stadardabweichung[RollX,PitchY,YawZ]= " + str(np.std(driveAngle, axis=1)))
    #np.median(driveAngle,axis=1)
    print("Median[RollX,PitchY,YawZ]= " + str(np.median(driveAngle,axis=1)))
    #np.mean(driveAngle,axis=1)
    print("Mittelwert[RollX,PitchY,YawZ]= " + str(np.mean(driveAngle,axis=1)))
    
    
    #Boxplot
    #print(len(rollx))
    #print(len(rollx400))
    titleBoxplot = "Boxplot von" + fileNameImuAngleDrive "Roll X"
    driveRollX.plot(kind="box", title=titleBoxplot)
    
    titleBoxplot = "Boxplot von" + fileNameImuAngleDrive "Pitch Y"
    drivePitchY.plot(kind="box", title=titleBoxplot)
    
    
    #Entspircht Max Ausschlag in positive Drehrichtung
    #np.max(driveAngle, axis=1)
    print("Max[RollX,PitchY,YawZ]=" + str(np.max(driveAngle, axis=1)))
    #Entspircht Max Ausschlag in negative Drehrichtung
    #np.min(driveAngle, axis=1)
    print("Min[RollX,PitchY,YawZ]=" + str(np.min(driveAngle, axis=1)))
    
    #Histogramm
    #Fausregel sqrt(n-Observationen)
    driveRollX.plot(kind="hist", edgecolor="black", bins=20)
    plt.title("Histogramm: " +placeNumber"Drive "+i)     
    plt.xlabel("Winkel um x-Achse (Roll)")
    plt.ylabel("Anz. Messwerte")
    plt.show()
    
    drivePitchY.plot(kind="hist", edgecolor="black", bins=20)
    plt.title("Histogramm: " +placeNumber"Drive "+i)     
    plt.xlabel("Winkel um y-Achse (Pitch)")
    plt.ylabel("Anz. Messwerte")
    plt.show()
    """
    
    ##Gesamtwinkel berechnen
    alphaRadImuDrive=np.arccos(np.cos(np.radians(driveRollX))*np.cos(np.radians(drivePitchY)))
    alphaDegImuDrive=np.degrees(alphaRadImuDrive)
    #print(alphaDegImuDrive)
    
    #Verlauf plotten    
    plt.plot(alphaDegImuDrive)
    plt.title("Neigungswinkel: IMU_only_Drive")
    #plt.axis([0,len(alphaDegImuDrive),0,3.5])
    plt.xlabel('Index')
    plt.ylabel('Neigungswinkel alpha [°]')    
    plt.savefig("plots/Neigungswinkel: IMU_only_Drive")
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
    label="IMU_only_Drive" 
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
    titleBoxplot = "Boxplot: " +label
    df.plot(kind="box", title=titleBoxplot)
    plt.ylabel('Neigungswinkel alpha [°]')
    plt.savefig("plots/Boxplot: "+label)
    plt.close()
    #plt.show()
    
       
    #Histogramm
    #Fausregel sqrt(n-Observationen)
    trimAlphaDegImuDrive.plot(kind="hist", edgecolor="black", bins=int(np.sqrt(len(trimAlphaDegImuDrive))))
    plt.title("Histogramm: " +label)     
    plt.xlabel("Neigungswinkel alpha [°]")
    plt.ylabel("Anz. Messwerte")
    plt.savefig("plots/Histogramm: " +label)
    plt.close()
    #plt.show()
    
      
    v=1.42 ##[km/h]
    

csvfile.close()
csvfile2.close()
    
    
  

    
    
