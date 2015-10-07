import Zero
import Events
import Property
import VectorMath

class HealthStatus:
    MaxHealth = Property.Float(100.0)
    
    def Initialize(self, initializer):
        self.health = self.MaxHealth
        self.isdead = False
        
    def AddHealth(self,health):
        if not self.isdead:
            self.health += health
            if self.health > self.MaxHealth:
                self.health = self.MaxHealth
                
            elif self.health < 0:
                self.isdead = True
                self.health = 0
        
    def GetHealth(self):
        return self.health
        
    def IsDead(self):
        return self.isdead

Zero.RegisterComponent("HealthStatus", HealthStatus)