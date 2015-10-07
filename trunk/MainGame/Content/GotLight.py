import Zero
import Events
import Property
import VectorMath

class GotLight:
    Light = Property.Cog()
    Size = Property.Float(.25)
    def Initialize(self, initializer):
        self.Light = self.Space.CreateAtPosition("LightCircle", self.Owner.Transform.Translation)
        self.Light.AttachToRelative(self.Owner)
        self.Light.SphereCollider.Radius = self.Size
    def ChangeSize(self, size):
        self.Size = size
        self.Light.SphereCollider.Radius = self.Size

Zero.RegisterComponent("GotLight", GotLight)