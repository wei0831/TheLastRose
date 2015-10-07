import Zero
import Events
import Property
import VectorMath

class TriggerDoor:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "TriggerEvent", self.OnTrigger)
        
    def OnTrigger(self, TriggerEvent):
        self.Owner.Sprite.Color = VectorMath.Vec4(0,0,0,1)

Zero.RegisterComponent("TriggerDoor", TriggerDoor)