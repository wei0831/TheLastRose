import Zero
import Events
import Property
import VectorMath
Vec3 = VectorMath.Vec3
import random


class AIMovementFloatCharge:
    Speed = Property.Float(1.0)
    InitialDirection = Property.Vector3(Vec3(1,0,0))
    Active = Property.Bool(True)
    DetectionBox = Property.Vector3(Vec3(5,5,1))    
    
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
        if not self.Owner.GravityEffect:
            self.Owner.AddComponentByName("GravityEffect")
            self.Owner.GravityEffect.Direction = Vec3(0,1,0)
            self.Owner.GravityEffect.Strength = self.Space.FindObjectByName("LevelSettings").GravityEffect.Strength
            
        self.InitialPosition = self.Owner.Transform.Translation
        self.Direction = self.InitialDirection
        self.resetcounter = 0
        self.waitcounter = 0
        self.SpeedMultiplier = 1
        self.dumbcounter = 0
        self.wandercounter = 0
        
        self.InitialPoint = self.Owner.Transform.Translation

            
        self.CurrentUpdate = self.Ensuring
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
    

    def Waiting(self):
        
        self.waitcounter -= 1        
        
        if self.resetcounter > 0:
            self.resetcounter -= 1
        elif self.resetcounter == 0:
            self.SpeedMultiplier = 0*0.2 + self.SpeedMultiplier * 0.8
        
        direct = self.Owner.PlayerDetectorInterface.GetDirection() 
        self.Direction = Vec3(1,0,0) if direct.x >= 0 else Vec3(-1,0,0)
        self.Owner.Sprite.FlipX = self.Direction.x > 0
        self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
        if self.waitcounter <= 0 and self.Owner.PlayerDetectorInterface.InRange():
            self.dumbcounter = 100
            self.CurrentUpdate = self.Attacking
        elif not self.Owner.PlayerDetectorInterface.InRange():
            self.dumbcounter = 50
            self.CurrentUpdate = self.Walking
            
            
    def Attacking(self):
        if not self.Owner.PlayerDetectorInterface.InRange():
            self.CurrentUpdate = self.Walking
            
        if self.dumbcounter > 0:
            self.dumbcounter -= 1
        else:
            self.CurrentUpdate = self.Walking
            self.dumbcounter = 100
        self.SpeedMultiplier = 1
        self.Direction = self.Owner.PlayerDetectorInterface.GetDirection() 
        
        
        self.Owner.Sprite.FlipX = self.Direction.x > 0
        
        
        self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
        
    def Walking(self):
        if self.dumbcounter <= 0 and self.Owner.PlayerDetectorInterface.InRange():
            if (self.Owner.PlayerDetectorInterface.GetDirection().x > 0) == self.Owner.Sprite.FlipX:
                self.CurrentUpdate = self.Waiting
                self.waitcounter = 20
        else:
            self.dumbcounter -= 1

        self.Owner.Sprite.FlipX = self.Owner.RigidBody.Velocity.x > 0
        if self.wandercounter <= 0:
            self.Owner.RigidBody.ApplyForce(Vec3(random.uniform(-300,300),random.uniform(-300,300),0))
            self.wandercounter = 150
        else:
            self.wandercounter -= 1
        diff = self.InitialPosition - self.Owner.Transform.Translation
        
        self.Owner.RigidBody.ApplyForce(0.01*diff + 1.5*Vec3(diff.x**3, diff.y**3, diff.z**3))
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            self.CurrentUpdate()
        
            
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.IsSentry:
            
            if abs(CollisionEvent.FirstPoint.WorldNormalTowardsOther.x) > 0.95:
                self.CurrentUpdate = self.Walking
                self.dumbcounter = 100
                direction = CollisionEvent.OtherObject.IsSentry.SentryDirection
                if direction.x == 0 and direction.y == 0:
                    self.Direction = Vec3(1,0,0) if CollisionEvent.FirstPoint.WorldNormalTowardsOther.x < 0 else Vec3(-1,0,0)
                else:
                    self.Direction = direction
        elif CollisionEvent.OtherObject.PlayerController:
            if self.CurrentUpdate == self.Attacking:
                self.CurrentUpdate = self.Waiting
                self.waitcounter = 100
                
            
    def SlowDownBy(self, SlowDownRatio, TimeSteps):
        pass

Zero.RegisterComponent("AIMovementFloatCharge", AIMovementFloatCharge)