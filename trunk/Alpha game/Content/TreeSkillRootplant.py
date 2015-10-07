import Zero
import Events
import Property
import VectorMath

class TreeSkillRootplant:
    Name = Property.String("TreeSkillRootplant")
    
    def Initialize(self, initializer):
        pass
        
    def Perform(self, position, physeffect = None):
        rootplant = self.Space.CreateAtPosition("Rootplant", position)
        if physeffect:
            physeffect.Modify(rootplant)
            

Zero.RegisterComponent("TreeSkillRootplant", TreeSkillRootplant)