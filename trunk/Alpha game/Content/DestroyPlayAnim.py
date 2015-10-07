import Zero
import Events
import Property
import VectorMath

class DestroyPlayAnim:
    def Initialize(self, initializer):
        self.Activated = False
        if not self.Owner.DestroyInterface:
            self.Owner.AddComponentByName("DestroyInterface")
    def Destroy(self):
        if not self.Activated:
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
                                              countdown=1)

Zero.RegisterComponent("DestroyPlayAnim", DestroyPlayAnim)