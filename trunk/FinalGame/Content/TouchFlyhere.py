import Zero
import Events
import Property
import VectorMath

class TouchFlyhere:
    HidingOffset = Property.Float(10)
    Normal = Property.Vector3(VectorMath.Vec3(0,1,0))
    def Initialize(self, initializer):
        self.destination = self.Owner.Transform.WorldTranslation
        hiding_vec = self.HidingOffset * self.Owner.Transform.TransformNormalLocal(self.Normal)

        self.Owner.Transform.WorldTranslation += hiding_vec
        self.Owner.Collider.Offset -= VectorMath.Vec3(0,self.HidingOffset, 0)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        Zero.Connect(self.Space, Events.LogicUpdate, self.FlyUpdate)
        Zero.Disconnect(self.Owner, Events.CollisionStarted, self)
    
    def FlyUpdate(self, UpdateEvent):
        t = self.Owner.Transform.WorldTranslation
        self.Owner.Transform.WorldTranslation = t * 0.9 + self.destination * 0.1
        
        if (self.Owner.Transform.WorldTranslation - self.destination).length() < 0.01:
            Zero.Disconnect(self.Space, Events.LogicUpdate, self)
            

Zero.RegisterComponent("TouchFlyhere", TouchFlyhere)