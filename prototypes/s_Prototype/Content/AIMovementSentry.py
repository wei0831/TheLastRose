import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
class AIMovementSentry:
    
    Speed = Property.Float(1.0)
    InitialDirection = Property.Vector3(Vec3(1,0,0))
    Active = Property.Bool(True)
    
    def Initialize(self, initializer):
        self.Direction = self.InitialDirection
        self.resetcounter = 0
        self.SpeedMultiplier = 1
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            self.resetcounter -= 1
            if self.resetcounter == 0:
                self.SpeedMultiplier = 1
                
            
            self.Owner.Sprite.FlipX = self.Direction.x > 0
            self.Owner.Transform.Translation += self.Direction * self.Speed * self.SpeedMultiplier
            
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.IsSentry:
            direction = CollisionEvent.OtherObject.IsSentry.SentryDirection
            if direction.x == 0 and direction.y == 0:
                self.Direction = -self.Direction
            else:
                self.Direction = direction
            
    def SlowDownBy(self, SlowDownRatio, TimeSteps):
        self.resetcounter = TimeSteps
        self.SpeedMultiplier = SlowDownRatio
        
Zero.RegisterComponent("AIMovementSentry", AIMovementSentry)