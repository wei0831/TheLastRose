import Zero
import Events
import Property
import VectorMath

class PoisonAnim:
    Active = Property.Bool(True)
    Alpha = Property.Float(0.16)
    
    def Initialize(self, initializer):
        self.poisonanim = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active:
            if self.poisonanim:
                self.poisonanim.Destroy()
        else: 
            if not self.poisonanim:
                self.poisonanim = self.Space.CreateAtPosition("PoisonParticle", self.Owner.Transform.Translation)
                t = self.poisonanim.SpriteParticleSystem.Tint
                t.a = self.Alpha
                self.poisonanim.SpriteParticleSystem.Tint = t
                
                self.poisonanim.Transform.Scale = self.Owner.Transform.Scale * 0.1
                self.poisonanim.AttachToRelative(self.Owner)
                
                
                
    def Destroyed(self):
        if self.poisonanim:
            self.poisonanim.Destroy()


Zero.RegisterComponent("PoisonAnim", PoisonAnim)