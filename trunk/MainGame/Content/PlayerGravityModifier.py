import Zero
import Events
import Property
import VectorMath

class PlayerGravityModifier:
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if self.Active and not CollisionEvent.OtherObject.Collider.Ghost:
            
            normal = CollisionEvent.FirstPoint.WorldNormalTowardsOther
            # if degree > 22.5 and degree < 65
            if abs(normal.y) < abs(normal.x) * 4 and abs(normal.y) * 1.5 > abs(normal.x):
                force = VectorMath.Vec3(normal.x*11, -normal.y*3, 0)
                self.Owner.RigidBody.ApplyForce(force)

Zero.RegisterComponent("PlayerGravityModifier", PlayerGravityModifier)