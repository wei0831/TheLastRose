import Zero
import Events
import Property
import VectorMath
import Action

class WeatherObjects:
    MaxLife = Property.Float(4)
        
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)       
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, self.MaxLife)
        Action.Call(sequence, self.Death)
       
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.Collider.Ghost == False:
            if CollisionEvent.OtherObject.NoRainDropEffect == None:
                self.Space.CreateAtPosition("RainDrop", CollisionEvent.FirstPoint.WorldPoint)
            self.Death()
        
    def Death(self):
        self.Owner.Destroy()
        
        

Zero.RegisterComponent("WeatherObjects", WeatherObjects)