import Zero
import Events
import Property
import VectorMath

class PhysSkillIce:
    Name = Property.String("PhysSkillIce")
    
    def Initialize(self, initializer):
        self.powertext = "I use ice power!!"
        self.modifiertext = "with ice!!"
        
    def OnLogicUpdate(self, UpdateEvent):
        print (self.powertext)
        
    def GetModifier(self):
        return self.modifiertext
        
Zero.RegisterComponent("PhysSkillIce", PhysSkillIce)