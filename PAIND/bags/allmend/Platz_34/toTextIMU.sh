#/bin/bash
mkdir txt;
for f in *.bag; do eval "rostopic echo -b $f -p /vectornav/IMU > txt/IMU_$f.txt"; echo "Done $f";
 done 
