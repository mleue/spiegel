# TODO make this robust
# TODO filter magic methods right here?
# TODO write tests for this
# TODO get all public attributes on class/object?

def get_methods_on_class(cls):
    return [name for name, obj in vars(cls).items() if callable(obj)]


def get_properties_on_class(cls):
    return [
        name for name, obj in vars(cls).items() if isinstance(obj, property)
    ]
