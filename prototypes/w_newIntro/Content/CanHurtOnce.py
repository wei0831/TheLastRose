import Zero
import Events
import Property
import VectorMath

class CanHurtOnce:
    HurtValue = Property.Float(-1.0)
    Active = Property.Bool(True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if self.Active:
            if CollisionEvent.OtherObject.PlayerController:
               CollisionEvent.OtherObject.HealthStatus.AddHealth(self.HurtValue)
               if CollisionEvent.OtherObject.BlinkAnim:
                   CollisionEvent.OtherObject.BlinkAnim.Active = True
                   CollisionEvent.OtherObject.BlinkAnim.Countdown = 50
                   
               
               
               
    

Zero.RegisterComponent("CanHurtOnce", CanHurtOnce)