import Zero
import Events
import Property
import VectorMath

class PhysSkillFire:
    Name = Property.String("PhysSkillFire")
    
    def Initialize(self, initializer):
        self.powertext = "I use fire power!!"
        self.modifiertext = "with fire!!"
        
    def OnLogicUpdate(self, UpdateEvent):
        print (self.powertext)
        
    def GetModifier(self):
        return self.modifiertext
        
        

Zero.RegisterComponent("PhysSkillFire", PhysSkillFire)