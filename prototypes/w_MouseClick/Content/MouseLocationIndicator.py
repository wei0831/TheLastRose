import Zero
import Events
import Property
import VectorMath

class MouseLocationIndicator:
    withInRange = False
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, Events.MouseUpdate, self.OnMouseUpdate)
        Zero.Connect(self.Space, Events.MouseUp, self.OnMouseUp)
        Zero.Connect(self.Space, Events.MouseDown, self.OnMouseDown)
        self.hero = self.Space.FindObjectByName("Hero")
        
    def OnLogicUpdate(self, UpdateEvent):
        pass
            
    def OnMouseUpdate(self, MouseUpdateEvent):
        self.mousePos = MouseUpdateEvent.ToWorldZPlane(0.0)
        self.Owner.Transform.Translation = self.mousePos

    def OnMouseDown(self, MouseDownEvent):
        self.Owner.Sprite.Color = VectorMath.Vec4(1, 0, 0, 0.25)
        
        heroClickEvent = Zero.ScriptEvent()
        heroClickEvent.Target = self.hero
        heroClickEvent.MaxRangeSqrt = 36
        self.Owner.Region.DispatchEvent("heroClickEvent", heroClickEvent)
        
    def OnMouseUp(self, MouseUpEvent):
        self.Owner.Sprite.Color = VectorMath.Vec4(0, 1, 0, 0.25)
        
    

Zero.RegisterComponent("MouseLocationIndicator", MouseLocationIndicator)