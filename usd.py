# usd.py

# Properties are registered into Blender like so:
# bpy.data.objects["Cube"].arnold.subdiv_iterations
#
# However, Blender's USD/Hydra Implementation requires primvars and attributes to be like so:
# bpy.data.objects["Cube"]["primvars:arnold:subdiv_iterations"]
#
# These set of functions help convert properties into a USD/Hydra compatible format.

import bpy, os


def make_id_prop(prop_name, default, convert=lambda x: x):
    def getter(self):
        return convert(self.id_data.get(prop_name, default))
    def setter(self, value):
        self.id_data[prop_name] = convert(value)
    return getter, setter


def make_enum_id_prop(prop_name, items, default_id):
    item_keys = [item[0] for item in items]
    indices = {key: i for i, key in enumerate(item_keys)}
    default_idx = indices.get(default_id, 0)

    def getter(self):
        return indices.get(
            self.id_data.get(prop_name, default_id),
            default_idx
        )

    def setter(self, value):
        self.id_data[prop_name] = item_keys[value]

    return getter, setter


PROPERTY_HANDLERS = {
    bpy.props.FloatProperty:        (0.0, lambda p, d: make_id_prop(p, d)),
    bpy.props.IntProperty:          (0,   lambda p, d: make_id_prop(p, d)),
    bpy.props.BoolProperty:         (False, lambda p, d: make_id_prop(p, d)),
    bpy.props.StringProperty:       ("", lambda p, d: make_id_prop(p, d)),
    bpy.props.FloatVectorProperty:  ((0.0, 0.0, 0.0),
                                     lambda p, d: make_id_prop(p, d, list)),
}


def USDProperty(*args, usd=None, type=None, **kwargs):
    if usd is None:
        usd, *args = args
    if type is None:
        type, *args = args

    if "items" in kwargs:
        default = kwargs.get("default", kwargs["items"][0][0])
        get_, set_ = make_enum_id_prop(usd, kwargs["items"], default)
    else:
        try:
            default, factory = PROPERTY_HANDLERS[type]
        except KeyError:
            raise TypeError(f"Unsupported property type: {type}")

        default = kwargs.get("default", default)
        get_, set_ = factory(usd, default)

    kwargs["get"] = get_
    kwargs["set"] = set_
    return type(*args, **kwargs)


def register_plugin():
    bpy.utils.expose_bundled_modules()

    import pxr.Plug

    path = os.path.join(
        os.environ.get("BTOA_ROOT", ""),
        "plugin"
    )

    if os.path.exists(path):
        pxr.Plug.Registry().RegisterPlugins([path])

def configure_hydra():
    scene = bpy.context.scene
    if scene is not None:
        scene.hydra.export_method = 'USD'
    return None
