import Zero
import Events
import Property
import VectorMath
import Action

class WeatherObjects:
    MaxLife = Property.Float(4)
    Done = False
        
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)       
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, self.MaxLife)
        Action.Call(sequence, self.Owner.Destroy)
       
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.Collider.Ghost == False and not self.Done :
            self.Done = True
            self.Space.CreateAtPosition("RainDrop", CollisionEvent.FirstPoint.WorldPoint)
            self.Owner.Destroy()
        elif CollisionEvent.OtherObject.WeatherDestroy:
            self.Done = True
            self.Space.CreateAtPosition("RainDrop", CollisionEvent.FirstPoint.WorldPoint)
            self.Owner.Destroy()
            
        
        
        
        

Zero.RegisterComponent("WeatherObjects", WeatherObjects)