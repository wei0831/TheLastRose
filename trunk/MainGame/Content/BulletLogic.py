import Zero
import Events
import Property
import VectorMath

class BulletLogic:
    def Initialize(self, initializer):
        self.followpoint = None
        self.followed = None
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
    def OnCollision(self, CollisionEvent):
        if not CollisionEvent.OtherObject.PlayerController:
            Zero.Disconnect(self.Owner,Events.CollisionStarted,self)
            self.Owner.Collider.Ghost = True

            self.Owner.TimedDeath.Active = True
            self.Owner.CanHurtOnce.Active = False
            self.Owner.RigidBody.Kinematic = True
        else:
            Zero.Disconnect(self.Owner,Events.CollisionStarted,self)
            
            self.Owner.Collider.Ghost = True
            self.Owner.RigidBody.Kinematic = True
            self.Owner.TimedDeath.Active = True
            self.Owner.GravityEffect.Active = False
            
            self.followed = CollisionEvent.OtherObject
            self.followpoint = self.Owner.Transform.Translation - self.followed.Transform.Translation
            
            Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
            
    def OnLogicUpdate(self, UpdateEvent):
        if not self.followed.CanFancyDie.DeathActive:
            self.Owner.RigidBody.Kinematic = False
            
            Zero.Disconnect(self.Space, Events.LogicUpdate, self)
        else:
            
            self.Owner.Transform.Translation = self.followpoint + self.followed.Transform.Translation
        
Zero.RegisterComponent("BulletLogic", BulletLogic)