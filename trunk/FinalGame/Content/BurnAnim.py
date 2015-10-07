import Zero
import Events
import Property
import VectorMath
import Action
class BurnAnim:
    
    Active = Property.Bool(True)
    Alpha = Property.Float(0.26)
    Amplifier = Property.Float(1)
    
    def Initialize(self, initializer):
        self.burnanim = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):

        if not self.Active:
            if self.burnanim:
                self.burnanim.DetachRelative()
                self.burnanim.Destroy()
        else: 
            if not self.burnanim:
                
                self.burnanim = self.Space.CreateAtPosition("FireParticle", self.Owner.Transform.WorldTranslation)
                t = self.burnanim.SpriteParticleSystem.Tint
                t.a = self.Alpha
                self.burnanim.SpriteParticleSystem.Tint = t
                
                self.burnanim.SphericalParticleEmitter.EmitRate *= self.Amplifier 
                self.burnanim.Transform.WorldScale = self.Owner.Transform.WorldScale

                self.burnanim.AttachToRelative(self.Owner)

        if self.burnanim:        
            t = self.burnanim.SpriteParticleSystem.Tint
            t.a = self.Alpha
            self.burnanim.SpriteParticleSystem.Tint = t
    
    def GetAnim(self):
        
        return self.burnanim
                
    
    def Destroyed(self):
        if self.burnanim:
            self.burnanim.DetachRelative()
            seq = Action.Sequence(self.burnanim)
            self.burnanim.SphericalParticleEmitter.EmitRate = 0
            Action.Delay(seq, 1)
            Action.Call(seq, lambda:self.burnanim.Destroy)
            

Zero.RegisterComponent("BurnAnim", BurnAnim)