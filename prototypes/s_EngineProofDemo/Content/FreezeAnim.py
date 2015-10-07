import Zero
import Events
import Property
import VectorMath

class FreezeAnim:    
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        self.freezeanim = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active:
            if self.freezeanim:
                self.freezeanim.Destroy()
        else: 
            if not self.freezeanim:
                if not self.Owner == self.Owner.FindRoot():
                    self.freezeanim = self.Space.CreateAtPosition("IceParticle", self.Owner.FindRoot().Transform.Translation)
                    self.freezeanim.Transform.Scale = self.Owner.FindRoot().Transform.Scale
                    self.freezeanim.AttachToRelative(self.Owner.FindRoot())
                    self.freezeanim.Transform.Translation = self.Owner.Transform.Translation
                    self.freezeanim.AttachToRelative(self.Owner)
                else:
                    self.freezeanim = self.Space.CreateAtPosition("IceParticle", self.Owner.Transform.Translation)
                    self.freezeanim.Transform.Scale = self.Owner.Transform.Scale
                    self.freezeanim.AttachToRelative(self.Owner)
                
    def Destroyed(self):
        if self.freezeanim:
            self.freezeanim.Destroy()

Zero.RegisterComponent("FreezeAnim", FreezeAnim)
