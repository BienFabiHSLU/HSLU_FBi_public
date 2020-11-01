#include <stdio.h>

int main( int argc, char* argv[] )
{
	long long timeStamp = 0;
	int pressureVal = 0;
	char systemState = 0;
	char alarmState = 0;
	
	FILE *pRead = fopen("pressureSpike.bin", "rb");
	if( pRead != NULL)
	{
		while((timeStamp = getchar()) != EOF)	
		{
			fread(&timeStamp, sizeof(long long), 1, pRead);
			printf("timeStamp is: %lld\n", timeStamp);
			
			fread(&pressureVal, sizeof(int), 1, pRead);
			printf("pressureVal is: %d\n", pressureVal);
			
			fread(&systemState, sizeof(char), 1, pRead);
			printf("systemState is: %d\n", systemState);
			
			fread(&alarmState, sizeof(char), 1, pRead);
			printf("alarmState is: %d\n", alarmState);
		}
	}
	
	return 0;
}
