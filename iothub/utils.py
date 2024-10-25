class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.cache_name = f"_{func.__name__}_cache"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, self.cache_name):
            setattr(obj, self.cache_name, self.func(obj))
        return getattr(obj, self.cache_name)
