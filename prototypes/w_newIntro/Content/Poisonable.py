import Zero
import Events
import Property
import VectorMath

class Poisonable:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "PoisonEvent", self.OnPoison)
        
    def OnPoison(self, PoisonEvent):
        pass

Zero.RegisterComponent("Poisonable", Poisonable)