import Zero
import Events
import Property
import VectorMath

class BulletLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
    def OnCollision(self, CollisionEvent):
        if not CollisionEvent.OtherObject.PlayerController:
            Zero.Disconnect(self.Owner,Events.CollisionStarted,self)
            self.Owner.Collider.Ghost = True

            self.Owner.TimedDeath.Active = True
            self.Owner.CanHurtOnce.Active = False
            self.Owner.RigidBody.Static = True
        else:
            Zero.Disconnect(self.Owner,Events.CollisionStarted,self)
            self.Owner.Collider.Ghost = True
            self.Owner.RigidBody.Static = True
            self.Owner.TimedDeath.Active = True
            self.Owner.GravityEffect.Active = False
            self.Owner.AttachToRelative(CollisionEvent.OtherObject)
        
Zero.RegisterComponent("BulletLogic", BulletLogic)