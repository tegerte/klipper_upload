#! /bin/sh
# Fancy version with some sounds...enjoy ;-)
# here goes the directory to monitor for changed gcode files
dir_to_watch="/home/tassilo/3d_print/gcode/"
# the ip adress of your hardware running Moonraker
ip="192.168.1.165"
# for nice red error messages in console
RED='\033[0;31m'
NC='\033[0m' # No Color
# Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=6313">Pixabay</a>
echo "Klipper hardware's ip address is configured as $ip."
# you might need to install sudo apt install libsox-fmt-mp3
play  tada-fanfare-a-6313.mp3 --no-show-progress -V0
echo "Upload service starting...."
/home/tassilo/.local/share/virtualenvs/klipper_upload-cINr6ycz/bin/python /home/tassilo/programming/klipper_upload/gcode_upload_to_moonraker.py -d $dir_to_watch -i "$ip" --fancy
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
