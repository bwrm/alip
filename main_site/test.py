class Person:
    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay=pay

    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))

    def __str__(self):
        return 'Person %s, %s' % (self.name, self.pay)


class Manager(Person):
    def giveRaise(self, percent, bonus=.10):
        Person.giveRaise(self, percent + bonus)


if __name__ == '__main__':
    bob = Person('Bob Smith')
    sue = Person('Sue Jones', job='dev', pay=1000)
    tom = Manager('Tom Jnes', 'mgr', pay=2000)
    tom.giveRaise(.20)
    print(bob)
    print(sue)
    print(tom)

