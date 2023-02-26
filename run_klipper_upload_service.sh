#! /bin/sh
dir_to_watch="/home/tassilo/3d_print/gcode/"
ip="192.168.1.165"
RED='\033[0;31m'
NC='\033[0m' # No Color
echo "Klipper hardware's ip address is configured as $ip."
echo "Upload service starting...."
/home/tassilo/.local/share/virtualenvs/klipper_upload-cINr6ycz/bin/python /home/tassilo/programming/klipper_upload/gcode_upload_to_moonraker.py -d $dir_to_watch -i "$ip"
# echo $?
if [ $? -eq 10 ];
  then
    echo "Uploader returned argument error"
    echo " > IP is configured as $ip"
    echo " > directory is configured as $dir_to_watch"
  else [ $? -eq 0 ];
    printf "${RED} Uhhhps!! Uploader returned error, check error messages above, exiting...${NC}\n }"
    exit 1
fi

echo "Upload service listening for changes in directory:  $dir_to_watch\n"
