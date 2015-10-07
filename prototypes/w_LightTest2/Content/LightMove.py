import Zero
import Events
import Property
import VectorMath

class LightMove:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.MouseUpdate, self.OnMouseUpdate)
        
    def OnMouseUpdate(self, MouseUpdate):
        mousePos = MouseUpdate.ToWorldZPlane(0.0)
        mousePos.z = 0
        self.Owner.Transform.WorldTranslation = mousePos

Zero.RegisterComponent("LightMove", LightMove)