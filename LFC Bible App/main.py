from typing import Callable
import pyuac
import pywintypes
import sys
import os
from App import BibleApp

def run_as_admin(main: Callable):
    """
    Helper function in order to make running this as admin a bit more easier
    It does the following:
    - Makes admin request to the user for the app
    - Handles all errors from cancelation of admin request
    - Removes temp files from the failure of admin request
    - Gives the app admin priveledges if admin request is approved
    
    Parameters:
    - main: The main function of the application
    """
    @pyuac.main_requires_admin
    def code():
        main()

    if __name__ == '__main__':
        if not pyuac.isUserAdmin():
            try:
                code()
            except (pywintypes.error, PermissionError):
                sys.exit()
            except AttributeError:
                stdout_temp_fn = 'pyuac.stdout.tmp.txt'
                stderr_temp_fn = 'pyuac.stderr.tmp.txt'
                if os.path.exists(stdout_temp_fn):
                    os.remove(stdout_temp_fn)
                if os.path.exists(stderr_temp_fn):
                    os.remove(stderr_temp_fn)
        else:
            code()

def main():
    app = BibleApp()
    app.run()

# Runs code normally
# main()
# Runs Code as admin
run_as_admin(main)


