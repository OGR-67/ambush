class Parent:
    def __init__(self, ):
        self.update()
    
        
    def update(self):
        self.value = 1


class Child(Parent):
    def __init__(self, multiplier):
        super().__init__()
        self.get_value(multiplier)
        
    def get_value(self, multiplier):
        self.value = 5 * multiplier
        
class Child2(Child):
    def __init__(self):
        super().__init__(5)
        print(self.value)

# parent_instance = Parent(3)
child_instance = Child2()
# print(parent_instance.value)        


