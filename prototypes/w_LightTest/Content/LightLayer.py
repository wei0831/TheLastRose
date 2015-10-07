import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class LightLayer:
    Rec_W = 1
    Rec_H = 1
    Gap = 0
    HardCodeFix = 15
    LayerDeapth = 5
    Ratio = 16.0/9.0
    Color = Vec4(0, 0, 0, 0.1)

    def Initialize(self, initializer):
        self.GenerateLayer()

    def GenerateLayer(self):
        self.cameraSize = self.Owner.Camera.Size
        self.cameraCenter = self.Owner.Transform.Translation
        self.cameraHalfW = self.cameraSize * 0.5 * self.Ratio
        self.cameraHalfH = self.cameraSize * 0.5 * self.Ratio
        self.layerTopLeft = Vec3(self.cameraCenter.x - self.cameraHalfW, self.cameraCenter.y + self.cameraHalfH, self.LayerDeapth)
        self.RecsInX = int(((self.cameraHalfW * 2) / self.Rec_W) + 0.5)
        self.RecsInX += self.HardCodeFix
        self.RecsInY = int(((self.cameraHalfH * 2) / self.Rec_H) + 0.5)
        self.RecsInY += self.HardCodeFix
        
        self.RecArray = [[0 for x in range(self.RecsInX)] for x in range(self.RecsInY)] 
        for i, col in enumerate(self.RecArray):
            for j, item in enumerate(col):
                item = self.Space.CreateAtPosition("LightRec", self.layerTopLeft + Vec3((self.Rec_W - self.Gap)* j, -1 * (self.Rec_H - self.Gap) * i, 0))
                item.Transform.Scale = Vec3(item.Transform.Scale.x * self.Rec_W, item.Transform.Scale.y * self.Rec_H, item.Transform.Scale.z)
                item.Sprite.Color = self.Color
                item.AttachToRelative(self.Owner)
                
Zero.RegisterComponent("LightLayer", LightLayer)