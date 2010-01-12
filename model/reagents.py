
class Reagents( dict ):
    def __init__(self, *args, **kwargs):
        super(Reagents,self).__init__(*args,**kwargs)
    
    def addReagent(self, name, id):
        self[name] = Reagent(name, id)

class Reagent( object ):
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def __repr__(self):
        return "Reagent( %s )" % self.name
    
    def __str__(self):
        return str(self.id)
        