from builder_base import user_function, BaseBuilder
from ast import *
from inspect import *
import traceback

# def get_module(builder, module):
#     return type(module.__name__ + builder.__name__, (module, builder,), dict(module.__dict__))


class IncludeModule(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.current_path = ""

    def set_current_path(self, base_path):
        self.current_path = os.path.dirname(os.path.abspath(base_path))

    @user_function
    def include(self, incfile: str):

        old = self.current_path
        self.current_path = os.path.join(old, os.path.dirname(incfile))

        path = os.path.join(self.current_path, os.path.basename(incfile))
        sys.path.append(self.current_path)

        try:
            content = open(path, "rb").read()
            os.chdir(self.current_path)  # set the current working directory, for open() etc.
            exec(compile(content, path, 'exec'), self.user_functions)
        except Exception as err:
            print("An exception occured while building: ", file=sys.stderr)
            lines = traceback.format_exc(None, err).splitlines()
            print("  " + lines[-1], file=sys.stderr)
            for l in lines[3:-1]:
                print(l, file=sys.stderr)
            exit(1)

        sys.path.remove(self.current_path)
        os.chdir(old)
        self.current_path = old

    def load(self, file):
        self.set_current_path(file)
        super().load(file)


class AreaModule(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.areas = []

    @user_function
    def append(self, bytes_l):
        super().append(bytes_l)
        self.check_areas()

    @user_function
    def begin_area(self, size):
        if not self.loaded:
            return
        self.areas.append((len(self.chain), size))

    @user_function
    def end_area(self):
        if not self.loaded:
            return
        self.areas.pop()

    def check_areas(self):
        for area in self.areas:
            if len(self.chain)-area[0] > area[1]:
                raise OverflowError("Area overflowed!")


class LabelContext:
    def __init__(self, parent, l_locals):
        self.locals = l_locals
        self.parent = parent

    def setdefault(self, key, value):
        self.locals.setdefault(key, value)

    def __getitem__(self, item):
        """
        Return the value associated to the label name in the nearest context that contains it.
        (search in context then context's parent and then parents of context's parent...)
        :param item: label name
        :return: address associated to the label
        """
        current = self
        while current is not None:
            if item in current.locals:
                return current.locals[item]
            current = current.parent

    def __contains__(self, item):
        """
        Override 'in' operator, search the label in the local dict and all the parents dicts.
        :param item: label to search
        :return: True if label is found, False otherwise
        """
        current = self
        while current is not None:
            if item in current.locals:
                return True
            current = current.parent
        return False


class Macro:

    def __init__(self):
        self.total_count = 0
        self.current_instance = 0
        self.instance_contexts = []

    def add_instance(self, context):
        """
        Add a new instance.
        :param context: instance label context
        :return: None
        """
        self.instance_contexts.append(context)
        self.total_count += 1

    def reset_current_instance(self):
        """
        Reset the current_instance counter.
        :return: None
        """
        self.current_instance = 0

    def get_last_instance(self):
        """
        Get the last instance added.
        :return: macro's last instance
        """
        return self.instance_contexts[-1]

    def get_next_instance(self):
        """
        Get the current instance, then increment the current_instance value.
        :return: current instance label context
        """
        self.current_instance += 1
        return self.instance_contexts[self.current_instance - 1]


class LabelModule(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.context_stack = []

        self.global_context = dict()
        self.current_context = self.global_context

        self.macros = dict()

    def load(self, file):
        self.parse_labels(open(file).read())
        self.user_functions.update(self.global_context)
        super().load(file)
        self.user_functions.update(self.global_context)

    def __setitem__(self, name: str, address: int):
        """
        Add a label to the current context.
        Override [] assignment.
        :param name: label name
        :param address: label address
        :return: None
        """
        if self.loaded:
            return

        if address is None:
            address = self.mem_offset
        elif address.bit_length() > 32:
            raise ValueError("Label address should be 32 bits long!")

        self.current_context[name] = address
        self.user_functions.update(self.current_context)

    def __getitem__(self, name):
        """
        Get address associated to the label name in current_context.
        :param name: label name
        :return: address associated to label
        """
        if name not in self.current_context:
            raise KeyError("Trying to use an undefined label!")
        return self.current_context[name]

    def __contains__(self, item):
        """
        Override 'in' operator.
        :param item: label name
        :return: True if current_context contains the label, False otherwise
        """
        return item in self.current_context

    def get_current_context(self):
        return self.current_context

    def register_macro(self, name: str):
        """
        Register a new macro in the macros dict.
        :param name: macro's name
        :return: None
        """
        self.macros.setdefault(name, Macro())

    def add_macro_context(self, name: str, context: dict = None):
        """
        Add a new instance/context to a Macro object
        :param name: macro's name
        :param context: macro's label context, default = dict()
        :return: None
        """
        if context is None:
            context = dict()
        self.macros[name].add_instance(dict())

    def switch_context(self, context):
        """
        Switch the current context.
        :param context: the new context
        :return: None
        """
        self.context_stack.append(self.current_context)
        self.current_context = context

    def restore_context(self):
        """
        Restore the previous context.
        :return: None
        """
        self.current_context = self.context_stack.pop()

    @user_function
    def put_label(self, name: str, address: int = None):
        if type(name) is not str:
            raise ValueError("Label name expected, " + type(name).__name__ + " was given!")
        self[name] = address

    @user_function
    def get_label(self, name: str):
        return self[name]

    def parse_labels(self, source):
        tree = parse(source, "<ast>", 'exec')
        for node in walk(tree):
            if isinstance(node, Call):
                id = node.func.id if isinstance(node.func, Name) else node.func.attr
                if id == "put_label" and node.args and isinstance(node.args[0], Str):
                    name = node.args[0].s
                    if name in self.current_context:
                        raise NameError("Label name already used!")
                    self.current_context.setdefault(name, 0)



    @user_function
    def macro(self, func):
        """
        The macro function decorator.
        :param func: macro function
        :return: the wrapped function
        """
        self.register_macro(func.__name__)

        def wrapper(*args, **kwargs):
            old = func.__globals__.copy()
            for key in self.current_context.keys():
                del func.__globals__[key]

            if not self.loaded:
                self.add_macro_context(func.__name__)
                self.switch_context(self.macros[func.__name__].get_last_instance())
                self.parse_labels(getsource(func))

            else:
                self.switch_context(self.macros[func.__name__].get_next_instance())

            func.__globals__.update(self.current_context)
            func(*args, **kwargs)
            func.__globals__.clear()
            func.__globals__.update(old)

            self.restore_context()

        wrapper.original = func.original if hasattr(func, 'original') else func
        return wrapper


class PopModule(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.pop_macros = dict()
        self.current_count = 0

    def append_stub(self, other):
            self.current_count += len(other)

    @user_function
    def pop_macro(self, func):
        wrapped_func = func
        original_func = func.original if hasattr(func, 'original') else func

        args = signature(original_func).parameters.keys()
        if set(args) - {"r"+str(i) for i in range(16)}:
            raise Exception("Non register argument found in pop_macro!")

        self.current_count = 0
        append = self.append
        self.append = self.append_stub

        wrapped_func(**({name: 0 for name in args}))
        self.append = append

        self.pop_macros[original_func.__name__] = (func, set(args), self.current_count)
        return func

    @user_function
    def pop(self, **registers):
        reg_set = set(registers.keys())
        if reg_set - {"r"+str(i) for i in range(16)}:
            raise Exception("Trying to pass non register argument to a pop_macro!")
        candidates = {name: infos for name, infos in self.pop_macros.items() if infos[1] & reg_set}
        pop_stack = []
        while reg_set:
            pop_stack.append(self.find_best(candidates, reg_set))
            if pop_stack[-1] is None:
                raise Exception("Could not find pop_macro to pop register(s): " + str(reg_set))
            reg_set -= self.pop_macros[pop_stack[-1]][1]
        for func in pop_stack:
            candidates[func][0](**{reg: registers.get(reg, 0x0) for reg in candidates[func][1]})
            # if the value to pop isn't specified, then pop 0x0, for example when you only have pop {r2-r6, pc} to pop
            # r2 then 0x0 will be popped to r3-r6
        print(pop_stack)

    @staticmethod
    def find_best(candidates, regs):
        name = None
        best_rate = 0
        total_pop = 16
        for func, infos in candidates.items():
            nb = len(regs & infos[1])
            rate = nb/infos[2]
            if nb == 0:
                continue
            if best_rate < rate or (best_rate == rate and len(infos[1]) <= total_pop):
                name = func
                best_rate = rate
                total_pop = len(infos[1])
        return name
