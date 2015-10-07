import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class GrowthAnim:
    VerticalGrowthCurve = Property.SampleCurve()
    HorizontalGrowhCurve = Property.SampleCurve()
    Active = Property.Bool(True)
    Duration = Property.Float(1.0)
    Reverse = Property.Bool(False)
    Repeat = Property.Bool(False)
    Scaling = Property.Float(1.0)
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
            z_scale = self.Owner.Transform.Scale.z
            x_scale = self.HorizontalGrowhCurve.Sample(self.age) * self.Scaling
            y_scale = self.VerticalGrowthCurve.Sample(self.age) * self.Scaling
            
            self.Owner.Transform.Scale = Vec3(x_scale, y_scale, z_scale)
            
            
          
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
      
        
        
        

Zero.RegisterComponent("GrowthAnim", GrowthAnim)