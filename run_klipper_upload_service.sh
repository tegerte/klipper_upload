#! /bin/sh
# here goes the directory to monitor for changed gcode files
dir_to_watch="/home/tassilo/3d_print/gcode/"
# the ip adress of your hardware running Moonraker
ip="192.168.1.165"
# for nice red error messages in console
RED='\033[0;31m'
GREEN='\033[92m'
NC='\033[0m' # No Color

echo "Klipper hardware's ip address is configured as $ip."
echo "Upload service starting...."
/home/tassilo/.local/share/virtualenvs/klipper_upload-cINr6ycz/bin/python /home/tassilo/programming/klipper_upload/gcode_upload_to_moonraker.py -d $dir_to_watch -i "$ip"
# echo $?
if [ $? -eq 10 ]; then
  echo "Uploader returned argument error"
  echo " > IP is configured as $ip"
  echo " > directory is configured as $dir_to_watch"
elif [ $? -eq 0 ]; then
  printf "${RED} Uhhhps!! Uploader returned error, check error messages above, exiting...${NC}\n }"
  exit 1
elif [ $? -eq 1 ]; then
  printf "${GREEN} Thanks for the session, bye...${NC}\n }"
  exit 1
fi

echo "Upload service listening for changes in directory:  $dir_to_watch\n"
