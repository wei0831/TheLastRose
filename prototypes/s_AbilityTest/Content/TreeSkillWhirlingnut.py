import Zero
import Events
import Property
import VectorMath

class TreeSkillWhirlingnut:
    Name = Property.String("TreeSkillWhirlingnut")
    
    def Initialize(self, initializer):
        self.powertext = "I use whirlingnut power!!"
        
    def OnLogicUpdate(self, UpdateEvent, physeffect = None):
        if physeffect:
            print (self.powertext[:-2] + " " + physeffect.GetModifier())
        else:
            print (self.powertext)
            

Zero.RegisterComponent("TreeSkillWhirlingnut", TreeSkillWhirlingnut)