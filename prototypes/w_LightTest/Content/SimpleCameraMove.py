import Zero
import Events
import Property
import VectorMath

class SimpleCameraMove:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if Zero.Keyboard.KeyIsDown(Zero.Keys.Right):
            self.Owner.Transform.Translation += VectorMath.Vec3(1, 0, 0)
            
        if Zero.Keyboard.KeyIsDown(Zero.Keys.Left):
            self.Owner.Transform.Translation += VectorMath.Vec3(-1, 0, 0)

        if Zero.Keyboard.KeyIsDown(Zero.Keys.Up):
            self.Owner.Transform.Translation += VectorMath.Vec3(0, 1, 0)
            
        if Zero.Keyboard.KeyIsDown(Zero.Keys.Down):
            self.Owner.Transform.Translation += VectorMath.Vec3(0, -1, 0)  
            

Zero.RegisterComponent("SimpleCameraMove", SimpleCameraMove)