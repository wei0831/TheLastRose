import Zero
import Events
import Property
import VectorMath

Vec4 = VectorMath.Vec4

class FadeAnim:
    FadingDuration = Property.Float(1)
    Active = Property.Bool(True)
    FadeDirection = Property.Int(-1)
    Repeat = Property.Bool(False)
        
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            has_both = False
            
            # select the proper target for fading
            if self.Owner.Sprite:
                target = self.Owner.Sprite
                if self.Owner.SpriteText:
                    has_both = True
            else:
                target = self.Owner.SpriteText
    
            # calculate new alpha
            c = target.Color
            alpha = c.a + self.FadeDirection * (1. / self.FadingDuration) * UpdateEvent.Dt             
            
            # if alpha out of bounds
            if alpha < 0:
                alpha = 0
                if not self.Repeat:
                    self.Active = False
                else:
                    self.FadeDirection = 1
            elif alpha > 1:
                alpha = 1
                if not self.Repeat:
                    self.Active = False
                else:
                    self.FadeDirection = -1
            
            # set alpha to color
            target.Color = Vec4(c.x, c.y, c.z, alpha)
            
            # synchronize text and sprite alpha
            if has_both:
                tc = self.Owner.SpriteText.Color
                self.Owner.SpriteText.Color = Vec4(tc.x, tc.y, tc.z, alpha)
            
    def Off(self):
        self.Active = False
        
    def On(self):
        self.Active = True
        
    def Toggle(self):
        self.Active = not self.Active
        
    def ResetAlpha(self, alpha=1):
        targetlist = []
        if self.Owner.Sprite:
            targetlist.append(self.Owner.Sprite)
        if self.Owner.SpriteText:
            targetlist.append(self.Owner.SpriteText)
        
        for target in targetlist:
            c = target.Color
            target.Color = VectorMath.Vec4(c.x, c.y, c.z, alpha)

Zero.RegisterComponent("FadeAnim", FadeAnim)