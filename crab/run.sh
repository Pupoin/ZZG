i=0
while [ "x$i" == "x0" ]
do
    crab resubmit crab2018MC5/crab_ZZ_MC_2018/
    crab resubmit crab2018MC2/crab_ZZ_MC_2018/  
    sleep 1500
done
