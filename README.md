# klipper_upload

Small Utility to automate gcode upload to klipper after slicing in PrusaSlicer. 

Inspired by [this thread on github](https://github.com/Arksine/moonraker/discussions/128) i decided to create a small automation utility for impreovement of my workflow if generating gcode and printig.

The script monitores a directory for newly generated 
gcode-files and uploads them to Klipper using Moonraker-API.
Find the docu of the file upload in Moonraker [here](https://moonraker.readthedocs.io/en/latest/web_api/#file-upload).

A shell script for Linux users adds some convenience.
If pipenv isn't installed on your system run 
```bash
pip install pipenv
```
Install your virtual env using pipenv by running
```bash
pipenv install 
pipenv shell
```

Usage: 
```bash
<WHEREEVER _YOUR_VENVS_LIVE>/klipper_upload-cINr6ycz/bin/python <WHEREEVER_YOUR_CODE_LIVES>/gcode_upload_to_moonraker.py -d <dir_to_watch> -i <Moonraker_ip>"
```
Command line params:

| short | long           | meaning                             |
|-------|----------------|-------------------------------------|
| -i    | --ip_adress    | IP-address of Moonraker             |
| -d    | --observed_dir | dirctory to momitor for gcode files |



