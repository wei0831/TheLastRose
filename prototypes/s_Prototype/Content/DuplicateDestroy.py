import Zero
import Events
import Property
import VectorMath

class DuplicateDestroy:
    Code = Property.String("")
    
    def Initialize(self, initializer):
        if not self.Code:
            self.Code = self.Owner.Name
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def MatchCode(self, code):
        return self.Code == code
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.DuplicateDestroy:
            if CollisionEvent.OtherObject.DuplicateDestroy.MatchCode(self.Code):
                if self.Owner.DestroyInterface:
                    self.Owner.DestroyInterface.Destroy()
                else:
                    self.Owner.Destroy()
        
    
        

Zero.RegisterComponent("DuplicateDestroy", DuplicateDestroy)