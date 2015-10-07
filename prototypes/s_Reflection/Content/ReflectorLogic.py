import Zero
import Events
import Property
import VectorMath

class ReflectorLogic:
    def Initialize(self, initializer):
        self.mydict = {}
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
    
    def OnCollisionEnd(self, CollisionEvent):
        if CollisionEvent.OtherObject.Name in self.mydict:
            self.mydict[CollisionEvent.OtherObject.Name][0].Destroy()
            del self.mydict[CollisionEvent.OtherObject.Name]
    def OnCollision(self, CollisionEvent):
        if not CollisionEvent.OtherObject.Name in self.mydict and CollisionEvent.OtherObject.Sprite:
            transformer = self.Space.CreateAtPosition("Sprite", self.GetReflect(CollisionEvent.OtherObject.Transform.Translation))
            self.mydict[CollisionEvent.OtherObject.Name] = (transformer,CollisionEvent.OtherObject)
            transformer.Sprite.SpriteSource = CollisionEvent.OtherObject.Sprite.SpriteSource
            transformer.Sprite.FlipY = True
            transformer.Sprite.BlendMode = Zero.BlendMode.Additive
    def OnLogicUpdate(self, UpdateEvent):
        for shade, entity in self.mydict.values():
            shade.Transform.Translation = self.GetReflect(entity.Transform.Translation)
            shade.Sprite.FlipX = entity.Sprite.FlipX
            shade.Transform.Rotation = entity.Transform.Rotation.inverted()
            shade.Transform.Scale = entity.Transform.Scale
    def GetReflect(self, pos):
        x = pos.x
        y = pos.y
        z = pos.z
        return VectorMath.Vec3(pos.x, -4 - (pos.y- -4), pos.z)
        
            
   
            
            
Zero.RegisterComponent("ReflectorLogic", ReflectorLogic)