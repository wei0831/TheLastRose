import Zero
import Events
import Property
import VectorMath
Vec3 = VectorMath.Vec3
class Menu:
    
    def Initialize(self, initializer):
        
        childlist = [child for child in self.Owner.Hierarchy.Children]
        self.childlist = sorted(childlist, key=lambda item:item.Transform.Translation.y)
        self.childdict = dict( ( child.Transform.Translation.y, idx) for idx, child in enumerate(self.childlist))
        
        self.idx = 0
        self.selected = childlist[self.idx]        
        self.Indicator = self.Space.FindObjectByName("Indicator")
        self.last_mouse_selected = childlist[self.idx]        
        
    def DirectSelect(self, child, IsMouse = False):
        if IsMouse:
            self.last_mouse_selected = child
        
        self.selected = child
        self.Indicator.Transform.Translation = self.selected.SpriteText.GetCharacterPosition(0) - Vec3(.35,0.2,0)
        
    def Select(self, idx):
        self.idx = idx % len(self.childlist)
        self.DirectSelect(self.childlist[self.idx])
        
    def SelectByY(self, y):
        self.Select(self.childdict[y])
        
    def Increment(self):
        self.Select(self.idx+1)
        
    def Decrement(self):
        self.Select(self.idx-1)
        

    def GetIndex(self):
        return self.idx
        
    def ResumeMouseSelect(self):
        self.SelectByY(self.last_mouse_selected.Transform.Translation.y)
        
    
    def GetActionCode(self):
        return self.selected.MenuItem.ActionCode

Zero.RegisterComponent("Menu", Menu)