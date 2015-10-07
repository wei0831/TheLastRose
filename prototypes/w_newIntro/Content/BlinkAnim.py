import Zero
import Events
import Property
import VectorMath
import Color

class BlinkAnim:
    BlinkColor = Property.Color(VectorMath.Vec4(1,0,0,1))
    BlinkTick = Property.Int(3)
    Countdown = Property.Float(-1)
    Active = Property.Bool(False)

    def Initialize(self, initializer):
        self.blink_tick = self.BlinkTick
        self.blink_counter = 0
        self.oricolor = self.Owner.Sprite.Color
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    def SetCountDown(self, countdown):
        self.Countdown = countdown
        
    def OnLogicUpdate(self, UpdateEvent):
        
        if self.Active:
            if self.Countdown > 0:
                self.Countdown -= 1
            if self.Countdown == 0:
                self.Active = False
                self.Countdown = -1
            
            if self.blink_tick <= self.BlinkTick:
                self.blink_tick += 1
            if self.blink_tick >= self.BlinkTick:
                if not self.Owner.Sprite.Color == self.BlinkColor:
                    self.Owner.Sprite.Color = self.BlinkColor
                else:
                    self.Owner.Sprite.Color = self.oricolor
                self.blink_tick = 0
        else:
            c = self.Owner.Sprite.Color
            self.Owner.Sprite.Color = VectorMath.Vec4(self.oricolor.x,self.oricolor.y,self.oricolor.z,c.a)
            

Zero.RegisterComponent("BlinkAnim", BlinkAnim)