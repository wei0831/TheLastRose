import Zero
import Events
import Property
import VectorMath

class TouchAnimChange:
    Active = Property.Bool(True)
   
    AnimTable = Property.ResourceTable()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        self.Owner.Sprite.SpriteSource = self.AnimTable.FindValue("Activated")
        Zero.Disconnect(self.Owner, Events.CollisionStarted, self)
        
    def Reset(self):
        self.Owner.Sprite.SpriteSource = self.AnimTable.FindValue("NonActivated")
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def DeactivateAndReset(self):
        self.Owner.Sprite.SpriteSource = self.AnimTable.FindValue("NonActivated")
        Zero.Disconnect(self.Owner, Events.CollisionStarted, self)
    
    
    
        
        

Zero.RegisterComponent("TouchAnimChange", TouchAnimChange)