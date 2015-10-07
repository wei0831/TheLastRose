import Zero
import Events
import Property
import VectorMath

class Collectible:
    def Initialize(self, initializer):
        pass
        
    def Collected(self):
        self.Space.CreateAtPosition("GoldParticle", self.Owner.Transform.Translation)
        self.Owner.Destroy()

Zero.RegisterComponent("Collectible", Collectible)