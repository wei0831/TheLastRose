import Zero
import Events
import Property
import VectorMath
import random
class DestroyFadeAnim:
    InvalidateColliderBox = Property.Bool(True)
    def Initialize(self, initializer):
        self.Activated = False
        if not self.Owner.DestroyInterface:
            self.Owner.AddComponentByName("DestroyInterface")
        
    def Destroy(self):
        if self.InvalidateColliderBox:
            self.Owner.Collider.Offset += VectorMath.Vec3(0, 0,9999)

        if not self.Activated:
            self.Activated = True
            self.Owner.FadeAnim.Active = True
            
            def waitmovieend():
                return not self.Owner.FadeAnim.Active
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
Zero.RegisterComponent("DestroyFadeAnim", DestroyFadeAnim)