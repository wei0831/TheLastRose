import Zero
import Events
import Property
import VectorMath
import math
Vec3 = VectorMath.Vec3
class ShadowBehavior:
    RightDoor = Property.Bool(True)
    IsOwner = False
    OffsetX = 0.15
    HardcodeDistance = 3
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        self.Player = self.Space.FindObjectByName("Player")
        self.PlayerShadow = self.Player.FindChildByName("PlayerShadow")
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.IsOwner and self.PlayerShadow.Sprite.Visible :
            
            distance = self.Owner.Parent.Transform.WorldTranslation.x - self.Player.Transform.WorldTranslation.x
            distance = math.fabs(distance)
            self.PlayerShadow.Transform.WorldScale = Vec3(self.HardcodeDistance - distance, self.PlayerShadow.Transform.WorldScale.y, self.PlayerShadow.Transform.WorldScale.z)

            flag = -1 if self.RightDoor else 1
            self.PlayerShadow.Transform.LocalTranslation = Vec3(flag* self.OffsetX * self.PlayerShadow.Transform.LocalScale.x, self.PlayerShadow.Transform.LocalTranslation.y, self.PlayerShadow.Transform.LocalTranslation.z)

    def OnCollisionStart(self, CollisionEvent):
        if CollisionEvent.OtherObject == self.Player:
            self.PlayerShadow.Sprite.Visible = True
            self.IsOwner = True
            
    def OnCollisionEnd(self, CollisionEvent):
        if CollisionEvent.OtherObject == self.Player:
            self.PlayerShadow.Sprite.Visible = False
            self.IsOwner = False
    
Zero.RegisterComponent("ShadowBehavior", ShadowBehavior)