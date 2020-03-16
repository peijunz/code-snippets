class Adder:
    def __init__(self):
        self.S = 0
    def __call__(self, *args):
        if len(args) == 0:
            S, self.S = self.S, 0
            return S
        else:
            self.S += sum(args)
            return self
    def __repr__(self):
        return str(self.S)

sum_ = Adder()

sum_(4)(6)(3)(2)(0)(7,5,4)(8,3)(3)()
