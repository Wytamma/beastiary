echo $(ps -ewf | grep '[b]eastiary.cli' | awk '{ print $0 }') 

if [ $(ps -ewf | grep '[b]eastiary.cli' | awk '{ print $2 }' | wc -l) -gt 0 ]; then 
    kill $(ps -ewf | grep '[b]eastiary.cli' | awk '{ print $2 }'); 
fi 
# wait