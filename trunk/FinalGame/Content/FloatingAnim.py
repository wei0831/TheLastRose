import Zero
import Events
import Property
import VectorMath

class FloatingAnim:
    def Initialize(self, initializer):
        pass
            
class GrowthAnim:
    FloatingCurve = Property.SampleCurve()
    RotatingCurve = Property.SampleCurve()
    Active = Property.Bool(True)
    Duration = Property.Float(1.0)
    Reverse = Property.Bool(False)
    Repeat = Property.Bool(False)
    
    def Initialize(self, initializer):
        self.SetReverse(self.Reverse)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            # Update age and do out of bounds check
            self.age += UpdateEvent.Dt * self.direction / self.Duration
            if self.age > 1:
                self.age = 1
                self.Active = False
                if self.Repeat:
                    self.ReversePlay()
            elif self.age < 0:
                self.age = 0
                self.Active = False
                if self.Repeat:
                    self.ReversePlay()
            
            # set new transform
            
            
            
            self.Owner.Transform.Translation += VectorMath.Vec3(0,1,0)
            
            
          
    def On(self):
        self.Active = True
        
    def Off(self):
        self.Active = False
        
    def Toggle(self):
        self.Active = not self.Active  
        
    def Reset(self):
        if not self.Reverse:
            self.age = 0
        else:
            self.age = 1
            
    def SetReverse(self, want_reverse):
        self.Reverse = want_reverse
        
        if want_reverse:
            self.direction = -1
            self.age = 1
        else:
            self.direction = +1
            self.age = 0
            
    def ToggleReverse(self):
        self.Reverse = not self.Reverse
        self.direction *= -1
    
    def ReversePlay(self):
        self.ToggleReverse()
        self.Reset()
        self.On()
      
        
        
Zero.RegisterComponent("FloatingAnim", FloatingAnim)