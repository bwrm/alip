class FirstClass:
    def setdata(self, value):
        self.data = value

    def display(self):
        print(self.data)

class SecondClass(FirstClass):
    # Наследует setdata
    def display(self):
    # Изменяет display
        print('Current value = “%s”' % self.data)


class ThirdClass(SecondClass):
    # Наследует SecondClass
    def __init__(self, value):
        self.data = value

    def __add__(self, other):
        return ThirdClass(self.data + other)

    def __str__(self):
        return '[ThirdClass: %s]' % self.data