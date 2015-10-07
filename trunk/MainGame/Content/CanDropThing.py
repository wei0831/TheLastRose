import Zero
import Events
import Property
import VectorMath

class CanDropThing:
    Dropped = Property.Archetype()
    def Initialize(self, initializer):
        pass
        
    def Drop():
        self.Space.CreateAtPosition(self.Dropped,self.Owner.Transform.Translation)
        
        

Zero.RegisterComponent("CanDropThing", CanDropThing)