import Zero
import Events
import Property
import VectorMath

class DestroyInterface:
    def Initialize(self, initializer):
        if self.Owner.DestroyCreateArchetype:
            self.Destroyer = self.Owner.DestroyCreateArchetype
        elif self.Owner.DestroyPlayAnim:
            self.Destroyer = self.Owner.DestroyPlayAnim
        else: 
            self.Destroyer = None
    def Destroy(self):
        if self.Destroyer:
            self.Destroyer.Destroy()
        else:
            self.Owner.Destroy()
Zero.RegisterComponent("DestroyInterface", DestroyInterface)