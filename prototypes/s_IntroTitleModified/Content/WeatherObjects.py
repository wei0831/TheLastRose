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
        #Zero.Connect(self.Owner, "WeatherDestory", self.OnWeatherDestory)   
         
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, self.MaxLife)
        Action.Call(sequence, self.Death)
       
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.Collider.Ghost == False:
            if CollisionEvent.OtherObject.NoRainDropEffect == None and not self.Done:
                self.Space.CreateAtPosition("RainDrop", CollisionEvent.FirstPoint.WorldPoint)
                self.Done = True 
            self.Death()
    
    #def OnWeatherDestory(self, WeatherEvent):
    #    if WeatherEvent.RainDropEffect and not self.Done:
    #        self.Space.CreateAtPosition("RainDrop", WeatherEvent.CollidePos)   
    #        self.Done = True 
    #    self.Death()
        
    def Death(self):
        self.Owner.Destroy()
        
        

Zero.RegisterComponent("WeatherObjects", WeatherObjects)