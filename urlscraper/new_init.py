class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print("cls= ",cls)
        print(("name=",name))
        print("bases = ",bases)
        print("att=",attrs)
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)

        return type.__new__(cls, name, bases, attrs)
class Model(dict,metaclass=ModelMetaclass):
    __metaclass__ = ModelMetaclass

    name = "as"
    def __init__(self, **kw):
        super().__init__(**kw)

m = Model(name = "xa")

print(m)

