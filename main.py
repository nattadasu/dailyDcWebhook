from getopt import getopt, GetoptError
import sys
import os
import subprocess
import shutil
from extensions.hoyolab_checkin import hoyoverse_daily_checkin
from extensions.dailies import daily_images
# from extensions.server_reset import hoyoverse_server_reset_webhook

def main() -> None:
    """nattadasu/dailyDcWebhook - A private script collections for Natsu's needs in Discord.

License:
    GNU General Public License v3.0

Usage:
    python main.py [options]

Argv:
    -h, --help, -?: Show help message.
    --edit: Edit config.yaml.
    -c, --checkin: Check in to Hoyoverse's daily check in.
    -d, --daily: Send a daily message to Discord's webhook.
    --server-reset: Send a server reset message to Discord's webhook.
        valid options: sea, eu, na, tw, global (themis only)

Examples:
    >>> python main.py --edit
    >>> python main.py --checkin
    >>> python main.py --daily
    >>> python main.py --server-reset=sea"""

    try:
        opts, args = getopt(sys.argv[1:], 'h?cd', ['edit', 'help', 'checkin', 'daily', 'server-reset='])
    except GetoptError as e:
        print(e)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-h', '-?', '--help']:
            print(main.__doc__)
            sys.exit()
        # edit config.yaml
        elif opt in ['--edit']:
            # Determine available editors based on platform
            standard_editors = [ 'subl', 'code', 'atom', 'micro', 'nano', 'vim', 'vi']
            if os.name == 'nt':  # Windows
                available_editors =  ['notepad.exe'] + standard_editors
            elif os.name == 'posix':  # Linux and macOS
                available_editors = ['gnome-text-editor', 'gedit', 'kate', 'mousepad'] + standard_editors + ['emacs']
            else:
                print('Unsupported platform:', os.name)
                exit(1)

            # Check which editor is available
            editor = None
            for editor_candidate in available_editors:
                if shutil.which(editor_candidate) is not None:
                    editor = editor_candidate
                    break

            # Open the file with the selected editor
            if editor is not None:
                subprocess.run([editor, 'config.yaml'])
            else:
                print('No text editor found.')
                exit(1)


        elif opt in ['-c', '--checkin']:
            hoyoverse_daily_checkin()
        elif opt in ['-d', '--daily']:
            daily_images()
        # elif opt in ['-s', '--server-reset']:
        #     # arg must be one of the following: sea, eu, na, tw, global
        #     arg = arg.lower()
        #     if arg not in ['sea', 'eu', 'na', 'tw', 'global']:
        #         print(main.__doc__)
        #         sys.exit(2)
        #     hoyoverse_server_reset_webhook(arg) # type: ignore
        else:
            print(main.__doc__)
            sys.exit(2)


if __name__ == "__main__":
    main()
