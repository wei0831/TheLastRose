import Zero
import Events
import Property
import VectorMath


class TimedDeath:
    LifeTime = Property.Float(1.0)
    Active = Property.Bool(False)
    DestroyAtTheEnd = Property.Bool(False)
    
    def Initialize(self, initializer):
        self.Callback = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def Activate(self, callback = 0):
        self.Active = True
        if callback != 0:
            self.SetCallBack(callback)
        
    def SetCallback(self, callback):
        self.Callback = callback
        
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active:
            pass
        else:
            self.LifeTime -= UpdateEvent.Dt
            if self.LifeTime <= 0:
                if self.Callback:
                    self.Callback(self)
                if self.DestroyAtTheEnd:
                    self.Owner.Destroy()

Zero.RegisterComponent("TimedDeath", TimedDeath)