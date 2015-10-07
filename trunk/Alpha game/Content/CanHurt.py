import Zero
import Events
import Property
import VectorMath

class CanHurt:
    HurtRate = Property.Float(-10.0)
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        
    def OnCollision(self, CollisionEvent):
        if self.Active:
            if CollisionEvent.OtherObject.PlayerController:
               CollisionEvent.OtherObject.HealthStatus.RegenHealth(self.HurtRate)
               if CollisionEvent.OtherObject.BlinkAnim:
                   CollisionEvent.OtherObject.BlinkAnim.Active = True
               
               
    def OnCollisionEnd(self, CollisionEvent):
        if CollisionEvent.OtherObject.PlayerController:
            CollisionEvent.OtherObject.HealthStatus.ResetRegen()
        if CollisionEvent.OtherObject.BlinkAnim:
               CollisionEvent.OtherObject.BlinkAnim.Active = False
        

Zero.RegisterComponent("CanHurt", CanHurt)