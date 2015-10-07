import Zero
import Events
import Property
import VectorMath

class TreeSkillMushroom:
    Name = Property.String("TreeSkillMushroom")
    
    def Initialize(self, initializer):
        self.powertext = "I use mushroom power!!"
        
    def OnLogicUpdate(self, UpdateEvent, physeffect = None):
        if physeffect:
            print (self.powertext[:-2] + " " + physeffect.GetModifier())
        else:
            print (self.powertext)
            

Zero.RegisterComponent("TreeSkillMushroom", TreeSkillMushroom)