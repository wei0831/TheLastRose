import Zero
import Events
import Property
import VectorMath

class ParticleFadeAnim:
    Active = Property.Bool(True)
    DecaySpeed = Property.Float(0.01)
    DestroyAtEnd = Property.Bool(True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            self.Owner.SpriteParticleSystem.Tint *= VectorMath.Vec4(1,1,1,0.9)
            if self.Owner.SpriteParticleSystem.Tint.a < 0.01:
                self.Owner.Destroy()
            #if self.Owner.SphericalParticleEmitter.Size > 0:
            #    self.Owner.SphericalParticleEmitter.Size -= self.DecaySpeed
            #elif self.Owner.SphericalParticleEmitter.Size < 0:
            #    self.Owner.SphericalParticleEmitter.Size = 0
            #    if self.DestroyAtEnd:
            #        if self.Owner.DestroyInterface:
            #            self.Owner.DestroyInterface.Destroy()
            #        else:
            #            self.Owner.Destroy()
                

Zero.RegisterComponent("ParticleFadeAnim", ParticleFadeAnim)