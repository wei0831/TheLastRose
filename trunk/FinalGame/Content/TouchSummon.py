import Zero
import Events
import Property
import VectorMath

class TouchSummon:    
    SummonSpeed = Property.Float(0.125)
    def Initialize(self, initializer):
        self.EnsureObserver()
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        self.EnsureObserver()
        for observer in self.observers:
            observer.Summoned.ShowAll()
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.FlyUpdate)
        Zero.Disconnect(self.Owner, Events.CollisionStarted, self)
    
    def FlyUpdate(self, UpdateEvent):
        
        invalids = []
        
        for summoned in self.observers:
            t = self.Owner.Transform.WorldTranslation
            summoned.Transform.WorldTranslation = t * self.SummonSpeed + summoned.Transform.WorldTranslation * (1-self.SummonSpeed)
            
        self.observers = [summoned for summoned in self.observers if not (summoned.Transform.WorldTranslation - self.Owner.Transform.WorldTranslation).length() < 0.01]
                
        if not self.observers:
            if self.Owner.DestroyInterface:
                self.Owner.DestroyInterface.Destroy()
            else:
                self.Owner.Destroy()
            
    def EnsureObserver(self):
        self.observers = []
        def Null():
            pass        
        self.EnsureObserver= Null
        

    def RegisterObserver(self,target):
        self.EnsureObserver()
        self.observers.append(target)

Zero.RegisterComponent("TouchSummon", TouchSummon)