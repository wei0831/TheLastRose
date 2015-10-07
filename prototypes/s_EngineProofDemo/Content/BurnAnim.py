import Zero
import Events
import Property
import VectorMath

class BurnAnim:
    
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        self.burnanim = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active:
            if self.burnanim:
                self.burnanim.Destroy()
        else: 
            if not self.burnanim:
                self.burnanim = self.Space.CreateAtPosition("FireParticle", self.Owner.Transform.Translation)
                self.burnanim.Transform.Scale = self.Owner.Transform.Scale

                self.burnanim.AttachToRelative(self.Owner)
    
    def Destroyed(self):
        if self.burnanim:
            self.burnanim.Destroy()

Zero.RegisterComponent("BurnAnim", BurnAnim)