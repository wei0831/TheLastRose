import Zero
import Events
import Property
import VectorMath
import math
Vec3 = VectorMath.Vec3
class ShadowBehavior:
    RightDoor = Property.Bool(True)
    OffsetX = 0.4
    HardcodeDistance = 10
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        self.Player = self.Space.FindObjectByName("Player")
        self.PlayerShadow = self.Player.FindChildByName("PlayerShadow")
        self.TakingControl = False
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.TakingControl:
            if self.RightDoor:
                distance = self.Owner.Parent.Transform.WorldTranslation.x - self.Player.Transform.WorldTranslation.x
                self.PlayerShadow.Transform.WorldScale = Vec3(self.HardcodeDistance - distance, self.PlayerShadow.Transform.WorldScale.y, self.PlayerShadow.Transform.WorldScale.z)
                self.PlayerShadow.Transform.LocalTranslation = Vec3(-0.4-1* self.OffsetX * self.PlayerShadow.Transform.LocalScale.x, self.PlayerShadow.Transform.LocalTranslation.y, self.PlayerShadow.Transform.LocalTranslation.z)
            elif not self.RightDoor:
                distance =  self.Player.Transform.WorldTranslation.x - self.Owner.Parent.Transform.WorldTranslation.x
                self.PlayerShadow.Transform.WorldScale = Vec3(self.HardcodeDistance - distance, self.PlayerShadow.Transform.WorldScale.y, self.PlayerShadow.Transform.WorldScale.z)
                self.PlayerShadow.Transform.LocalTranslation = Vec3(-0.4, self.PlayerShadow.Transform.LocalTranslation.y, self.PlayerShadow.Transform.LocalTranslation.z)

    def OnCollisionStart(self, CollisionEvent):
        if CollisionEvent.OtherObject == self.Player:
            self.PlayerShadow.Sprite.Visible = True
            self.TakingControl = True
            
    def OnCollisionEnd(self, CollisionEvent):
        if CollisionEvent.OtherObject == self.Player:
            self.PlayerShadow.Sprite.Visible = False
            self.TakingControl = False
    
Zero.RegisterComponent("ShadowBehavior", ShadowBehavior)
