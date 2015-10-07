import Zero
import Events
import Property
import VectorMath
import Action

class WeatherObjects:
    MaxerLife = Property.Float(7)
    Done = False
        
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)       
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, self.MaxerLife)
        Action.Call(sequence, self.Owner.Destroy)
       
    def OnCollision(self, CollisionEvent):
        if (CollisionEvent.OtherObject.Collider.Ghost == False and not self.Done) or CollisionEvent.OtherObject.WeatherDestroy:
            self.Done = True
            raindrop = self.Space.CreateAtPosition("RainDrop", CollisionEvent.FirstPoint.WorldPoint+VectorMath.Vec3(0,0,1))
            for child in self.Owner.Hierarchy.Children:
                raindrop.Sprite.Color = child.Sprite.Color
            self.Owner.Destroy()
            
        
        
        
        

Zero.RegisterComponent("WeatherObjects", WeatherObjects)