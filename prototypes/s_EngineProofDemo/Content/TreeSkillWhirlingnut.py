import Zero
import Events
import Property
import VectorMath

class TreeSkillWhirlingnut:
    Name = Property.String("TreeSkillWhirlingnut")
    
    def Initialize(self, initializer):
        pass
        
    def Perform(self, position, physeffect = None):
        whirlingnut = self.Space.CreateAtPosition("Whirlingnut", position)
        whirlingnut.AddComponentByName("ActionList")
        
        def TestAnimActive(self):
            return not self.Owner.GrowthAnim.Active
        def ActivateHook(self):
            if not self.Owner.Hookable.NonActivatable:
                self.Owner.Hookable.Active=True
            
        whirlingnut.ActionList.AddCallback(callback=TestAnimActive, 
                                           has_self=True, blocking=True, countdown=None)
        whirlingnut.ActionList.AddCallback(callback=None, has_self=False, blocking=True, countdown=0.1)
        whirlingnut.ActionList.AddCallback(callback=ActivateHook,
                                           has_self=True, blocking=False, countdown=0)
                                            
        
        if physeffect:
            physeffect.Modify(whirlingnut)
            
            

Zero.RegisterComponent("TreeSkillWhirlingnut", TreeSkillWhirlingnut)