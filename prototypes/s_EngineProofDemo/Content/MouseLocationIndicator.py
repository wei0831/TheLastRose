import Zero
import Events
import Property
import VectorMath
import random
Vec3 = VectorMath.Vec3

class MouseLocationIndicator:
    Range = Property.Float(6.0)
    
    def Initialize(self, initializer):
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, Events.MouseUpdate, self.OnMouseUpdate)
        Zero.Connect(self.Space, Events.MouseUp, self.OnMouseUp)
        Zero.Connect(self.Space, Events.MouseDown, self.OnMouseDown)
        Zero.Connect(self.Space, Events.RightMouseUp, self.OnRightMouseUp)
        Zero.Connect(self.Space, Events.RightMouseDown, self.OnRightMouseDown)
        
        self.initial_size = self.Owner.Transform.Scale
        self.ball_size = self.Owner.SphereCollider.Radius
       
        self.hero = self.Space.FindObjectByName("Player")
        self.Active = False
        self.TouchAttackable = False
        self.TouchGrowable = False
        self.WithInRange = False
        self.MousePos = Vec3(0,0,0)
    
        
    def OnLogicUpdate(self, UpdateEvent):
        self.UpdateEnvironmentInfo()
        if self.Active and self.WithInRange:
            self.PerformAbsorb()
            
        target_color = VectorMath.Vec4(1, 1, 1, 0.25)
        target_scale = 1
        if self.WithInRange:
            if self.TouchAttackable:
                target_color = VectorMath.Vec4(1, 0, 0, 0.25)
                target_scale = 5
            elif not self.TouchAnnihilator and self.TouchGrowable:
                target_color = VectorMath.Vec4(0, 1, 0, 0.25)
                target_scale = 5
        self.Owner.Sprite.Color = target_color
        self.Owner.Transform.Scale = self.initial_size * target_scale
        self.Owner.SphereCollider.Radius = self.ball_size / target_scale
        
    def PerformAbsorb(self):
        heroClickEvent = Zero.ScriptEvent()
        heroClickEvent.Target = self.hero
        self.Owner.Region.DispatchEvent("heroClickEvent", heroClickEvent)
        
    def OnMouseUpdate(self, MouseUpdateEvent):
        self.MousePos = MouseUpdateEvent.ToWorldZPlane(0)
        self.Owner.Transform.Translation = self.MousePos
    
    def OnMouseDown(self, MouseDownEvent):
        self.Active = True
        
    def OnMouseUp(self, MouseUpEvent):
        self.Active = False
    
    def OnRightMouseDown(self, MouseDownEvent):
        if self.WithInRange and not self.TouchAnnihilator and self.TouchGrowable:
            self.hero.AbilityStatus.Perform(self.MousePos)
                
    def UpdateEnvironmentInfo(self):
        touched_objs = tuple(contactholder.OtherObject for contactholder in self.Owner.Collider.Contacts)
        self.TouchGrowable = any(tuple(obj.GrowableGround for obj in touched_objs))
        self.TouchAttackable = any(tuple(obj.ClickReceiver for obj in touched_objs))
        self.TouchAnnihilator = any(tuple(obj.PlantAnnihilator for obj in touched_objs))
        x2 = (self.MousePos.x  - self.hero.Transform.Translation.x)**2
        y2 = (self.MousePos.y  - self.hero.Transform.Translation.y)**2
        self.WithInRange = x2 + y2 < self.Range**2
        
    def OnRightMouseUp(self, MouseUpEvent):
        pass

Zero.RegisterComponent("MouseLocationIndicator", MouseLocationIndicator)