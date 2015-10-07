import Zero
import Events
import Property
import VectorMath
import Action
import math
Vec3 = VectorMath.Vec3

class CanFancyDie:
    CurrentUpdate = None
    DeathActive = Property.Bool(True)
    SoulMoveSpeed = Property.Float(0.04)
    Delay_Die = Property.Float(0.25)
    IncreaseSizeDelta = Property.Float(0.025)
    MaxSize = Property.Float(1.25)
    DecreaseSizeDelta = Property.Float(0.025)
    MinSize = Property.Float(0.00)
    IncreaseAlphaDelta = Property.Float(0.03)    

    def Initialize(self, initializer):
        self.IsImmune = False
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        
        
        if self.CurrentUpdate:
            self.CurrentUpdate()
        
    def Die(self):
        self.IsImmune = True
        if not self.DeathActive:
            return
        if self.Owner.CanHook:
            self.Owner.CanHook.ForceUnhooked()
        if self.Owner.PlayerController.Mouse:
            self.Owner.PlayerController.Mouse.MouseLocationIndicator.Deactivated = True
        if self.Owner.CanTrigger:
            self.Owner.CanTrigger.Active = False
        self.DeathActive = False
        self.Owner.Sprite.Visible = False
        self.Owner.Collider.Ghost = True
        self.Owner.PlayerController.Active = False
        self.Owner.Sprite.AnimationActive = False
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, self.Delay_Die)
        Action.Call(sequence, self.DelayDie)
        
        self.Death_Stage1()
    
    def DelayDie(self):
        self.Owner.RigidBody.Kinematic = True
    
    def Death_Stage1(self):

        self.Soul = self.Space.CreateAtPosition("RespawnSoul", self.Owner.Transform.WorldTranslation)
        self.Soul.SphericalParticleEmitter.EmitterSize = Vec3(self.MinSize, self.MinSize, self.MinSize)
        self.Soul.AttachToRelative(self.Owner)

        self.CurrentUpdate = self.IncreaseSize

    def IncreaseSize(self):
        

        size = self.Soul.SphericalParticleEmitter.EmitterSize
        size += Vec3(self.IncreaseSizeDelta, self.IncreaseSizeDelta, self.IncreaseSizeDelta)
        if(size.x >= self.MaxSize or size.y >= self.MaxSize or size.z >= self.MaxSize):
            self.CurrentUpdate = self.GoRespawn
        self.Soul.SphericalParticleEmitter.EmitterSize = size
       
        
    def GoRespawn(self):
        
        if not self.Owner.CanCheck:
            return
        
        towardVec = self.Owner.CanCheck.GetCheck() - self.Owner.Transform.WorldTranslation
        towardVec.z = 0
        towardVec.normalized()
        

        if towardVec.length() > 0.1:
            self.Owner.Transform.WorldTranslation += towardVec * self.SoulMoveSpeed
        else:
            self.CurrentUpdate = self.DecreaseSize
    
           
    def DecreaseSize(self):
        size = self.Soul.SphericalParticleEmitter.EmitterSize
        size -= Vec3(1 ,1, 1) * self.DecreaseSizeDelta
        if size.x <= self.MinSize or size.y <= self.MinSize or size.z <= self.MinSize:
            self.CurrentUpdate = None
            self.Death_Stage4()
        self.Soul.SphericalParticleEmitter.EmitterSize = size
        
    def Death_Stage4(self):
        self.Owner.Sprite.Visible = True
        self.Owner.Sprite.Color = Vec3(1, 1, 1, 0)
        self.Owner.Collider.Ghost = False
        
        self.Owner.RigidBody.Force *= 0
        self.Owner.RigidBody.Velocity *= 0
        self.Owner.RigidBody.Kinematic = False
        
        self.Owner.PlayerController.Active = True
        self.Owner.Sprite.AnimationActive = True
        self.Owner.HealthStatus.Reset()
        self.Owner.BlinkAnim.Active = False
        self.CurrentUpdate = self.IncreaseAlpha
        
    def IncreaseAlpha(self):
        self.Soul.SpriteParticleSystem.Tint *= VectorMath.Vec4(1,1,1,0.9)
        
        color = self.Owner.Sprite.Color
        color.w += self.IncreaseAlphaDelta
        if(color.w >= 1.0):
            color.w = 1.0
            self.CurrentUpdate = None
            self.DeathActive = True
            self.Soul.Destroy()
            if self.Owner.PlayerController.Mouse:
                self.Owner.PlayerController.Mouse.MouseLocationIndicator.Deactivated = False
            self.IsImmune = False
            self.Owner.CanTrigger.Active = True
        
            
        self.Owner.Sprite.Color = color
    def Immune(self):
        return self.IsImmune
        
Zero.RegisterComponent("CanFancyDie", CanFancyDie)