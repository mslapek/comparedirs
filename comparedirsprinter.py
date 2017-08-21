from colorama import Fore

COLORS_COLORED = {
    'none': Fore.CYAN,
    'left': Fore.YELLOW,
    'right': Fore.GREEN,
    'reset': Fore.RESET
}

COLORS_OFF = {'none': '', 'left': '', 'right': '', 'reset': ''}


def print_on_terminal(comparer, palette=None):
    if palette is None:
        palette = COLORS_OFF

    if not comparer.dir1_additional and not comparer.dir2_additional:
        print(palette['none'] + 'No differences.' + palette['reset'])
    else:
        if comparer.dir1_additional:
            print('Directory ' + comparer.dir1 + ':')
            _print_files(comparer.dir1_additional, '<< ', 'left', palette)

        if comparer.dir2_additional:
            print('Directory ' + comparer.dir2 + ':')
            _print_files(comparer.dir2_additional, '>> ', 'right', palette)


def _print_files(files, trim, side, palette):
    for file in files:
        print(trim + palette[side] + file + palette['reset'])
