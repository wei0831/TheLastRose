import Zero
import Events
import Property
import VectorMath
Vec3 = VectorMath.Vec3
import random
import math

class AIMovementFloatProjectile:
    Speed = Property.Float(1.0)
    InitialDirection = Property.Vector3(Vec3(1,0,0))
    
    Active = Property.Bool(True)
    DetectionBox = Property.Vector3(Vec3(5,5,1))    
    
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
        self.attackcounter = 0
        
        self.walkanim = self.AnimTable.FindResource("Walk")
        self.attackanim = self.AnimTable.FindResource("Attack")
        
        
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
        self.Owner.Sprite.FlipX = self.Direction.x < 0
        self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
        
        if self.waitcounter <= 0 and self.Owner.PlayerDetectorInterface.InRange():
            self.CurrentUpdate = self.Attacking
        elif not self.Owner.PlayerDetectorInterface.InRange():
            self.dumbcounter = 20
            self.CurrentUpdate = self.Walking
           
            
    def Attacking(self):
        if not self.Owner.Sprite.SpriteSource == self.walkanim:
            self.Owner.Sprite.SpriteSource = self.walkanim
        
        direction = self.Owner.PlayerDetectorInterface.GetDirection()
        length = direction.length()
        force = 20 * direction if length > 1.6 else -10*direction
        if force.y < 0:
            force.y *= 0.3
        self.Owner.RigidBody.ApplyForce(force)
        self.Owner.Sprite.FlipX = direction.x < 0
        
        self.attackcounter += 1
        if self.attackcounter == 75:
            self.CurrentUpdate = self.PerformShoot
            self.attackcounter = 0
        
        if not self.Owner.PlayerDetectorInterface.InRange():
            self.dumbcounter = 10
            self.CurrentUpdate = self.Walking
            
            
        
        
    def PerformShoot(self):
        if not self.Owner.Sprite.SpriteSource == self.attackanim:
            self.Owner.Sprite.SpriteSource = self.attackanim
            
        if self.Owner.Sprite.CurrentFrame == 1:
            bullet = self.Space.CreateAtPosition("EnemyBullet", self.Owner.Transform.Translation - Vec3(0,.35,0))
            
            direction = self.Owner.PlayerDetectorInterface.GetDirection()
            direction.normalize()
            bullet.Transform.RotateByAngles(Vec3(0,0,direction.angleZ()-math.pi*5/4))
            bullet.RigidBody.Velocity = direction * 6
            self.Owner.Sprite.FlipX = direction.x < 0
            self.CurrentUpdate = self.Attacking
        
        
        
    def Walking(self):
        
        if self.dumbcounter <= 0 and self.Owner.PlayerDetectorInterface.InRange():
                self.CurrentUpdate = self.Waiting
                self.waitcounter = 3
        else:
            self.dumbcounter -= 1

        self.Owner.Sprite.FlipX = self.Owner.RigidBody.Velocity.x < 0
        if self.wandercounter <= 0:
            self.Owner.RigidBody.ApplyForce(Vec3(random.uniform(-500,500),random.uniform(-400,500),0))
            self.wandercounter = 50
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
                self.dumbcounter = 30
                direction = CollisionEvent.OtherObject.IsSentry.SentryDirection
                if direction.x == 0 and direction.y == 0:
                    self.Direction = Vec3(1,0,0) if CollisionEvent.FirstPoint.WorldNormalTowardsOther.x < 0 else Vec3(-1,0,0)
                else:
                    self.Direction = direction
            
    def SlowDownBy(self, SlowDownRatio, TimeSteps):
        pass
        
Zero.RegisterComponent("AIMovementFloatProjectile", AIMovementFloatProjectile)