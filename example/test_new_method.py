class Foo:
    ab = 100

    def __init__(self):
        self.a = 10

    @classmethod
    def nah(cls):
        Foo.ab = self.a

foo = Foo()
foo.nah(foo)
print foo.ab
