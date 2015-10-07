import Zero
import Events
import Property
import VectorMath
import Action

class TreeSkillRootplant:
    Name = Property.String("TreeSkillRootplant")
    
    def Initialize(self, initializer):
        pass
        
    def Perform(self, position, physeffect = None):
        rootplant = self.Space.CreateAtPosition("Rootplant", position)
    
        if physeffect:
            physeffect.Modify(rootplant)
            
            
        def Activate():
            for child in rootplant.Hierarchy.Children:
                if child.CanTeleport:
                    child.CanTeleport.Active = True

            
        seq = Action.Sequence(rootplant.Actions)
        Action.Delay(seq, 0.5)
        Action.Call(seq, Activate)
        
        return rootplant
            

Zero.RegisterComponent("TreeSkillRootplant", TreeSkillRootplant)