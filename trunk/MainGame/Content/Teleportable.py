import Zero
import Events
import Property
import VectorMath
import Action
class Teleportable:
    Active = Property.Bool(True)
    TeleportDelay = Property.Float(.5)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)

    def OnCollision(self, CollisionEvent):
        if self.Active and CollisionEvent.OtherObject.CanTeleport:
            CollisionEvent.OtherObject.CanTeleport.Teleport(self.Owner)
            self.Active = False
            
            # set dumb duration
            seq = Action.Sequence(self.Owner.Actions)
            Action.Delay(seq, self.TeleportDelay)
            def Activate():
                self.Active = True
            Action.Call(seq,Activate)
Zero.RegisterComponent("Teleportable", Teleportable)