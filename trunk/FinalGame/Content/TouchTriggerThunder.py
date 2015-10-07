import Zero
import Events
import Property
import VectorMath

class TouchTriggerThunder:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        self.Space.FindObjectByName("Camera").ThunderGenerator.ActivateThunder()

Zero.RegisterComponent("TouchTriggerThunder", TouchTriggerThunder)