import Zero
import Events
import Property
import VectorMath

class DuplicateDestroy:
    Code = Property.String("")
    Active = Property.Bool(True)
    
    def Initialize(self, initializer):
        if not self.Code:
            self.Code = self.Owner.Name
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def MatchCode(self, code):
        return self.Code == code
        
    def OnCollision(self, CollisionEvent):
        if self.Active:
            otherobj = CollisionEvent.OtherObject
            if otherobj.DuplicateDestroy and otherobj.DuplicateDestroy.Active:
                if otherobj.DuplicateDestroy.MatchCode(self.Code):
                    self.Owner.DuplicateDestroy.Active = False
                    otherobj.DuplicateDestroy.Active = False
                    
                    for obj in (self.Owner, otherobj):
                        if obj.CanBounce:
                                obj.CanBounce.Active = False
                        if obj.CanTeleport:
                            obj.CanTeleport.Active = False
                        if obj.Hookable:
                            obj.Hookable.NonActivatable = True
                        if obj.CanBurn:
                            obj.CanBurn.Active = False
                        if obj.CanFreeze:
                            obj.CanFreeze.Active = False
                        if obj.CanPoison:
                            obj.CanPoison.Active = False
                        obj.Collider.Ghost = True
                        if obj.DestroyInterface:
                            obj.DestroyInterface.Destroy()
                            
                            
                        else:
                            obj.Destroy()
                        
    
        

Zero.RegisterComponent("DuplicateDestroy", DuplicateDestroy)