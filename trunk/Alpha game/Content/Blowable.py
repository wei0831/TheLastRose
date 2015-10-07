import Zero
import Events
import Property
import VectorMath

class Blowable:
    Active = Property.Bool(True)
    Decay = Property.Float(1.0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if self.Active and CollisionEvent.OtherObject.CanBlow:
            CollisionEvent.OtherObject.CanBlow.Blow(self.Owner, self.Decay)
            
Zero.RegisterComponent("Blowable", Blowable)