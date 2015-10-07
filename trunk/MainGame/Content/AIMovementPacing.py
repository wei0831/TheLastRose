import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class AIMovementPacing:
    Duration = Property.Float(1.0)
    Speed = Property.Float(1.0)
    Direction = Property.Int(+1)
    Active = Property.Bool(+1)
    SpeedMultiplier = Property.Float(1.0)
    
    def Initialize(self, initializer):
        self.accum_dt = 0
        self.init_direction = self.Direction
        self.resetcounter = 0
        if not self.Owner.AIMovementInterface:
            self.Owner.AddComponentByName("AIMovementInterface")
            self.Owner.AIMovementInterface.Set(self)
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            if self.resetcounter > 0:
                self.resetcounter -= 1
            else:
                self.SpeedMultiplier = 1
                
            self.Owner.Sprite.FlipX = self.Direction < 0
            self.Owner.Transform.Translation += Vec3(self.Direction,0,0) * self.Speed * self.SpeedMultiplier

            self.accum_dt += UpdateEvent.Dt * self.Direction * self.init_direction
            if self.accum_dt > self.Duration:
                self.Direction = -1
            elif self.accum_dt < 0:
                self.Direction = +1
            
    def SlowDownBy(self, SlowDownRatio, TimeSteps):
        self.resetcounter = TimeSteps
        self.SpeedMultiplier = SlowDownRatio

Zero.RegisterComponent("AIMovementPacing", AIMovementPacing)