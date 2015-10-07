import Zero
import Events
import Property
import VectorMath

class WeatherDestroy:
    RainDropEffect = Property.Bool(True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        #obj = CollisionEvent.OtherObject
        pass
        #if(obj.WeatherObjects != None):
        #    WeatherDestory = Zero.ScriptEvent()
        #    WeatherDestory.Owner = self.Owner
        #    WeatherDestory.CollidePos = CollisionEvent.FirstPoint.WorldPoint
        #    WeatherDestory.RainDropEffect = self.RainDropEffect
        #    obj.DispatchEvent("WeatherDestory", WeatherDestory)

Zero.RegisterComponent("WeatherDestroy", WeatherDestroy)