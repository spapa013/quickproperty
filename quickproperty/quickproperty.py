class QuickProperty:
    """
    An alternative implementation of Python's `property` descriptor.
    """
    def __init__(
        self, 
        init_value=None, 
        *, 
        on_get=None, 
        on_set=None, 
        on_get_kws=None, 
        on_set_kws=None, 
        on_get_kws_name=None, 
        on_set_kws_name=None, 
        static=False, 
        **on_get_set_kws
    ):
        """
        Args:
            init_value (Any) - the initial value to set (does not trigger on_set)
            on_get (function) - the function to run when value is accessed. Must accept and return value.
            on_set (function) - the function to run when value is set. Must accept and return value.
            on_get_kws (dict) - kws to pass to on_get
            on_set_kws (dict) - kws to pass to on_set
            on_get_kws_name (str) - the name of the attr in the owner class where the kws to pass to on_get are stored
            on_set_kws_name (str) - the name of the attr in the owner class where the kws to pass to on_Set are stored
            static (bool) - if True, does not pass the owner class or instance into on_get and on_set, default is False
            on_get_set_kws - additional default kws to pass to both on_set and on_get. 
        """
        assert not (on_get_kws is not None and on_get_kws_name is not None), 'Provide either on_get_kws or on_get_kws_name but not both'
        assert not (on_set_kws is not None and on_set_kws_name is not None), 'Provide either on_set_kws or on_set_kws_name but not both'
        self.init_value = init_value
        self.f_on_get = on_get
        self.f_on_set = on_set
        self.on_get_kws = on_get_kws
        self.on_set_kws = on_set_kws
        self.on_get_kws_name = on_get_kws_name
        self.on_set_kws_name = on_set_kws_name
        self.static = static
        self.on_get_set_kws = on_get_set_kws

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name
        setattr(owner, self.private_name, self.init_value)
        
    def __get__(self, instance, owner):
        source = instance if instance is not None else owner
        value = getattr(source, self.private_name)

        if self.f_on_get is not None:
            if self.on_get_kws_name is not None:
                print('got here')
                on_get_kws = getattr(source, self.on_get_kws_name)
            elif self.on_get_kws is not None:
                assert isinstance(self.on_get_kws, dict)
                on_get_kws = self.on_get_kws
            else:
                on_get_kws = {}
            assert isinstance(on_get_kws, dict)
            for k, v in self.on_get_set_kws.items():
                on_get_kws.setdefault(k, v)
            return self.f_on_get(source, value, **on_get_kws) if not self.static else self.f_on_get(value, **on_get_kws)
        else:
            return value

    def __set__(self, instance, value):        
        if self.f_on_set is not None:
            if self.on_set_kws_name is not None:
                on_set_kws = getattr(instance, self.on_set_kws_name)
            elif self.on_set_kws is not None:
                on_set_kws = self.on_set_kws
            else:
                on_set_kws = {}
            assert isinstance(on_set_kws, dict)
            for k, v in self.on_get_set_kws.items():
                on_set_kws.setdefault(k, v)
            value = self.f_on_set(instance, value, **on_set_kws) if not self.static else self.f_on_set(value, **on_set_kws)
    
        setattr(instance, self.private_name, value)
    
    def on_get(self, on_get):
        self.f_on_get = on_get
        return on_get
        
    def on_set(self, on_set):
        self.f_on_set = on_set
        return on_set