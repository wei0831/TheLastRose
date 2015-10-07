import Zero
import Events
import Property
import VectorMath

class CanInstantKill:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
    
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.CanFancyDie:
            CollisionEvent.OtherObject.CanFancyDie.Die()

Zero.RegisterComponent("CanInstantKill", CanInstantKill)