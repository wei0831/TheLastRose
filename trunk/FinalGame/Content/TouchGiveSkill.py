import Zero
import Events
import Property
import VectorMath

class TouchGiveSkill:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, CollisionEvent):
        CollisionEvent.OtherObject.AbilityStatus.SwapPhysSkill("PhysSkillWorldtree")
        CollisionEvent.OtherObject.AbilityStatus.SwapTreeSkill("TreeSkillWorldtree")
        

Zero.RegisterComponent("TouchGiveSkill", TouchGiveSkill)