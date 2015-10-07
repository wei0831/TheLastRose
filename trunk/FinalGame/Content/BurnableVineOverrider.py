import Zero
import Events
import Property
import VectorMath
import Action
class BurnableVineOverrider:
    
    def Initialize(self, initializer):
        seq = Action.Sequence(self.Owner.Actions)
        Action.Call(seq, self.EnsureChild)
            
    def EnsureChild(self):
        for child in self.Owner.Hierarchy.Children:
            if child.BurnableVine:
                child.BurnableVine.PropagateDelay = .175
        
        
            
            
   

Zero.RegisterComponent("BurnableVineOverrider", BurnableVineOverrider)