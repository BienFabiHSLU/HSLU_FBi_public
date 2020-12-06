#/bin/bash
mkdir txt;
for f in *.bag; do eval "rostopic echo -b $f -p /leica/position > txt/LEICA_$f.txt"; echo "Done $f";
 done 
