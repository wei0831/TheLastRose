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
    
    def EnsureSoundEmitter(self):
        if not self.Owner.SoundEmitter:
            self.Owner.AddComponentByName("SoundEmitter")
        def Null():
            pass
        self.EnsureSoundEmitter = Null
    
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
        Zero.Connect(self.Owner, "BounceEvent", self.OnBounce)

    def OnBounce(self, BounceEvent):
        if self.Owner.Bounceable.Active :
            self.CurrentUpdate = self.SecondResting
            self.dumbcounter = 300
            self.Owner.ClickReceiver.Receivable = True

        
    def Waiting(self):       
        self.Owner.Teleportable.Active = True
        self.Owner.Bounceable.Active = False

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
            #self.CurrentUpdate = self.HighAttack
            self.Owner.Sprite.Visible = True
    
    def HighAttack(self):
        self.Owner.Teleportable.Active = True
        self.Owner.Bounceable.Active = False

        self.Owner.ClickReceiver.Receivable = True
        

        if not self.Owner.Sprite.SpriteSource == self.outanim:
            self.Owner.Sprite.SpriteSource = self.outanim
            
        if self.Owner.Sprite.CurrentFrame == 2:
            hurtbox = self.Space.CreateAtPosition("HurtBox",self.Owner.Transform.Translation + Vec3(0,.7,0))
            hurtbox.Transform.Scale = Vec3(.26,0.75,1)
            hurtbox.CanHurt.HurtRate = -20
            hurtbox.TimedDeath.LifeTime = 0.05
            hurtbox.AttachToRelative(self.Owner)
            
            self.Owner.RigidBody.ApplyLinearImpulse(VectorMath.Vec3(0,5,0))
            
            sandsmoke = self.Space.CreateAtPosition("SandSmokeParticle", self.Owner.Transform.Translation)
            t = sandsmoke.SpriteParticleSystem.Tint
            sandsmoke.SpriteParticleSystem.Tint = VectorMath.Vec4(t.x, t.y, t.z, 0.1)
            sandsmoke.SphericalParticleEmitter.RandomVelocity *= 0.4
            sandsmoke.SphericalParticleEmitter.EmitCount = 3
            sandsmoke.SphericalParticleEmitter.ResetCount()
            
        if self.Owner.Sprite.CurrentFrame == 3:
            self.Owner.Sprite.AnimationSpeed = 0
            
        if self.Owner.RigidBody.Velocity.y < 0:
            self.Owner.Sprite.AnimationSpeed = 1
            self.CurrentUpdate = self.GoUnder
            

    def Attacking(self):
        self.Owner.Teleportable.Active = True
        self.Owner.Bounceable.Active = False

        self.Owner.ClickReceiver.Receivable = True
        

        if not self.Owner.Sprite.SpriteSource == self.outanim:
            self.Owner.SoundEmitter.PlayCue("DigCue")
            self.Owner.Sprite.SpriteSource = self.outanim
        
            
        if self.Owner.Sprite.CurrentFrame == 2:
            hurtbox = self.Space.CreateAtPosition("HurtBox",self.Owner.Transform.Translation + Vec3(0,.6,0))
            hurtbox.Transform.Scale = Vec3(.32,0.85,1)
            hurtbox.CanHurt.HurtRate = -100
            hurtbox.TimedDeath.LifeTime = 0.05
            hurtbox.AttachToRelative(self.Owner)
            
            
            
            sandsmoke = self.Space.CreateAtPosition("SandSmokeParticle", self.Owner.Transform.Translation)
            t = sandsmoke.SpriteParticleSystem.Tint
            sandsmoke.SpriteParticleSystem.Tint = VectorMath.Vec4(t.x, t.y, t.z, 0.1)
            sandsmoke.SphericalParticleEmitter.RandomVelocity *= 0.4
            sandsmoke.SphericalParticleEmitter.EmitCount = 3
            sandsmoke.SphericalParticleEmitter.ResetCount()
        if self.Owner.Sprite.CurrentFrame == 3:
            self.Owner.RigidBody.ApplyLinearImpulse(VectorMath.Vec3(0,2.5,0))
        if self.Owner.Sprite.CurrentFrame == 5:
            self.dumbcounter = 20
            self.CurrentUpdate = self.Resting
            
    def Resting(self):
        self.Owner.Teleportable.Active = True
        self.Owner.Bounceable.Active = True

        if not self.Owner.Sprite.SpriteSource == self.restanim:
            self.Owner.Sprite.SpriteSource = self.restanim
            
        self.dumbcounter -= 1
        
        if self.dumbcounter <= 0:
            self.Owner.Bounceable.Active = True
            self.CurrentUpdate = self.Lunging
    def Lunging(self):
        self.Owner.Teleportable.Active = True
        self.Owner.Bounceable.Active = True

        if not self.Owner.Sprite.SpriteSource == self.attackanim:
            self.Owner.Sprite.SpriteSource = self.attackanim
        if self.Owner.Sprite.CurrentFrame == 1:
            dir = 1 if not self.Owner.Sprite.FlipX else -1
            modifier = .6 if not self.Owner.Sprite.FlipX else -.2
            
            hurtbox = self.Space.CreateAtPosition("HurtBox",self.Owner.Transform.Translation + Vec3(dir * modifier,.35,0))
            hurtbox.Transform.Scale = Vec3(1,.4,1)
            hurtbox.CanHurt.HurtRate = -30
            hurtbox.TimedDeath.LifeTime = 0.25
            hurtbox.AttachToRelative(self.Owner)
            
            self.Owner.Sprite.AnimationActive = False
            
            self.Owner.RigidBody.ApplyLinearImpulse(Vec3(dir * 15,5,0))
            self.CurrentUpdate = self.Postlunging
            
    def Postlunging(self):
        self.Owner.Teleportable.Active = True
        self.Owner.Sprite.AnimationActive = True
        if self.Owner.Sprite.CurrentFrame == 2:
            self.dumbcounter = 40
            self.CurrentUpdate = self.SecondResting
            
    def SecondResting(self):
        self.Owner.Teleportable.Active = True
        self.Owner.Bounceable.Active = False

        if not self.Owner.Sprite.SpriteSource == self.restanim:
            self.Owner.Sprite.SpriteSource = self.restanim
            
        self.dumbcounter -= 1
        if self.dumbcounter <= 0:
            self.CurrentUpdate = self.GoUnder
            self.EnsureSoundEmitter()
            self.Owner.SoundEmitter.PlayCue("MonsterDigBackCue")
            
    def GoUnder(self):
        self.Owner.Teleportable.Active = False
        self.Owner.Bounceable.Active = False
        self.Owner.Collider.Ghost = True

        if not self.Owner.Sprite.SpriteSource == self.inanim:
            self.Owner.Sprite.SpriteSource = self.inanim
            
        if self.Owner.Sprite.CurrentFrame == 2:
            self.dumbcounter = 50
            self.CurrentUpdate = self.UndergroundWalking
            
            sandsmoke = self.Space.CreateAtPosition("SandSmokeParticle", self.Owner.Transform.Translation)
            t = sandsmoke.SpriteParticleSystem.Tint
            sandsmoke.SpriteParticleSystem.Tint = VectorMath.Vec4(t.x, t.y, t.z, 0.1)
            sandsmoke.SphericalParticleEmitter.RandomVelocity *= .5
            sandsmoke.SphericalParticleEmitter.StartVelocity *= .5
            sandsmoke.SphericalParticleEmitter.EmitCount = 10
            sandsmoke.SphericalParticleEmitter.ResetCount()
            
            
        
                
    def UndergroundWalking(self):
        self.Owner.Teleportable.Active = False
        self.Owner.Bounceable.Active = False
        self.Owner.ClickReceiver.Receivable = False
        self.Owner.Sprite.Visible = True
        self.Owner.Collider.Ghost = True
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