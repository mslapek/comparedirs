from argparse import ArgumentParser

from colorama import Fore, init

from comparedirs import CompareDirs
from comparedirsprinter import COLORS_COLORED, print_on_terminal


# pylint: disable=too-few-public-methods
class Main:
    def __init__(self, args):
        self._ignore_list = []
        if args.ignore_list is not None:
            self._read_ignore_patterns(args.ignore_list)

        self.comparer = CompareDirs()
        self.comparer.dir1 = args.dir1
        self.comparer.dir2 = args.dir2
        self.comparer.ignore_list = self._ignore_list

        self._assumeyes = args.assumeyes
        self._copy_dir1_to_dir2 = args.copy_dir1_to_dir2

    def main(self):
        try:
            self.comparer.calculate_differences()
        except OSError as error:
            _print_error(error)
        else:
            print_on_terminal(self.comparer, palette=COLORS_COLORED)
            if self._copy_dir1_to_dir2:
                self._ask_to_copy_files()

    def _read_ignore_patterns(self, ignore_patterns_path):
        with open(ignore_patterns_path) as file:
            self._ignore_list = [line.strip() for line in file]

    def _ask_to_copy_files(self):
        if self.comparer.dir1_additional:
            response = self._ask('Copy additional files from ' +
                                 self.comparer.dir1 + ' to ' +
                                 self.comparer.dir2 + '? [n]/y: ')
            if response in ['y', 'yes']:
                try:
                    self.comparer.copy_from_dir1()
                except OSError as error:
                    _print_error(error)
                else:
                    print(Fore.GREEN + 'Copied files.' + Fore.RESET)
            else:
                print(Fore.CYAN + 'Nothing changed.' + Fore.RESET)

    def _ask(self, msg):
        if self._assumeyes:
            return True
        else:
            response = input(msg)
            return response in ['y', 'yes']


def _print_error(error):
    print(Fore.RED + 'Exception: ' + error.strerror + ': ' + Fore.RESET +
          error.filename)


def main():
    init()
    parser = ArgumentParser()
    parser.add_argument('dir1', help='path to first directory')
    parser.add_argument('dir2', help='path to second directory')
    parser.add_argument('--ignore-list', help='path to file with ignore list')
    parser.add_argument(
        '--copy-dir1-to-dir2',
        help=
        'perform copy of missing files from first directory to second directory',
        action='store_true')
    parser.add_argument(
        '-y',
        '--assumeyes',
        help=
        'assume yes; assume that the answer to any question which would be asked is yes',
        action='store_true')
    args = parser.parse_args()

    main_object = Main(args)
    main_object.main()


if __name__ == '__main__':
    main()
