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
