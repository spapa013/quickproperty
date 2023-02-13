class QuickProperty:
    def __init__(self, init_value=None, on_get=None, on_set=None, on_get_kws_name=None, on_set_kws_name=None, static=False):
        self.init_value = init_value
        self.f_on_get = on_get
        self.f_on_set = on_set
        self.on_get_kws_name = on_get_kws_name
        self.on_set_kws_name = on_set_kws_name
        self.static = static
    
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name
        setattr(owner, self.private_name, self.init_value)
        
    def __get__(self, instance, owner):
        source = instance if instance is not None else owner
        value = getattr(source, self.private_name)

        if self.f_on_get is not None:
            if self.on_get_kws_name is not None:
                on_get_kws = getattr(source, self.on_get_kws_name)
            else:
                on_get_kws = {}
            return self.f_on_get(source, value, **on_get_kws) if not self.static else self.f_on_get(value, **on_get_kws)
        else:
            return value

    def __set__(self, instance, value):        
        if self.f_on_set is not None:
            if self.on_set_kws_name is not None:
                on_set_kws = getattr(instance, self.on_set_kws_name)
            else:
                on_set_kws = {}
            value = self.f_on_set(instance, value, **on_set_kws) if not self.static else self.f_on_set(value, **on_set_kws)
    
        setattr(instance, self.private_name, value)
    
    def on_get(self, on_get):
        self.f_on_get = on_get
        return on_get
        
    def on_set(self, on_set):
        self.f_on_set = on_set
        return on_set