import Zero
import Events
import Property
import VectorMath

class Pause:
    Parent = Property.Resource("Level")
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.Space):
           self.Parent.TimeSpace.TogglePause()
        
    

Zero.RegisterComponent("Pause", Pause)