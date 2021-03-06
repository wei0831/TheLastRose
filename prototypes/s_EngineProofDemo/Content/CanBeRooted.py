import Zero
import Events
import Property
import VectorMath

class CanBeRooted:
    ShouldRoot = Property.Bool(True)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.GrowableGround:
            
            normal = - CollisionEvent.FirstPoint.WorldNormalTowardsOther
            self.Owner.Transform.Translation += normal * CollisionEvent.FirstPoint.Penetration
            if self.ShouldRoot:
                self.Owner.Transform.Rotation = CollisionEvent.OtherObject.Transform.Rotation
                self.Owner.RigidBody.Kinematic = True
                
            if self.Owner.CanBounce:
                self.Owner.CanBounce.ToDirection(normal)
                
            Zero.Disconnect(self.Owner, Events.CollisionStarted, self)

            

Zero.RegisterComponent("CanBeRooted", CanBeRooted)