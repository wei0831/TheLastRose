import Zero
import Events
import Property
import VectorMath

class PhysSkillWorldtree:
    Name = Property.String("PhysSkillWorldtree")
    def Initialize(self, initializer):
        self.mouse = self.Space.FindObjectByName("MouseIndicator")
        
        
    def Modify(self, obj):
        pass
        
    def Perform(self, position):
        pass
        
Zero.RegisterComponent("PhysSkillWorldtree", PhysSkillWorldtree)