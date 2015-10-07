import Zero
import Events
import Property
import VectorMath

class HealthStatus:
    MaxHealth = Property.Float(100.0)
    RegenRate = Property.Float(0)
    Updatable = Property.Bool(True)
    UseVisualCue = Property.Bool(False)
    
    def Initialize(self, initializer):
        self.health = self.MaxHealth
        self.isdead = False
        self.init_regen = self.RegenRate
        if self.UseVisualCue:
            self.healthparticle = self.Space.CreateAtPosition("HealthParticle", self.Owner.Transform.WorldTranslation)
            self.healthparticle.AttachToRelative(self.Owner)
            self.healthparticle.SphericalParticleEmitter.Active = False
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def AddHealth(self,health):

        
        
        if self.Updatable:
            if not self.isdead:
                self.health += health
                
                if health < 0 and self.UseVisualCue:
                    self.healthparticle.SphericalParticleEmitter.Active = True
                    self.healthparticle.SphericalParticleEmitter.ResetCount()
                
                if self.health > self.MaxHealth:
                    self.health = self.MaxHealth
                    
                elif self.health < 0:
                    self.isdead = True
                    if self.Owner.CanFancyDie:
                        self.Owner.CanFancyDie.Die()
                    self.health = 0
                    
                    
                    

    def GetHealth(self):
        return self.health
        
    def IsDead(self):
        return self.isdead
        
    def ResetRegen(self):
        self.RegenRate = self.init_regen
        
    def RegenHealth(self, regen_rate):
        self.RegenRate = regen_rate
        
    def ResetHealth(self):
        self.health = self.MaxHealth
        self.isdead = False
    
    def Reset(self):
        self.ResetHealth()
        self.ResetRegen()
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.RegenRate != 0 and self.Updatable:
            self.AddHealth(UpdateEvent.Dt * self.RegenRate)

Zero.RegisterComponent("HealthStatus", HealthStatus)