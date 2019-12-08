def get_methods_and_properties(cls):
    methods = [name for name, obj in vars(cls).items() if callable(obj)]
    properties = [name for name, obj in vars(cls).items() if isinstance(obj, property)]
    return methods, properties
