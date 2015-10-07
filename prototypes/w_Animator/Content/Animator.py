import Zero
import Events
import Property
import VectorMath

class Animator:
    
    Active = Property.Bool(True)
    End_GoBack_Start = Property.Bool(False)
    Repeat = Property.Int(0)

    SpriteResources = Property.ResourceTable()
    FramePerSecond = Property.Float(0.1)
    StartingFrame = Property.Int(0)
    CurrentFrame = Property.Int(0)
    timer = 0;
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.Owner.Sprite.SpriteSource = self.SpriteResources.GetResourceAt(self.CurrentFrame)
        self.repeatLast = self.Repeat
        self.maxFrame = self.SpriteResources.Size
        
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active : return
        
        self.timer += UpdateEvent.Dt
        if self.timer > self.FramePerSecond :
            self.timer = 0
            self.CurrentFrame += 1
            
            if self.CurrentFrame >= self.maxFrame:
                if self.repeatLast > 0:
                    self.repeatLast -= 1
                    self.CurrentFrame = 0
                else:
                    if self.End_GoBack_Start:
                        self.Owner.Sprite.SpriteSource = self.SpriteResources.GetResourceAt(0)
                    self.Active = False
                    return
                    
            self.Owner.Sprite.SpriteSource = self.SpriteResources.GetResourceAt(self.CurrentFrame)

Zero.RegisterComponent("Animator", Animator)