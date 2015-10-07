import Zero
import Events
import Property
import VectorMath

class TreeSkillMushroom:
    Name = Property.String("TreeSkillMushroom")
    
    
    def Initialize(self, initializer):
        pass
                                          
        
    def Perform(self, position, physeffect = None):
        mushroom = self.Space.CreateAtPosition("Mushroom", position)
        if physeffect:
            physeffect.Modify(mushroom)
        

        if mushroom.TimedDeath:
            def DeactivateBounce(self):
                self.Owner.CanBounce.Active = False
                
            mushroom.TimedDeath.SetCallback(DeactivateBounce)
            mushroom.TimedDeath.Active = True
        return mushroom
            

Zero.RegisterComponent("TreeSkillMushroom", TreeSkillMushroom)