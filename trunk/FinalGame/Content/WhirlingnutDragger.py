import Zero
import Events
import Property
import VectorMath

class WhirlingnutDragger:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.Name == "Whirlingnut":
            CollisionEvent.OtherObject.MassOverride.Mass = 100
            CollisionEvent.OtherObject.GravityEffect.Direction *= -1
            
            
            #CollisionEvent.OtherObject.MassOverride.Mass = 1000
        
        
    

Zero.RegisterComponent("WhirlingnutDragger", WhirlingnutDragger)