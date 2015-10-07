import Zero
import Events
import Property
import VectorMath

class BurnableVine:
    def Initialize(self, initializer):
        self.BeginBurning = False
        Zero.Connect(self.Owner, "BurnEvent", self.OnBurn)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.BeginBurning:
            s = self.Owner.Sprite.Color 
            self.Owner.Sprite.Color = VectorMath.Vec4(s.x * 0.99, s.y * 0.99 , s.z * 0.99, 1)
            
            if s.x + s.y + s.z < 0.05:
                if self.Owner.DestroyInterface:
                    self.Owner.DestroyInterface.Destroy()
                    Zero.Disconnect(self.Space, Events.LogicUpdate, self)
                else:
                     self.Owner.Destroy()
        
    def OnBurn(self, BurnEvent):
        self.BeginBurning = True
        if not self.Owner.CanBurn:
            self.Owner.AddComponentByName("CanBurn")
            

Zero.RegisterComponent("BurnableVine", BurnableVine)