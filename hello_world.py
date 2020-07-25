class Sample:
    def __init__(self):
        self.t = 5
    
    def get_t(self):
        return self.t


a = Sample()
m = a.t
m = 8
print(a.get_t())