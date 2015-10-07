import Zero
import Events
import Property
import VectorMath

class ShadePolymorpher:
    ShadeTable = Property.ResourceTable("ShadeTable")
    def Initialize(self, initializer):
        self.spriter = self.Space.CreateAtPosition("Sprite", self.Owner.Transform.WorldTranslation)
        self.spriter.Sprite.Visible = False
        self.spriter.AttachToRelative(self.Owner)
        
    def SetImage(self,name):
        self.spriter.Sprite.SpriteSource = self.ShadeTable.FindValue(name)
        self.spriter.Sprite.Visible = True
        self.spriter.Sprite.Color = VectorMath.Vec3(0,0,0,0.7)

Zero.RegisterComponent("ShadePolymorpher", ShadePolymorpher)