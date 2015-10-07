import Zero
import Events
import Property
import VectorMath
import random
class DestroyPlayAnim:
    InvalidateCollider = Property.Bool(True)
    def Initialize(self, initializer):
        self.Activated = False
        if not self.Owner.DestroyInterface:
            self.Owner.AddComponentByName("DestroyInterface")
    def Destroy(self):
        if not self.Activated:
            if self.InvalidateCollider:
                self.Owner.Collider.Offset += VectorMath.Vec3(0, 0, 999)
            
            self.Activated = True
            
            if not self.Owner.ActionList:
                self.Owner.AddComponentByName("ActionList")
            self.Owner.ActionList.EmptyAll()
            self.Owner.GrowthAnim.SetReverse(True)
            self.Owner.GrowthAnim.Active = True
                
            def waitmovieend():
                return not self.Owner.GrowthAnim.Active
            def destroy():
                self.Owner.Destroy()
            
            self.Owner.ActionList.AddCallback(callback=waitmovieend, 
                                              has_self=False, 
                                              blocking=True, 
                                              countdown=None)
                                              
            self.Owner.ActionList.AddCallback(callback=destroy, 
                                              has_self=False, 
                                              blocking=True, 
                                              countdown=0)
    def IsActivated(self):
        return self.Activated
Zero.RegisterComponent("DestroyPlayAnim", DestroyPlayAnim)