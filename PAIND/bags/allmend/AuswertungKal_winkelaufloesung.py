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
from glob import glob 

os.makedirs('plots', exist_ok=True)
csvfile = open('PAIND_Kalib_winkelaufl.csv', 'w', newline='')
spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Place', 'TrimSart', 'TrimEnd', 'Median', 'Mean', 'Std', 'Max', 'Min'])


    
print ("Base Folder Path")
baseFolderPath = input()

##Grenzen definieren (Daten Trimmen)
print ("Enter lower limit")
n = input()
print ("Enter upper limit")
m = input()

for i in [0,2.5,5,10,15,20]:

	
	for f in glob(baseFolderPath+"/IMU_winkel"+str(i)+"X7_*bag.txt"): 
		
	    #Einlesen Winkel X
	    imuAngle = pd.read_csv(f)
	    print("done " +f)
	    
	    RollX=imuAngle["field.angular_velocity.z"]
	    
	    
	   
	       
	    ###RollX
	    
	    label= "IMU_winkel"+str(i)+"X"
	    
	    #Untere Anz. n Messwerte aussortieren
	    trimRollX=RollX[int(n) :]
	    #Obere Anz. m Messwerte aussortieren
	    trimRollX=trimRollX[: len(trimRollX)-int(m)]
	       
	    ##Statistische Grössen
	    
	    std=np.std(trimRollX)
	    print("Stadardabweichung[alpha]= " + str(std))
	    median = np.median(trimRollX)
	    print("Median[alpha]= " + str(median))
	    mean=np.mean(trimRollX)
	    print("Mittelwert[alpha]= " + str(mean))
	    
	    #Entspircht Max Neigungswinkel
	    maxi=np.max(trimRollX)
	    print("Max[alpha]=" + str(maxi))
	    #Entspricht Min Neigungswinkel
	    mini=np.min(trimRollX)
	    print("Min[alpha]=" + str(mini))
	    
	    	    
	    #spamwriter.writerow(['Place', 'TrimSart', 'TrimEnd', 'Median', 'Mean', 'Std', 'Max', 'Min'])
	    spamwriter.writerow([label, n, m, median, mean, std, maxi, mini])
	    
	    
	   
	    
	        
	      
	    v=1.42 ##[km/h]
	   

csvfile.close()


 

    
