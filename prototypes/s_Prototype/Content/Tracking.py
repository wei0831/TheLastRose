import Zero
import Events
import Property
import VectorMath

class Tracking:
    TrackedName = Property.String("")
    def Initialize(self, initializer):
        self.tracked = None
        if self.TrackedName:
            self.tracked = self.Space.FindObjectByName(self.TrackedName)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Transform.Translation = self.tracked.Transform.Translation
            
     
            
    

Zero.RegisterComponent("Tracking", Tracking)