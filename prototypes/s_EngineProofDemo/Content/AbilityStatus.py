import Zero
import Events
import Property
import VectorMath

class AbilityStatus:
    def Initialize(self, initializer):
        self.PhysSkill = None
        self.TreeSkill = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def Perform(self, position):
        if self.TreeSkill:
            self.TreeSkill.Perform(position, self.PhysSkill)
        elif self.PhysSkill:
            self.PhysSkill.Perform(position)
        else:
            pass
        
    
    def OnLogicUpdate(self, UpdateEvent):
        pass
        
            
    def SwapPhysSkill(self, skillname):
        self.EmptyPhysSkill()
        if skillname:
            self.Owner.AddComponentByName(skillname)
            self.PhysSkill = getattr(self.Owner,skillname)

        
    def SwapTreeSkill(self, skillname):
        
        self.EmptyTreeSkill()
        if skillname:
            self.Owner.AddComponentByName(skillname)
            self.TreeSkill = getattr(self.Owner, skillname)
        
        
    def EmptyPhysSkill(self):
        if self.PhysSkill:
            self.Owner.RemoveComponentByName(self.PhysSkill.Name)
            self.PhysSkill = None
        
    def EmptyTreeSkill(self):
        if self.TreeSkill:
            self.Owner.RemoveComponentByName(self.TreeSkill.Name)
            self.TreeSkill = None
        
    def EmptySkills(self):
        self.EmptyPhysSkill()
        self.EmptyTreeSkill()
    
    def NoPhysSkill(self):
        return not self.PhysSkill
    
    def NoTreeSkill(self):
        return not self.TreeSkill
        

Zero.RegisterComponent("AbilityStatus", AbilityStatus)