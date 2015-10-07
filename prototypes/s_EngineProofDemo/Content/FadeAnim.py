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

        self.target = self.Owner.Sprite or self.Owner.SpriteText
        self.targetslist = tuple(item for item in (self.Owner.Sprite, self.Owner.SpriteText) if item)
                              
    def ApplyAlpha(self, target, alpha):        
        tc = target.Color
        target.Color = Vec4(tc.x, tc.y, tc.z, alpha)
        
            
    def CheckAlphaBound(self, alpha):
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
        return alpha
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:    
            # calculate new alpha
            c = self.target.Color 
            alpha = c.a + self.FadeDirection * (1. / self.FadingDuration) * UpdateEvent.Dt             
            alpha = self.CheckAlphaBound(alpha)
                        
            for target in self.targetslist:
                self.ApplyAlpha(target, alpha)
            
            
    def Off(self):
        self.Active = False
        
    def On(self):
        self.Active = True
        
    def Toggle(self):
        self.Active = not self.Active
        
    def FadeIn(self):
        self.Active = True
        self.ResetAlpha(0)
        self.FadeDirection = 1
        
    def FadeOut(self):
        self.Active = True
        self.ResetAlpha(1)
        self.FadeDirection = -1
        
    def ResetAlpha(self, alpha=1):
        
        for target in self.targetslist:
            self.ApplyAlpha(target, alpha)
            

Zero.RegisterComponent("FadeAnim", FadeAnim)