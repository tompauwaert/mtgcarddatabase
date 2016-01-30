from mock import MagicMock
from mock import patch
import sys
import __builtin__
import os.path


# Reference to the original open function.
g__test_utils__original_open = open

class FileMocker(object):
    """
    This class handles the mocking of files. If you register a file
    at a certain path to be mocked, this class will make sure that
    only files at that specific location are being mocked. Other non-registered
    files will be opened as if not mocked.

    If you request os.path.isfile on a file you registered for mocking,
    this class will also automatically do that upon registering of the file.
    """

    def __init__(self):
        """
        Initialize the mockfiles class.
        :return:
        """
        self._original_open = open
        self._original_isfile = os.path.isfile
        if sys.version_info[0] == 3:
            import _io
            self._file_spec = list(set(dir(_io.TextIOWrapper)).union(set(dir(_io.BytesIO))))
        else:
            self._file_spec = file

        self._files = {}

    def __enter__(self):
        self._patcher_files = patch.object(__builtin__, 'open', self._open_side_effect)
        self._patcher_files.start()

        self._patcher_path_isfile = patch('os.path.isfile', self._isfile_side_effect)
        self._patcher_path_isfile.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._patcher_files.stop()
        self._patcher_path_isfile.stop()

    def _open_side_effect(self, file_path, mode=''):
        """
        The side effect called when the mocked open is executed. (When we have
        __entered__). The side effect determines whether the file being opened
        is a file that should be mocked or a file that should not be mocked and
        handles each case appropriately.
        :param file_path: path to the file that is to be opened.
        :return: either the original file, or a mock for that file.
        """
        if file_path in self._files:
            return self._files[file_path].get_mock()
        else:
            return self._original_open(file_path, mode)

    def _isfile_side_effect(self, file_path):
        """
        This side effect is called when the os.path.isfile method is executed while
        the respective patcher is running. If the file is registered the provided 'exists'
        output for that file will be returned, otherwise the actual method will be called.
        :param file_path: path to the file
        :return: either the output of the original isfile, or the output as specified
        by the user upon registering the file.
        """
        if file_path in self._files:
            return self._files[file_path].file_exists()
        else:
            return self._original_isfile(file_path)


    def register_file(self, file_path, exists=True, read_data=''):
        """
        Register a new file to be mocked. If the file already existed
        the previous file will be overwritten!
        :param file_path: path to the file
        :param exists: True if the file should be 'existing' false if the
            file should be flagged as not existing yet.
        :param read_data: data to be set as the read value for the file mock
        """
        mock = self._create_file_mock(read_data)
        file_container = self.File(file_path, mock, read_data, exists)

        if self._files is None:
            self._files = {}

        self._files[file_path] = file_container

    def _create_file_mock(self, read_data):
        file_handle = MagicMock(spec=self._file_spec)
        file_handle.write.return_value = None
        file_handle.__enter__.return_value = file_handle
        file_handle.read.return_value = read_data
        return file_handle

    def __len__(self):
        """
        Returns the number of registered files in the
        Filemocker.
        :return:
        """
        return len(self._files)

    def __getitem__(self, file_path):
        """
        Returns the mocked file container associated
        with the given file_path
        :param file_path: key of the mocked file to retrieve.
        :return: A file container for the mocked file with given
        file_path. Contains the path, whether the file exists or not
        and the mock used for the file.
        """
        return self._files[file_path]

    def __iter__(self):
        return self._files.__iter__()



    class File(object):
        """
        A container around a mock file. Keeps information about the
        mocked file, such as data to present on a read, whether or not
        the file should already exist or not yet.
        """

        def __init__(self, path='', mock=None, read_data='', exists=True):
            """
            Create a new file object
            :param path: path to the file
            :param mock: mock for the file
            :param read_data: data that should be attached to the file.read()
            :param exists: whether the file should already exist or not.
            Determines the return value for the behind the scenes of mock of
            os.path.isfile()
            :return: a new file object
            """
            self._path = path
            self._mock = mock
            self._exists = exists
            self._read_data = read_data

        def get_path(self):
            return self._path

        def get_mock(self):
            return self._mock

        def file_exists(self):
            return self._exists

if __name__ == "__main__":
    with FileMocker() as file_mocker:
        file_mocker.register_file('a', True, 'a - content')
        file_mocker.register_file('b', False, 'b - different content')

        with open('a') as file_handle:
            print file_handle.read()

        with open('b') as file_handle:
            print file_handle.read()

        # with open('content.txt') as file_handle:
        #     print file_handle.read()

        # test isfile
        print 'a is file? %s' % os.path.isfile('a')
        print 'b is file? %s' % os.path.isfile('b')
        print 'content.txt is file? %s' % os.path.isfile('content.txt')

