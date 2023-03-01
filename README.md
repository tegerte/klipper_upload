# klipper_upload

Small Utility to automate gcode upload to klipper after slicing in e.g. PrusaSlicer. 

Inspired by [this thread on GitHub](https://github.com/Arksine/moonraker/discussions/128) I decided to create a small automation utility for improvement of my workflow for generating gcode and 3D-printing. I like to use  PrusaSlicer, and unfortunately it has no way to export gcode to a Creality SonicPad.

The script monitors a directory for newly generated 
gcode-files and uploads them to Klipper using Moonraker-API.
Find the docu of the file upload in Moonraker [here](https://moonraker.readthedocs.io/en/latest/web_api/#file-upload).

## shell scripts
A shell script for Linux users adds some convenience.
## "Fancy" mode
If you want the more fancy version with some cool sounds you can lunch the `run_klipper_upload_service_fancy.sh` wich activates sounds.
This might be a little hard to get that running on Windows as it uses the Linux application  [SoX](https://sox.sourceforge.net/sox.html)... (maybe try [this approach](https://www.codeproject.com/Articles/33901/Compiling-SOX-with-Lame-and-Libmad-for-Windows) to get that running on Windows)

On Linux you might have to install `sudo apt install sox` and run a `sudo apt install libsox-fmt-mp3` to install mp3-libs.

Sound effects are downloaded from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=6313">Pixabay</a> Thx!.

## Install 

If pipenv isn't installed on your system run 
```bash
pip install pipenv
```
Install your virtual env using pipenv by running
```bash
pipenv install 
pipenv shell
```


## Usage: 
```bash
<WHEREEVER _YOUR_VENVS_LIVE>/klipper_upload-cINr6ycz/bin/python
<WHEREEVER_YOUR_CODE_LIVES>
/gcode_upload_to_moonraker.py -d <YOUR_DIR_TO_MONITOR> -i <MOONRAKER_IP>"
```
## Command line params:

| short | long           | meaning                                           |
|-------|----------------|---------------------------------------------------|
| -i    | --ip_address   | IP-address of Moonraker                           |
| -d    | --observed_dir | directory to monitor for gcode files              |
| -f    | --fancy        | fancy mode, play sounds, optional, default =False |


