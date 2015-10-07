import Zero
import Events
import Property
import VectorMath
import math
class AbilityStatus:
    
    def Initialize(self, initializer):
        self.PhysSkill = None
        self.TreeSkill = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def Perform(self, position, pre_rotate = None):
        if self.TreeSkill:
            tree = self.TreeSkill.Perform(position, self.PhysSkill)
            
            if pre_rotate:
                tree.Transform.RotateByAngles(VectorMath.Vec3(0,0,pre_rotate.angleZ()-math.pi/2))
            if tree.Name == "Mushroom":
                tree.CanBounce.ToDirection(pre_rotate)
            
        elif self.PhysSkill:
            self.PhysSkill.Perform(position)
        else:
            pass
        
        #if self.GetTreeSkillName() == "TreeSkillWhirlingnut" and self.GetPhysSkillName() == "PhysSkillIce":
        #    tree.Transform.Translation *= VectorMath.Vec3(1,1,-1)
        

            
        
    
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

    def GetTreeSkillName(self):
        if self.TreeSkill:
            return self.TreeSkill.Name
        else:
            return ""
    def GetPhysSkillName(self):
        if self.PhysSkill:
            return self.PhysSkill.Name
        else:
            return ""

Zero.RegisterComponent("AbilityStatus", AbilityStatus)