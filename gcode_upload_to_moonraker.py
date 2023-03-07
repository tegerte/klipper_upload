"""
Utility for making upload to Creality Sonic Pad (Or any other device that runs moonraker API).
Sound effects from Pixabay.
"""

import os
import signal
import time
import requests
import argparse
from subprocess import Popen
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

PATTERNS = ["*.gcode"]
COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

ignore_patterns = None
ignore_directories = False
case_sensitive = True
go_recursively = True

my_event_handler = PatternMatchingEventHandler(
    PATTERNS, ignore_patterns, ignore_directories, case_sensitive
)
my_observer = Observer()


def get_size(path):
    size = path.stat().st_size
    if size < 1024:
        return f"{size} bytes"
    elif size < pow(1024, 2):
        return f"{round(size / 1024, 2)} KB"
    elif size < pow(1024, 3):
        return f"{round(size / (pow(1024, 2)), 2)} MB"
    elif size < pow(1024, 4):
        return f"{round(size / (pow(1024, 3)), 2)} GB"


def upload_gcode(path_to_file: Path) -> tuple[int, str]:
    """
    Uses the API of Moonraker to upload a file to Klipper. Its checked in response if the uploaded filename is
    returned as indication of successful upload.

    :param path_to_file: Path-opbj
    :return: tuple errorcode, errormessage
    """
    file_path = Path(path_to_file)
    print(f"\nInitiating  upload to {cl_args.ip_address} !")
    if cl_args.fancy:
        play_fancy_sounds()

    with open(path_to_file, "rb") as gcode:
        pload = {"file": gcode, "print": "false"}
        print(
            f"~~~~~ Starting upload of {get_size(file_path)} to moonraker  ~~~~~~~~~~~~~~~~~"
        )
        try:
            r = requests.post(
                f"http://{cl_args.ip_address}/server/files/upload", files=pload
            )
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            return 11, str(errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            return 12, str(errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            return 13, str(errt)
        except requests.exceptions.RequestException as e:
            # catastrophic error...
            print(f"Something went really wrong, error message: {e}")
            return 100, "Apokalypse"
    if cl_args.debug:
        print("\n Return from API was:\n")
        print(r.json())

    if r != "" and r.json()["item"]["path"] == file_path.name:
        print(
            COLOR["GREEN"],
            f"~~~~~ Successfully uploaded new gcode file to moonraker  ~~~~~~~~~~~~~~~~~\n"
            f"Upload took {r.elapsed.seconds} seconds",
            COLOR["ENDC"],
        )
        return 0, ""
    return 1, "some other error"


def play_fancy_sounds():
    # do not show any distracting SoX output
    cmd_args = "" if cl_args.debug else " --no-show-progress -V0"
    cmd_cntdown = "play sounds/female-robotic-countdown-5-to-1-47653.mp3" + cmd_args
    cmd_fany_spaceship_sound = "play sounds/space-ship-soaring-81591.mp3" + cmd_args
    # Popen starts those processes in parallel wich gives a cool overlay ;-)
    Popen(cmd_cntdown, shell=True)
    time.sleep(0.4)
    Popen(cmd_fany_spaceship_sound, shell=True)


def on_created(event):
    print(f"hey ho, new gcode {event.src_path} has been created!")
    ret = upload_gcode(event.src_path)
    handle_upload_return(ret)


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")


def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")


def on_moved(event):
    print(f"Hey, i think PrucaSlicer created some nice gcode {event.dest_path} !")
    # the way PrisaSlicer generates the files...
    ret = upload_gcode(event.dest_path)
    handle_upload_return(ret)


def handle_upload_return(ret: tuple[int, str]) -> None:
    """
    simple helper to handle the return of uploading function.
    :param ret: return tuple of uploader
    :return: None
    """
    if ret[0] > 0:
        print(COLOR["RED"], f"Sh..., that didn't work, exiting...", COLOR["ENDC"])
        # that is not so nice, but we're in a threaded process so simply exiting will not work
        os.kill(os.getpid(), signal.SIGINT)
    else:
        print("Waiting for next job...")


def handle_cl():
    """
    Handels the command line stuff.
    :return: the args given on command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip_address")
    parser.add_argument("-d", "--observed_dir")
    parser.add_argument(
        "-f", "--fancy", action=argparse.BooleanOptionalAction, default=False
    )
    parser.add_argument(
        "-db", "--debug", action=argparse.BooleanOptionalAction, default=False
    )
    try:
        return parser.parse_args()

    except argparse.ArgumentError:
        return None


def main():
    os.system("")
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path_gcode = cl_args.observed_dir
    print(
        f"Listening for changes in {path_gcode} to upload to {cl_args.ip_address}... "
    )
    my_observer.schedule(my_event_handler, path_gcode, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()
    exit(1)


if __name__ == "__main__":
    cl_args = handle_cl()
    if not cl_args:
        exit(0)
    main()
