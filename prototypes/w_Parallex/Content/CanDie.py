import Zero
import Events
import Property
import VectorMath
import Action
import math
Vec3 = VectorMath.Vec3

class CanDie:
    CurrentUpdate = None
    DeathActive = Property.Bool(True)
    SoulMoveSpeed = Property.Float(0.04)
    Delay_Die = Property.Float(0.25)
    IncreaseSizeDelta = Property.Float(0.025)
    MaxSize = Property.Float(1.25)
    DecreaseSizeDelta = Property.Float(0.025)
    MinSize = Property.Float(0.01)
    IncreaseAlphaDelta = Property.Float(0.01)    
    
    def Initialize(self, initializer):
        self.CheckPoint = self.Space.FindObjectByName("CheckPoint")
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if(self.CurrentUpdate != None):
            self.CurrentUpdate()
        
    def Die(self):
        if(not self.DeathActive):
            return
        
        self.DeathActive = False
        self.Owner.Sprite.Visible = False
        self.Owner.BoxCollider.Ghost = True
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
            self.CurrentUpdate = None
            self.Death_Stage2()
        self.Soul.SphericalParticleEmitter.EmitterSize = size
        
    def Death_Stage2(self):
        self.CurrentUpdate = self.GoRespawn
        
    def GoRespawn(self):
        if(self.CheckPoint == None): 
            return
        
        towardVec = self.CheckPoint.Transform.WorldTranslation - self.Owner.Transform.WorldTranslation
        towardVec.z = 0
        towardVec.normalized()

        if(math.fabs(towardVec.length()) > 1):
            self.Owner.Transform.WorldTranslation += towardVec * self.SoulMoveSpeed
        else:
            self.CurrentUpdate = None
            self.Death_Stage3()
    
    def Death_Stage3(self):
        self.CurrentUpdate = self.DecreaseSize
    
    def DecreaseSize(self):
        size = self.Soul.SphericalParticleEmitter.EmitterSize
        size -= Vec3(self.DecreaseSizeDelta, self.DecreaseSizeDelta, self.DecreaseSizeDelta)
        if(size.x <= self.MinSize or size.y <= self.MinSize or size.z <= self.MinSize):
            self.CurrentUpdate = None
            self.Soul.Destroy()
            self.Death_Stage4()
        self.Soul.SphericalParticleEmitter.EmitterSize = size
        
    def Death_Stage4(self):
        self.Owner.Sprite.Visible = True
        self.Owner.Sprite.Color = Vec3(1, 1, 1, 0)
        self.Owner.BoxCollider.Ghost = False
        self.Owner.RigidBody.Kinematic = False
        self.Owner.PlayerController.Active = True
        self.Owner.Sprite.AnimationActive = True
        self.CurrentUpdate = self.IncreaseAlpha
        
    def IncreaseAlpha(self):
        color = self.Owner.Sprite.Color
        color.w += self.IncreaseAlphaDelta
        
        if(color.w >= 1.0):
            color.w = 1.0
            self.CurrentUpdate = None
            self.DeathActive = True
        self.Owner.Sprite.Color = color
        
Zero.RegisterComponent("CanDie", CanDie)