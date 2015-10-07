import Zero
import Events
import Property
import VectorMath
import AIMovementPacing
Vec3 = VectorMath.Vec3

class AIMovementCharging:
    Speed = Property.Float(1.0)
    InitialDirection = Property.Vector3(Vec3(1,0,0))
    Active = Property.Bool(True)
    DetectionBox = Property.Vector3(Vec3(7,1,1))
    AnimTable = Property.ResourceTable()
    
    def Ensuring(self):
        self.EnsureAiMovementInterface()
        self.EnsureDetectorInterface()
        self.CurrentUpdate = self.Walking
    
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
        self.charge_x = 0
        
        self.walkanim = self.AnimTable.FindResource("Walk")
        self.slamanim = self.AnimTable.FindResource("Slam")

        self.CurrentUpdate = self.Ensuring
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
        
    def Waiting(self):         
        
        #initial check
        if not self.Owner.Sprite.SpriteSource == self.walkanim:
            self.Owner.Sprite.SpriteSource = self.walkanim
        # update
        self.waitcounter -= 1        
        
        # slow down
        self.SpeedMultiplier = 0*0.1 + self.SpeedMultiplier * 0.9
        
        # stop sprite
        self.Owner.Sprite.AnimationSpeed = 0
        
        # set direction
        direct = self.Owner.PlayerDetectorInterface.GetDirection() 
        self.Direction = Vec3(1,0,0) if direct.x >= 0 else Vec3(-1,0,0)
        self.Owner.Sprite.FlipX = self.Direction.x < 0
        self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
        
        # leaving condition
        if self.waitcounter <= 0 and self.Owner.PlayerDetectorInterface.InRange():
            self.dumbcounter = 100
            self.CurrentUpdate = self.Charging
            self.charge_x = self.Owner.Transform.Translation.x + direct.x
        elif not self.Owner.PlayerDetectorInterface.InRange():
            self.dumbcounter = 30
            self.CurrentUpdate = self.Walking
    
    def GradualReset(self, value, ratio):
        if self.resetcounter > 0:
            self.resetcounter -= 1
        elif self.resetcounter == 0:
            self.SpeedMultiplier = value*ratio + self.SpeedMultiplier * (1-ratio)
            
    def Slamming(self):
        #initial check
        if not self.Owner.Sprite.SpriteSource == self.slamanim:
            self.Owner.Sprite.SpriteSource = self.slamanim
            
        if self.Owner.Sprite.CurrentFrame == 3:
            self.waitcounter = 100
            self.CurrentUpdate = self.PreWalk
            self.Owner.Sprite.AnimationActive = False
            self.SpeedMultiplier = 1
            self.Owner.CanBounce.Active = True
            dir_modifier = 1 if self.Owner.Sprite.FlipX else -1
            hurtbox = self.Space.CreateAtPosition("HurtBox",self.Owner.Transform.Translation - Vec3(dir_modifier * .5,.5,0))
            hurtbox.Transform.Scale = Vec3(1.5,.5,1)
            hurtbox.TimedDeath.LifeTime = 0.1
            
            sandsmoke = self.Space.CreateAtPosition("SandSmokeParticle", self.Owner.Transform.Translation)
            t = sandsmoke.SpriteParticleSystem.Tint
            sandsmoke.SpriteParticleSystem.Tint = VectorMath.Vec4(t.x, t.y, t.z, 0.8)
            sandsmoke.SphericalParticleEmitter.EmitCount = 25
            sandsmoke.SphericalParticleEmitter.ResetCount()
            
            
            
    def PreWalk(self):
 
        self.waitcounter -= 1
        if self.waitcounter == 80:
            self.Owner.CanBounce.Active = False
        if self.waitcounter <= 0:
            self.Owner.Sprite.AnimationActive = True
            self.CurrentUpdate = self.Walking
        
        
        
    def Charging(self):
        #initial check
        if not self.Owner.Sprite.SpriteSource == self.walkanim:
            self.Owner.Sprite.SpriteSource = self.walkanim
        
        # update
        self.GradualReset(1.5, 0.1)

        # update sprite speed
        self.Owner.Sprite.AnimationSpeed = 1.3
        
        # update direction
        #direct = self.Owner.PlayerDetectorInterface.GetDirection() 
        #self.Direction = Vec3(1,0,0) if direct.x >= 0 else Vec3(-1,0,0)
        #self.Owner.Sprite.FlipX = self.Direction.x < 0
        self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
        
        # leaving condition 
        #(keep attacking only up to a duration)
        if self.dumbcounter > 0:
            self.dumbcounter -= 1
        else:
            self.CurrentUpdate = self.Walking
            self.dumbcounter = 100
        
        if abs(self.Owner.Transform.Translation.x - self.charge_x) < 1:
            self.CurrentUpdate = self.Slamming
        #if not self.Owner.PlayerDetectorInterface.InRange():
        #    self.CurrentUpdate = self.Walking
        
        
        
    def Walking(self):
        
        #initial check
        if not self.Owner.Sprite.SpriteSource == self.walkanim:
            self.Owner.Sprite.SpriteSource = self.walkanim
        
        # update direction
        self.GradualReset(0.4, 0.01)
        self.Owner.Sprite.FlipX = self.Direction.x < 0
        self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
        
        # reset sprite speed
        self.Owner.Sprite.AnimationSpeed = .5
        
        
        # leaving condition
        if self.dumbcounter <= 0:
            if self.Owner.PlayerDetectorInterface.InRange():
                if (self.Owner.PlayerDetectorInterface.GetDirection().x < 0) == self.Owner.Sprite.FlipX:
                    self.CurrentUpdate = self.Waiting
                    self.waitcounter = 30
        else:
            self.dumbcounter -= 1

        
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            self.CurrentUpdate()
        
            
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.IsSentry:
            if abs(CollisionEvent.FirstPoint.WorldNormalTowardsOther.x) > 0.95:
                self.CurrentUpdate = self.Walking
                self.dumbcounter = 30
                direction = CollisionEvent.OtherObject.IsSentry.SentryDirection
                if direction.x == 0 and direction.y == 0:
                    self.Direction = Vec3(1,0,0) if CollisionEvent.FirstPoint.WorldNormalTowardsOther.x < 0 else Vec3(-1,0,0)
                else:
                    self.Direction = direction

    def SlowDownBy(self, SlowDownRatio, TimeSteps):
        self.resetcounter = TimeSteps
        self.SpeedMultiplier = SlowDownRatio

Zero.RegisterComponent("AIMovementCharging", AIMovementCharging)