from collections import Iterable, Iterator
import math

def get_add(dict, name, default):
    res = dict[name] = dict.get(name, default)
    return res


def is_empty_str(s):
    return s is None or s==''


def bin_fixed_list(int, width):
    """ Return list of boolean values """
    assert int >= 0, str(int)
    assert int <= math.pow(2, width)-1, str(int)

    bits = [bool(b!='0') for b in bin(int)[2:]]

    extension_size = width - len(bits)

    assert extension_size >= 0, str(extension_size)

    extended_bits = [False]*extension_size + bits
    return extended_bits


def index_of(lambda_func, iterable):
    for i, e in enumerate(iterable):
        if lambda_func(e):
            return i
    return None


class StrAwareList(Iterable):
    def __str__(self):
        return str(self._output)


    def __len__(self):
        try:
            return getattr(self._output, "__len__")()
        except AttributeError:
            return 0


    def __iter__(self):
        for e in self._output:
            yield e


    def __init__(self, output=None):
        if output is None:
            output = []

        self._output = output


    def __iadd__(self, other):
        self.__add__(other)
        return self


    def __add__(self, other):
        if isinstance(other, Iterable) and not isinstance(other, str) and not isinstance(other, bytes):
            self._output.extend(other)
            return self
        else:
            self._output.append(other)
            return self


class FileAsStringEmulator:
    def __init__(self, file_writer):
        self._file_writer = file_writer
        self._len = 0

    def append(self, str):
        self._file_writer.write(str)
        self._file_writer.write('\n')
        self._len += 1


    def extend(self, strings):
        for str in strings:
            self.append(str)


    def __len__(self):
        return self._len
