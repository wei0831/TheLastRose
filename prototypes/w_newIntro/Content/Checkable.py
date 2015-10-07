import Zero
import Events
import Property
import VectorMath

class Checkable:
    def Initialize(self, initializer):
        self.activated = False
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.CanCheck and not self.activated:
            self.activated = True
            CollisionEvent.OtherObject.CanCheck.SetCheck(self.Owner.Transform.Translation)
            self.Owner.Sprite.Color = VectorMath.Vec4(1,1,1,1)

            
            
            #self.Owner.Sprite.SpriteSource = self.Space.FindObjectByName("Checker").Sprite.SpriteSource

            

Zero.RegisterComponent("Checkable", Checkable)