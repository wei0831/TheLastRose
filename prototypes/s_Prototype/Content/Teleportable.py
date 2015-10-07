import Zero
import Events
import Property
import VectorMath

class Teleportable:
    Active = Property.Bool(True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)

    def OnCollision(self, CollisionEvent):
        if self.Active and CollisionEvent.OtherObject.CanTeleport:
            CollisionEvent.OtherObject.CanTeleport.Teleport(self.Owner)
Zero.RegisterComponent("Teleportable", Teleportable)