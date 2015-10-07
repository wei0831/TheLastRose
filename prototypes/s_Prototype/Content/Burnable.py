import Zero
import Events
import Property
import VectorMath

class Burnable:
    PropagateBurn = Property.Bool(True)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "BurnEvent", self.OnBurn)
        
    def OnBurn(self, BurnEvent):
        if not self.Owner.BurnAnim:
            self.Owner.AddComponentByName("BurnAnim")
        if self.PropagateBurn and not self.Owner.CanBurn:
            self.Owner.AddComponentByName("CanBurn")


Zero.RegisterComponent("Burnable", Burnable)