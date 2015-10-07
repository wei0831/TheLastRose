import Zero
import Events
import Property
import VectorMath

class LightReceiver:
    last_dist = Property.Float(9999)
    last_dominator = Property.Cog()
    semarphor = Property.Float(0)
    def Initialize(self, initializer):
        pass
        
    def AddObserver(self):
        self.semarphor += 1
        
    def RemoveObserver(self, alpha):
        self.semarphor -= 1
        
        self.last_dist = 9999
        self.last_dominator = None
        
        if self.semarphor == 0:
            self.Owner.Sprite.Color = VectorMath.Vec4(0,0,0,alpha)
            
    

Zero.RegisterComponent("LightReceiver", LightReceiver)