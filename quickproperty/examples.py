from . import QuickProperty


## static without decorators
def on_get_attr(value, name):
    print(f'{name} was accessed giving {value}')

def on_set_attr(value, name):
    print(f'{name} was set to {value}')
    
class Person:
    name = QuickProperty(on_get=on_get_attr, on_set=on_set_attr, on_get_kws=dict(name='name'), on_set_kws=dict(name='name'), static=True)
    age = QuickProperty(on_get=on_get_attr, on_set=on_set_attr, on_get_kws=dict(name='age'), on_set_kws=dict(name='age'), static=True)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age


## static with decorators
class Person2:
    name = QuickProperty(on_get_kws=dict(attr='name'), on_set_kws=dict(attr='name'), static=True)
    age = QuickProperty(on_get_kws=dict(attr='age'), on_set_kws=dict(attr='age'), static=True)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @name.on_get
    @age.on_get
    def on_get_attr(value, attr):
        print(f'{attr} was accessed giving {value}')
        return value

    @name.on_set
    @age.on_set
    def on_set_attr(value, attr):
        print(f'{attr} was set to {value}')
        return value

# with decorator and using on_get_set_kws
class Person3:
    name = QuickProperty('admin', name='name')
    age = QuickProperty(0, name='age')
    
    def __init__(self, user, name, age):
        self.user = user
        self.name = name
        self.age = age

    @name.on_set
    @age.on_set
    def set_attr(self, value, name):
        print(f'user {self.user} set {name} to {value}')
        return value


## with decorator
class Book:
    page = QuickProperty(0)
    
    def __init__(self, user, page=None):
        self.user = user
        if page is not None:
            self.page = page

    @page.on_set
    def on_set_page(self, value):
        print(f'{self.user} set page to {value}')
        return value