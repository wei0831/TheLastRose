import Zero
import Events
import Property
import VectorMath

class TriggerDoor:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "TriggerEvent", self.OnTrigger)
        
    def OnTrigger(self, TriggerEvent):        
        
        if self.Owner.FadeAnim:
            self.Owner.FadeAnim.Active = True

        if self.Owner.Sprite:
            s = self.Owner.Sprite.Color 
            self.Owner.Sprite.Color = VectorMath.Vec4(s.x, s.y, s.z, s.a * 0)
            
        if self.Owner.Collider:
            self.Owner.Collider.Ghost = True
        if self.Owner.Hierarchy:
            for child in self.Owner.Hierarchy.Children:
                if child.Sprite.Color:
                    s = child.Sprite.Color 
                    child.Sprite.Color = VectorMath.Vec4(s.x, s.y, s.z, s.a * 0)
                    if child.Collider:
                        child.Collider.Ghost = True
        
        if self.Owner.IsSentry:
            self.Owner.RemoveComponentByName("IsSentry")
    

Zero.RegisterComponent("TriggerDoor", TriggerDoor)