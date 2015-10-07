import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class LightLayer:
    Rec_W = 0.85
    Rec_H = 0.85
    Rec_Z = 2
    Gap = 0
    HardCodeFix = 0
    LayerDeapth = 5
    Ratio = 16.0/9.0
    Color = Vec4(0, 0, 0, 0)
    DefaultAlpha = Property.Float(0.5)
    DebugDraw = Property.Float(False)
    
    def Initialize(self, initializer):
        self.Color.w = self.DefaultAlpha
        self.GenerateLayer()

    def GenerateLayer(self):
        self.cameraSize = self.Owner.Camera.Size
        self.cameraCenter = self.Owner.Transform.Translation
        self.cameraHalfW = self.cameraSize * 0.5 * self.Ratio
        self.cameraHalfH = self.cameraSize * 0.5 * self.Ratio
        self.layerTopLeft = Vec3(self.cameraCenter.x - self.cameraHalfW, self.cameraCenter.y + self.cameraHalfH, self.LayerDeapth)
        self.RecsInX = int(((self.cameraHalfW * 2.0) / (self.Rec_W - self.Gap)) + 0.5)
        self.RecsInY = int(((self.cameraHalfH * 2.0) / (self.Rec_H - self.Gap)) + 0.5)
        
        self.RecArray = [[0 for x in range(self.RecsInX)] for x in range(self.RecsInY)] 
        for i, col in enumerate(self.RecArray):
            for j, item in enumerate(col):
                item = self.Space.CreateAtPosition("LightRec", self.layerTopLeft + Vec3((self.Rec_W - self.Gap)* j, -1 * (self.Rec_H - self.Gap) * i, 0))
                item.Transform.Scale = Vec3(item.Transform.Scale.x * self.Rec_W, item.Transform.Scale.y * self.Rec_H, self.Rec_Z)
                item.Sprite.Color = self.Color
                item.LightReciever.DefaultAlpha = self.DefaultAlpha
                if self.DebugDraw : 
                    item.SpriteText.Text = str(j) + " , " + str(i)
                    print(item.SpriteText.Text)
                item.AttachToRelative(self.Owner)
                
                
    def SetAlpha(self, alpha):
       for i, col in enumerate(self.RecArray):
            for j, item in enumerate(col):
                item.Sprite.Color = Vec3(item.Sprite.Color.x, item.Sprite.Color.y, item.Sprite.Color.z, alpha)
                
Zero.RegisterComponent("LightLayer", LightLayer)