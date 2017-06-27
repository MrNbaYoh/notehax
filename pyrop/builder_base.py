import traceback
import os
import sys

modules_user_functions = dict()


def user_function(func):
    infos = func.__qualname__.rsplit('.', 1)
    modules_user_functions.setdefault(infos[0], dict())
    modules_user_functions[infos[0]][infos[1]] = func
    return func


class BaseBuilder:
    @classmethod
    def create(cls, name, *modules):
        def init(self):
            super(builder, self).__init__()

        builder = type(name, tuple(modules) + (cls,), {"__init__": init})
        return builder()

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance.chain = None
        instance.mem_offset = 0
        instance.loaded = False
        instance.built = False
        instance.user_functions = dict()
        return instance

    def __init__(self):
        for base in reversed(self.__class__.__mro__):
            base_user_func = modules_user_functions.get(base.__qualname__, dict())
            self.user_functions.update({name: base.__dict__[name].__get__(self, self.__class__)
                                        for name, func in base_user_func.items()})

    def set_mem_offset(self, offset):
        pass

    def append(self, other):
        pass

    def load(self, file):
        pass

    def build(self, file):
        pass


class BasicBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.chain = []
        self.mem_offset = 0

    @user_function
    def set_mem_offset(self, offset: int):
        self.mem_offset = offset

    def append(self, bytes_l):
        self.mem_offset += len(bytes_l)
        if self.loaded:
            self.chain += bytes_l

    def add_value(self, word: int, byte_size: int = 4):
        if byte_size < 1:
            raise ValueError("Size of word should be greater than zero!")

        bit_size = byte_size * 8
        if word.bit_length() > bit_size:
            raise ValueError("Value does not fit in a " + str(bit_size) + "bits word!")

        self.append((word if self.loaded else 0).to_bytes(byte_size, 'little'))

    @user_function
    def add_word(self, word):
        self.add_value(word, 4)

    @user_function
    def add_halfword(self, word):
        self.add_value(word, 2)

    @user_function
    def add_byte(self, byte):
        self.add_value(byte, 1)

    @user_function
    def incbin(self, incfile: str):
        self.append(open(incfile, 'rb').read())

    @user_function
    def org(self, address: int):
        if address < self.mem_offset:
            raise ValueError("Trying to ORG backwards!")

        self.append([0x0 for i in range(address - self.mem_offset)])

    @user_function
    def align(self, value: int):
        self.append([0 for i in range((value - (self.mem_offset % value)) % value)])

    @user_function
    def fill(self, size: int, value: int, v_byte_size: int = 1):
        if v_byte_size < 1:
            raise ValueError("Size of value should be greater than zero!")

        bit_size = v_byte_size * 8
        if value.bit_length() > bit_size:
            raise ValueError("Value does not fit in a " + str(bit_size) + "bits word!")

        self.append((value.to_bytes(v_byte_size, 'little') * ((size // v_byte_size) + 1))[:size])

    @user_function
    def add_ascii(self, string: str):
        self.add_str(string)

    @user_function
    def add_utf16(self, string: str):
        self.add_str(string, 'utf_16_le')

    @user_function
    def add_str(self, string: str, encoding: str = 'us-ascii'):
        self.append([c for c in string.encode(encoding)])

    def build(self, file):
        if self.built:
            raise PermissionError("You cannot build multiple times!")

        if not self.loaded:
            self.load(file)

        old = os.getcwd()
        sys.path.append(os.path.dirname(os.path.abspath(file)))  # for module import that aren't "include" call
        try:
            content = open(file, "rb").read()
            os.chdir(os.path.dirname(os.path.abspath(file)))  # set the current working directory, for open() etc.
            exec(compile(content, file, 'exec'), self.user_functions)
        except Exception as err:
            print("An exception occured while building: ", file=sys.stderr)
            lines = traceback.format_exc(None, err).splitlines()
            print("  " + lines[-1], file=sys.stderr)
            for l in lines[3:-1]:
                print(l, file=sys.stderr)
            exit(1)

        os.chdir(old)
        sys.path.remove(os.path.dirname(os.path.abspath(file)))
        self.built = True

    def load(self, file):
        if self.loaded:
            return

        sys.path.append(os.path.dirname(os.path.abspath(file)))  # for module import that aren't "include" call
        old = os.getcwd()
        try:
            content = open(file, "rb").read()
            os.chdir(os.path.dirname(os.path.abspath(file)))  # set the current working directory, for open() etc.
            exec(compile(content, file, 'exec'), self.user_functions)
        except Exception as err:
            print("An exception occured while loading: ", file=sys.stderr)
            lines = traceback.format_exc(None, err).splitlines()
            print("  " + lines[-1], file=sys.stderr)
            for l in lines[3:-1]:
                print(l, file=sys.stderr)
            exit(1)

        os.chdir(old)
        sys.path.remove(os.path.dirname(os.path.abspath(file)))
        self.loaded = True
        self.mem_offset = 0
