import Zero
import Events
import Property
import VectorMath
Vec3 = VectorMath.Vec3

class AIMovementUnderground:
    Speed = Property.Float(1.0)
    InitialDirection = Property.Vector3(Vec3(1,0,0))
    Active = Property.Bool(True)
    DetectionBox = Property.Vector3(Vec3(2,2,1))
    AnimTable = Property.ResourceTable()
    
    def Ensuring(self):
        self.EnsureAiMovementInterface()
        self.EnsureDetectorInterface()
        self.CurrentUpdate = self.UndergroundWalking
    
    def EnsureAiMovementInterface(self):
        if not self.Owner.AIMovementInterface:
            self.Owner.AddComponentByName("AIMovementInterface")
        if not self.Owner.AIMovementInterface.IsSet():
            self.Owner.AIMovementInterface.Set(self)
            
    def EnsureDetectorInterface(self):
        if not self.Owner.PlayerDetectorInterface:
            self.Owner.AddComponentByName("PlayerDetectorInterface")
            self.Owner.PlayerDetectorInterface.SetSize(self.DetectionBox)
            self.Owner.PlayerDetectorInterface.Activate()
        
    
    def Initialize(self, initializer):
        self.Direction = self.InitialDirection
        self.resetcounter = 0
        self.waitcounter = 0
        self.SpeedMultiplier = 1
        self.dumbcounter = 0

        self.CurrentUpdate = self.Ensuring
        
        self.underanim = self.AnimTable.FindResource("Under")
        self.outanim = self.AnimTable.FindResource("Out")
        self.inanim = self.AnimTable.FindResource("In")
        self.restanim = self.AnimTable.FindResource("Rest")
        self.attackanim = self.AnimTable.FindResource("Attack")
        
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
        
    def Waiting(self):       
        self.waitcounter -= 1        
        self.Owner.Sprite.Visible = False
        
        if self.resetcounter > 0:
            self.resetcounter -= 1
        elif self.resetcounter == 0:
            self.SpeedMultiplier = 0*0.1 + self.SpeedMultiplier * 0.9
        
        direct = self.Owner.PlayerDetectorInterface.GetDirection() 
        self.Owner.Sprite.FlipX = direct.x < 0
                
        if self.waitcounter <= 0:
            self.CurrentUpdate = self.Attacking
            self.Owner.Sprite.Visible = True
            
            
    def Attacking(self):
        self.Owner.ClickReceiver.Receivable = True
        

        if not self.Owner.Sprite.SpriteSource == self.outanim:
            self.Owner.Sprite.SpriteSource = self.outanim
            
        if self.Owner.Sprite.CurrentFrame == 2:
            hurtbox = self.Space.CreateAtPosition("HurtBox",self.Owner.Transform.Translation + Vec3(0,.5,0))
            hurtbox.Transform.Scale = Vec3(1,1.5,1)
            hurtbox.CanHurt.HurtRate = -20
            hurtbox.TimedDeath.LifeTime = 0.3
            
            sandsmoke = self.Space.CreateAtPosition("SandSmokeParticle", self.Owner.Transform.Translation)
            t = sandsmoke.SpriteParticleSystem.Tint
            sandsmoke.SpriteParticleSystem.Tint = VectorMath.Vec4(t.x, t.y, t.z, 0.1)
            sandsmoke.SphericalParticleEmitter.EmitCount = 3
            sandsmoke.SphericalParticleEmitter.ResetCount()
            
        if self.Owner.Sprite.CurrentFrame == 5:
            self.dumbcounter = 20
            self.CurrentUpdate = self.Resting
            
    def Resting(self):
        if not self.Owner.Sprite.SpriteSource == self.restanim:
            self.Owner.Sprite.SpriteSource = self.restanim
            
        self.dumbcounter -= 1
        
        if self.dumbcounter <= 0:
            self.CurrentUpdate = self.Lunging
    def Lunging(self):
        if not self.Owner.Sprite.SpriteSource == self.attackanim:
            self.Owner.Sprite.SpriteSource = self.attackanim
        if self.Owner.Sprite.CurrentFrame == 1:
            dir = 1 if not self.Owner.Sprite.FlipX else -1
            
            hurtbox = self.Space.CreateAtPosition("HurtBox",self.Owner.Transform.Translation + Vec3(.5 * dir,.2,0))
            hurtbox.Transform.Scale = Vec3(1.7,1,1)
            hurtbox.CanHurt.HurtRate = -20
            hurtbox.TimedDeath.LifeTime = 0.2
            
            self.Owner.Sprite.AnimationActive = False
            
            self.Owner.RigidBody.ApplyLinearImpulse(Vec3(dir * 10,5,0))
            self.CurrentUpdate = self.Postlunging
            
    def Postlunging(self):
        
        self.Owner.Sprite.AnimationActive = True
        if self.Owner.Sprite.CurrentFrame == 2:
            self.dumbcounter = 20
            self.CurrentUpdate = self.SecondResting
            
    def SecondResting(self):
        if not self.Owner.Sprite.SpriteSource == self.restanim:
            self.Owner.Sprite.SpriteSource = self.restanim
            
        self.dumbcounter -= 1
        if self.dumbcounter <= 0:
            self.CurrentUpdate = self.GoUnder
    def GoUnder(self):
        if not self.Owner.Sprite.SpriteSource == self.inanim:
            self.Owner.Sprite.SpriteSource = self.inanim
        if self.Owner.Sprite.CurrentFrame == 2:
            self.dumbcounter = 50
            self.CurrentUpdate = self.UndergroundWalking
                
    def UndergroundWalking(self):
        self.Owner.ClickReceiver.Receivable = False
        self.Owner.Sprite.Visible = True
        if not self.Owner.Sprite.SpriteSource == self.underanim:
            self.Owner.Sprite.SpriteSource = self.underanim
        
        if self.dumbcounter <= 0:
            if self.Owner.PlayerDetectorInterface.InRange():
                self.CurrentUpdate = self.Waiting
                self.waitcounter = 35
        else:
            self.dumbcounter -= 1

        if self.resetcounter > 0:
            self.resetcounter -= 1
        elif self.resetcounter == 0:
            self.SpeedMultiplier = 0.4*0.01 + self.SpeedMultiplier * 0.99
            
        self.Owner.Sprite.FlipX = self.Direction.x < 0
        self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            self.CurrentUpdate()
        
            
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.IsSentry:
            
            if abs(CollisionEvent.FirstPoint.WorldNormalTowardsOther.x) > 0.95:
                self.CurrentUpdate = self.UndergroundWalking
                self.dumbcounter = 30
                direction = CollisionEvent.OtherObject.IsSentry.SentryDirection
                if direction.x == 0 and direction.y == 0:
                    self.Direction = Vec3(1,0,0) if CollisionEvent.FirstPoint.WorldNormalTowardsOther.x < 0 else Vec3(-1,0,0)
                else:
                    self.Direction = direction

            
    def SlowDownBy(self, SlowDownRatio, TimeSteps):
        self.resetcounter = TimeSteps
        self.SpeedMultiplier = SlowDownRatio


Zero.RegisterComponent("AIMovementUnderground", AIMovementUnderground)