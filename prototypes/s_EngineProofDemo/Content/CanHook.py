import Zero
import Events
import Property
import VectorMath

class CanHook:
    def Initialize(self, initializer):
        self.hooked = False
        self.hookobject = None
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnCollision(self, CollisionEvent):
        if not self.hooked and CollisionEvent.OtherObject.Hookable and CollisionEvent.OtherObject.Hookable.Active:
            
            self.hookobject = CollisionEvent.OtherObject
            self.hookobject.Hookable.Hook(self.Owner)
            
            self.Owner.AddComponentByName("GravityEffect")
            self.Owner.GravityEffect.Strength = 5
            self.Owner.GravityEffect.Direction = VectorMath.Vec3(0,-1,0)
            
            self.Owner.AddComponentByName("DragEffect")
            if not self.Owner.Blowable:
                self.Owner.AddComponentByName("Blowable")
            
            self.Owner.PlayerController.JumpActive = False
            
            self.hooked = True
            
    def OnLogicUpdate(self, UpdateEvent):
        
        if not self.hookobject or (self.hooked and Zero.Keyboard.KeyIsDown(Zero.Keys.S)):
            if self.hookobject:
                self.hookobject.Hookable.UnHook()
            
            if self.Owner.Blowable:
                self.Owner.Blowable.Active = False
                self.Owner.RemoveComponentByName("Blowable")
            if self.Owner.GravityEffect:
                self.Owner.RemoveComponentByName("GravityEffect")
            if self.Owner.DragEffect:
                self.Owner.RemoveComponentByName("DragEffect")
            
            self.Owner.PlayerController.JumpActive = True
            self.hooked = False
            
        
        

Zero.RegisterComponent("CanHook", CanHook)