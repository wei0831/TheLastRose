import Zero
import Events
import Property
import VectorMath

class CanCollect:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.Collectible:
            CollisionEvent.OtherObject.Collectible.Collected()

Zero.RegisterComponent("CanCollect", CanCollect)