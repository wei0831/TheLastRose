import Zero
import Events
import Property
import VectorMath

class AbilityStatus:
    def Initialize(self, initializer):
        self.PhysSkill = None
        self.TreeSkill = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.TreeSkill:
            if self.PhysSkill:
                self.TreeSkill.OnLogicUpdate(UpdateEvent, self.PhysSkill)
            else:
                self.TreeSkill.OnLogicUpdate(UpdateEvent)
                
        elif self.PhysSkill:
            self.PhysSkill.OnLogicUpdate(UpdateEvent)
        else:
            print ("No Power is Used!!")
            
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