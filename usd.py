def make_id_prop(prop_name, default):
    def getter(self):
        return self.id_data.get(prop_name, default)
    def setter(self, value):
        self.id_data[prop_name] = value
    return getter, setter


def make_vector_id_prop(prop_name, default):
    def getter(self):
        val = self.id_data.get(prop_name, default)
        return list(val)
    def setter(self, value):
        self.id_data[prop_name] = list(value)
    return getter, setter


def make_enum_id_prop(prop_name, items, default_id):
    item_keys = [item[0] for item in items]
    default_idx = item_keys.index(default_id) if default_id in item_keys else 0

    def getter(self):
        val = self.id_data.get(prop_name, default_id)
        if val in item_keys:
            return item_keys.index(val)
        return default_idx

    def setter(self, value):
        self.id_data[prop_name] = item_keys[value]

    return getter, setter

def USDProperty(*args, usd=None, type=None, **kwargs):
    # Handle positional arguments for usd and type if they are not keyword arguments
    if usd is None and len(args) > 0:
        usd = args[0]
        args = args[1:]
    if type is None and len(args) > 0:
        type = args[0]
        args = args[1:]

    if usd is None:
        raise TypeError("USDProperty is missing required argument 'usd'")
    if type is None:
        raise TypeError("USDProperty is missing required argument 'type'")

    type_name = type.__name__ if hasattr(type, '__name__') else str(type)
    default = kwargs.get('default')

    # Assign appropriate getters/setters based on property type
    if type_name == 'EnumProperty' or 'items' in kwargs:
        items = kwargs.get('items', [])
        if default is None:
            default = items[0][0] if items else ""
        get_func, set_func = make_enum_id_prop(usd, items, default)
    elif 'VectorProperty' in type_name:
        if default is None:
            default = (0.0, 0.0, 0.0)
        get_func, set_func = make_vector_id_prop(usd, default)
    else:
        if default is None:
            if type_name == 'FloatProperty':
                default = 0.0
            elif type_name == 'IntProperty':
                default = 0
            elif type_name == 'BoolProperty':
                default = False
            elif type_name == 'StringProperty':
                default = ""
        get_func, set_func = make_id_prop(usd, default)

    kwargs['get'] = get_func
    kwargs['set'] = set_func

    return type(*args, **kwargs)
