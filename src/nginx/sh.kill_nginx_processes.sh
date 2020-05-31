#ps aux | grep nginx | awk '{ print($1 " " $2 " " $11); }' | grep nginx | awk '{ print("sudo kill -9 " $2); }' | sh
ps aux | grep "nginx: master process nginx" | grep "root" | awk '{ print("sudo kill -QUIT " $2); }' | sh
