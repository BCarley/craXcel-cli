import argparse
import os

from craxcel import constants as C
from craxcel.main import (
    APP_SAVE_DIR,
    APP_TEMP_DIR,
    FileInfo,
    MicrosoftExcel,
    MicrosoftPowerpoint,
    MicrosoftWord,
    read_list_of_filepaths,
)


def handle_args():
    """
    Handles the command line arguments passed in by the user, returns them
    as an args object.
    """
    parser = argparse.ArgumentParser(
        description='Remove Workbook and Worksheet protection on Microsoft Excel files.'
    )
    parser.add_argument('filepath', help='Target filepath')

    excel_group = parser.add_mutually_exclusive_group()
    excel_group.add_argument(
        '-ws',
        '--worksheet',
        action='store_true',
        help='microsoft excel files: unlocks the Worksheets only (leaves Workbook Protection intact)',
    )
    excel_group.add_argument(
        '-wb',
        '--workbook',
        action='store_true',
        help='microsoft excel files: unlocks the Workbook only (leaves Worksheet Protection intact)',
    )

    parser.add_argument(
        '-vba',
        '--vba',
        action='store_true',
        help='removes projection from the VBA project of the file',
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='retains the temp folder. Useful for dubugging exceptions',
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='unlock a list of files specified in a line-seperated .txt file',
    )

    return parser.parse_args()


def create_directory_structure():
    """
    Creates the directory structure if it doesn't already exist.
    """
    if not os.path.exists(APP_SAVE_DIR):
        os.mkdir(APP_SAVE_DIR)

    if not os.path.exists(APP_TEMP_DIR):
        os.mkdir(APP_TEMP_DIR)


def main():
    """
    Main entry point of the application.
    """
    args = handle_args()

    print('\ncraXcel started')
    create_directory_structure()

    if args.list:
        print('\nList mode enabled')
        filepaths = read_list_of_filepaths(args.filepath)
        print(f'{len(filepaths)} files detected')
    else:
        filepaths = [args.filepath]

    files_unlocked = 0
    for locked_filepath in filepaths:
        print(f'\nChecking file {locked_filepath}...')

        if os.path.isfile(locked_filepath):
            file_info = FileInfo(locked_filepath)

            # Checks the extension of the file against the dictionary of
            # supported applications, returning the application name.
            try:
                detected_application = C.SUPPORTED_EXTENSIONS[file_info.extension]
            except KeyError:
                detected_application = 'unsupported'

            # Uses the deteted application to create the correct instance.
            if detected_application == C.MICROSOFT_EXCEL:
                cxl = MicrosoftExcel(args, locked_filepath)
            elif detected_application == C.MICROSOFT_WORD:
                cxl = MicrosoftWord(args, locked_filepath)
            elif detected_application == C.MICROSOFT_POWERPOINT:
                cxl = MicrosoftPowerpoint(args, locked_filepath)
            elif file_info.extension == '.txt':
                print(
                    'File rejected. Did you mean to use list mode? Try "python craxcel.py --help" for more info.'
                )
                break
            else:
                print('File rejected. Unsupported file extension.')
                break

            print('File accepted...')

            try:
                cxl.unlock()
                files_unlocked += 1
            except Exception as exc:
                print(exc)
                print(f'An error occured while unlocking {locked_filepath}')

        else:
            print('File not found...')

    print(f'\nSummary: {files_unlocked}/{len(filepaths)} files unlocked')
    print('\ncraXcel finished')


if __name__ == "__main__":
    main()
