import Zero
import Events
import Property
import VectorMath

class FreezeAnim:    
    Active = Property.Bool(True)
    Alpha = Property.Float(0.55)
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
                    
                    t = self.freezeanim.SpriteParticleSystem.Tint
                    t.a = self.Alpha
                    self.freezeanim.SpriteParticleSystem.Tint = t
                    
                    self.freezeanim.SphericalParticleEmitter.EmitterSize *= self.Owner.Transform.WorldScale.x
                    self.freezeanim.SphericalParticleEmitter.EmitRate *= self.Owner.Transform.WorldScale.x / 0.5
                    if self.freezeanim.SphericalParticleEmitter.EmitRate < 4:
                        self.freezeanim.SphericalParticleEmitter.EmitRate = 4
                    self.freezeanim.AttachToRelative(self.Owner)
                    
                
    def Destroyed(self):
        if self.freezeanim:
            self.freezeanim.Destroy()

Zero.RegisterComponent("FreezeAnim", FreezeAnim)
