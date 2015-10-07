import Zero
import Events
import Property
import VectorMath

class Checkable:
    DarkenedColor = Property.Vector4(VectorMath.Vec4(0.5,0.5,0.5,1))
    
    def Initialize(self, initializer):
        self.CheckOut()
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.CanCheck and not self.activated:
            self.activated = True
            CollisionEvent.OtherObject.CanCheck.SetCheck(self.Owner)
            self.Owner.Sprite.Color = VectorMath.Vec4(1,1,1,1)
            
    def CheckOut(self):
        self.activated = False
        self.Owner.Sprite.Color = self.DarkenedColor
            
            

            

Zero.RegisterComponent("Checkable", Checkable)