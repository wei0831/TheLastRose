import Zero
import Events
import Property
import VectorMath

class PlayerGravityModifier:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        normal = CollisionEvent.FirstPoint.WorldNormalTowardsOther
        # if degree > 22.5 and degree < 65
        if abs(normal.y) < abs(normal.x) * 4 and abs(normal.y) * 1.5 > abs(normal.x):
            #print("gravity")
            force = VectorMath.Vec3(normal.x * 22, 0, 0)
            self.Owner.RigidBody.ApplyForce(force)

Zero.RegisterComponent("PlayerGravityModifier", PlayerGravityModifier)