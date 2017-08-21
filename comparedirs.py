from fnmatch import fnmatch
from os import walk
from os.path import join, relpath
from shutil import copyfile


class CompareDirs:
    def __init__(self):
        self.dir1 = None
        self.dir2 = None
        self.dir1_additional = None
        self.dir2_additional = None
        self.ignore_list = []

    def calculate_differences(self):
        dir1_files = self._get_files_set(self.dir1)
        dir2_files = self._get_files_set(self.dir2)
        self.dir1_additional = list(dir1_files - dir2_files)
        self.dir2_additional = list(dir2_files - dir1_files)

    def copy_from_dir1(self):
        _copy_files_comparer(self.dir1, self.dir2, self.dir1_additional)
        self.dir1_additional = []

    def copy_from_dir2(self):
        _copy_files_comparer(self.dir2, self.dir1, self.dir2_additional)
        self.dir2_additional = []

    def _get_files_generator(self, top):
        for root, _, filenames in walk(top, onerror=_raise_error):
            relroot = relpath(root, top)
            for filename in filenames:
                if relroot == '.':
                    fullname = filename
                else:
                    fullname = join(relroot, filename)
                if self._is_valid_filename(fullname):
                    yield fullname

    def _is_valid_filename(self, fullname):
        for pattern in self.ignore_list:
            if fnmatch(fullname, pattern):
                return False

        return True

    def _get_files_set(self, top):
        return set(self._get_files_generator(top))


def _copy_files_comparer(src, dest, files):
    for filepath in files:
        file_src = join(src, filepath)
        file_dest = join(dest, filepath)
        copyfile(file_src, file_dest)


def _raise_error(error):
    raise error
