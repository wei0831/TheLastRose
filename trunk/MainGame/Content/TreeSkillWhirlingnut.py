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
        whirlingnut.GravityEffect.Strength = 20.5
        
        def TestAnimActive(self):
            return not self.Owner.GrowthAnim.Active
        def ActivateHook(self):
            if self.Owner.Hookable and not self.Owner.Hookable.NonActivatable:
                self.Owner.Hookable.Active=True
        def Accelerate():
            whirlingnut.GravityEffect.Strength = 22.6
            
        whirlingnut.ActionList.AddCallback(callback=TestAnimActive, 
                                           has_self=True, blocking=True, countdown=None)
        whirlingnut.ActionList.AddCallback(callback=None, has_self=False, blocking=True, countdown=0.1)
        whirlingnut.ActionList.AddCallback(callback=ActivateHook,
                                           has_self=True, blocking=False, countdown=0)
        whirlingnut.ActionList.AddCallback(callback=Accelerate, 
                                           has_self=False, blocking=False, countdown=.3)
        
        if physeffect:
            physeffect.Modify(whirlingnut)
            
        return whirlingnut

Zero.RegisterComponent("TreeSkillWhirlingnut", TreeSkillWhirlingnut)