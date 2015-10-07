import Zero
import Events
import Property
import VectorMath
Vec3 = VectorMath.Vec3

class PenetrablePlatform:
    def Initialize(self, initializer):
        self.player = self.Space.FindObjectByName("Player")
        self.temporary_disabled = False
        
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.RigidBody and CollisionEvent.OtherObject.Transform.Translation.y > self.Owner.Transform.Translation.y:
            
            if CollisionEvent.OtherObject.RigidBody.Velocity.y < 0:
                
                CollisionEvent.OtherObject.RigidBody.Velocity *= VectorMath.Vec3(1,0,0)
            if CollisionEvent.OtherObject.RigidBody.Force.y < 0:
                CollisionEvent.OtherObject.RigidBody.Force *= VectorMath.Vec3(1,0,0)
            
            CollisionEvent.OtherObject.Transform.Translation += Vec3(0,CollisionEvent.FirstPoint.Penetration*1.3,0)
            self.Owner.Collider.Ghost = False
                
    def OnCollisionEnd(self, CollisionEvent):
        if CollisionEvent.OtherObject.PlayerController:
            self.Owner.Collider.Ghost = True
            
    def OnLogicUpdate(self, UpdateEvent):
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.S):
            self.Owner.Collider.Ghost = True
            
        
        if self.player.Transform.Translation.y < self.Owner.Transform.Translation.y:
            self.Owner.Collider.Ghost = True
        

Zero.RegisterComponent("PenetrablePlatform", PenetrablePlatform)