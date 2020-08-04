__version__ = '1.0'
__author__ = 'Rudy'


class Person:
    """
    info
    """
    def __init__(self):
        pass
    def detail(self):
        temp = "i am %s, age %s , blood type %s " % (self.name, self.age, self.blood_type)
        print (temp)

    def test(self):
        print(1)

p = Person()