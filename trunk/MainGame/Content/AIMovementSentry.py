import Zero
import Events
import Property
import VectorMath
import random
Vec3 = VectorMath.Vec3

class AIMovementSentry:
    
    Speed = Property.Float(1.0)
    InitialDirection = Property.Vector3(Vec3(1,0,0))
    Active = Property.Bool(True)
    RandomStop = Property.Bool(True)
    RandomFlip = Property.Bool(True)
    
    def Initialize(self, initializer):
        self.Direction = self.InitialDirection
        self.resetcounter = 0
        self.SpeedMultiplier = 1
        self.target_multiplier = 1
        self.stopcounter = 0
        
        if not self.Owner.AIMovementInterface:
            self.Owner.AddComponentByName("AIMovementInterface")
            self.Owner.AIMovementInterface.Set(self)
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            self.resetcounter -= 1
            if self.resetcounter == 0:
                self.SpeedMultiplier = 1
            
            self.stopcounter -= 1
            
            self.SpeedMultiplier = self.SpeedMultiplier * .99 + 1*self.target_multiplier * 0.01
            
            self.Owner.Sprite.FlipX = self.Direction.x < 0
            self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
            
            if self.RandomStop and self.stopcounter <= 0:
                self.stopcounter = random.random() * 200 
                self.target_multiplier = random.random() * 2
                
            if self.RandomFlip and random.random() < 0.0001:
                self.Direction *= -1
                    
                    
            
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.IsSentry:
            if abs(CollisionEvent.FirstPoint.WorldNormalTowardsOther.x) > 0.95:
                direction = CollisionEvent.OtherObject.IsSentry.SentryDirection
                
                if direction.x == 0 and direction.y == 0:
                    self.Direction = Vec3(1,0,0) if CollisionEvent.FirstPoint.WorldNormalTowardsOther.x < 0 else Vec3(-1,0,0)
                else:
                    self.Direction = direction
            
    def SlowDownBy(self, SlowDownRatio, TimeSteps):
        self.resetcounter = TimeSteps
        self.SpeedMultiplier = SlowDownRatio
        
Zero.RegisterComponent("AIMovementSentry", AIMovementSentry)