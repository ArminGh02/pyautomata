import sys
import subprocess


_image_viewer_cmd = {'linux': 'xdg-open',
                     'win32': 'explorer',
                     'darwin': 'open'}


def open(path: str) -> None:
    with subprocess.Popen([_image_viewer_cmd[sys.platform], path]):
        pass
