import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class Parallax:
    Active = Property.Bool(True)
    DebugDraw= Property.Bool(False)
    OffsetY = Property.Float(0)
    ScaleX = Property.Float(2)
    ScaleY = Property.Float(2)
    Layer = Property.Int(-5)
    Image = Property.Resource("SpriteSource")
    Camera = Property.Cog()
    Player = Property.Cog()
    ScrollX = Property.Float(1.25)
    ScrollY = Property.Float(1)
    Org = Vec3(0, 0, 0)
    
    
    
    def Initialize(self, initializer):
        if not self.Active: return
        self.Owner.Transform.WorldTranslation = Vec3(self.Camera.Transform.WorldTranslation.x, self.Owner.Transform.WorldTranslation.y + self.OffsetY, self.Layer)
        self.Center = self.Space.Create("Sprite")
        self.Center.Transform.WorldTranslation = self.Owner.Transform.WorldTranslation
        self.Center.Sprite.SpriteSource = self.Image
        self.Center.Transform.Scale = Vec3(self.ScaleX, self.ScaleY, 1)  
        self.Center.AttachToRelative(self.Owner)
                
        self.Width = self.Center.Sprite.Size.x
        self.HalfWidth = self.Width/2
        self.DefaultY = self.Owner.Transform.WorldTranslation.y
     
        self.Right = self.Space.Create("Sprite")
        self.Right.Transform.WorldTranslation = self.Owner.Transform.WorldTranslation
        self.Right.Transform.WorldTranslation += Vec3(self.Width * self.ScaleX, 0, 0)
        self.Right.Sprite.SpriteSource = self.Image
        self.Right.Transform.Scale = Vec3(self.ScaleX, self.ScaleY, 1) 
        self.Right.AttachToRelative(self.Owner)
                
        self.Left = self.Space.Create("Sprite")
        self.Left.Transform.WorldTranslation = self.Owner.Transform.WorldTranslation
        self.Left.Transform.WorldTranslation -= Vec3(self.Width * self.ScaleX, 0, 0)
        self.Left.Sprite.SpriteSource = self.Image
        self.Left.Transform.Scale = Vec3(self.ScaleX, self.ScaleY, 1) 
        self.Left.AttachToRelative(self.Owner)
              
        if self.DebugDraw:
            self.Center.Sprite.Color = Vec4(0, 1, 0, 1)
            self.Right.Sprite.Color = Vec4(0, 0, 1, 1)
            self.Left.Sprite.Color = Vec4(1, 0, 0, 1)
            
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active: return
        vecDistance = self.Camera.Transform.WorldTranslation - self.Org
        vecDistance = Vec3(vecDistance.x * self.ScrollX, vecDistance.y * self.ScrollY + self.OffsetY, self.Layer)
        self.Owner.Transform.Translation = vecDistance
        self.CheckPlayerLocation()
        
    def CheckPlayerLocation(self):
        #case Right
        if self.Player.Transform.WorldTranslation.x > self.Right.Transform.WorldTranslation.x - self.HalfWidth:
            self.Left.Transform.WorldTranslation = self.Right.Transform.WorldTranslation + Vec3(self.Width * self.ScaleX, 0, 0)
            temp = self.Left
            self.Left = self.Center
            self.Center = self.Right
            self.Right = temp
    
        # case Left
        if self.Player.Transform.WorldTranslation.x < self.Left.Transform.WorldTranslation.x + self.HalfWidth:
            self.Right.Transform.WorldTranslation = self.Left.Transform.WorldTranslation - Vec3(self.Width * self.ScaleX, 0, 0)
            temp = self.Right
            self.Right = self.Center
            self.Center = self.Left
            self.Left = temp
    
Zero.RegisterComponent("Parallax", Parallax)