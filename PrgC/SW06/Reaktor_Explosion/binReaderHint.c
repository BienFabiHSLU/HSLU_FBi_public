#include <stdio.h>
#include <stdlib.h>
long long ComputePrintBinary(int);

int main(int argc, char *argv[]){
	//Beispiel von Adrian
	//long long timestamp = 0;

	
	/*FILE *fid = fopen("pressureSpike.bin", "rb");

	if( fid != NULL )
	{
		fread(&timestamp, sizeof(long long), 1, fid);
		printf("time stamp: %lld\n", timestamp);
	}*/
	
	
	
	
	long long timeStamp = 0;
	int pressureVal = 0;
	char systemState = 0;
	char alarmState = 0;
	long long systemStateBin = 0;
	long long oldTimeStamp = 1;		// Muss zum Starten ungeleich 0 sein!
	
	
	
	FILE *pRead = fopen("pressureSpike.bin", "rb");
	FILE *pWrite = fopen("pressureSpike.csv", "w");	//CSV File erstellt um die ausgelesenen Daten reinzuschreiben
	
	

	if( pRead != NULL && pWrite != NULL ) 
	{	
		fprintf(pWrite, "timeStamp,pressureValue,systemState,alarmState\n");
		
		while(timeStamp != oldTimeStamp)	//Abfangen mit end of file (EOF) hat nicht funktioniert?! Wo befindet sich das EOF genau? Daher wird hier das while mit dem Vergelich zum vorherigen timestamp abgefange, sobald oldTimeStamp=timeStamp
		{	
			oldTimeStamp=timeStamp;
			
			fread(&timeStamp, sizeof(long long), 1, pRead);
			//printf("time stamp: %lld\n", timeStamp);
							
			fread(&pressureVal, sizeof(int), 1, pRead);
			//printf("pressureVal: %d\n", pressureVal);
		
			fread(&systemState, sizeof(char), 1, pRead);
			//printf("systemState: %d\n", systemState);
		
			fread(&alarmState, sizeof(char), 1, pRead);
			//printf("alarmState: %d\n\n", alarmState);
			
			
			systemStateBin=ComputePrintBinary(systemState);		//number to Binär konverter, damit im CSV der Status der Pumpen und Ventile sofort aus der Binären schreibweise abgelesen werden kann
			
			if (timeStamp != oldTimeStamp) 	// Da das Abfangen des While verzögert ist wird letzter timeStamp 2 mal geschrieben, hiermit wird dies verhindert
			{
				fprintf(pWrite, "%lld,%d,%lld,%u\n", timeStamp, pressureVal, systemStateBin, alarmState); // Schreiben des CSV
			}
		}
	fclose(pRead);
	fclose(pWrite);	// In der if clause, weil fclose von einem leeren pointer fehler generiert	
	}
	
	printf("Done");	
	return 0;
	
	
	
	
}

long long ComputePrintBinary(int n) // long long weil Output eine sehr grosse Dezimalzahl ergeben kann!
{
	long long bin = 0;
	int rem = 0, i = 1;
	

	while(n != 0)
	{
		rem = n % 2;
		n = n / 2;
		bin = bin + rem * i;
		i = i *10;		// Hilfsvariable um Binäre ausgabe als Dezimalzahl zu erzeugen
	}
	return bin;
}

