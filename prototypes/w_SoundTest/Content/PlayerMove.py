import Zero
import Events
import Property
import VectorMath

class PlayerMove:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.MouseUpdate, self.OnMouseUpdate)
        
    def OnMouseUpdate(self, MouseEvent):
        Pos = MouseEvent.ToWorldZPlane(0.0)
        Pos.z = 0
        self.Owner.Transform.Translation = Pos

Zero.RegisterComponent("PlayerMove", PlayerMove)