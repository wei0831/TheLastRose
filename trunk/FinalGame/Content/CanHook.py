import Zero
import Events
import Property
import VectorMath

class CanHook:
    def Initialize(self, initializer):
        self.hooked = False
        self.hookobject = None
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnCollision(self, CollisionEvent):
        if not self.hooked and CollisionEvent.OtherObject.Hookable and CollisionEvent.OtherObject.Hookable.Active:
            #if not self.Owner.PlayerController.IsOnGround() and Zero.Keyboard.KeyIsDown(Zero.Keys.W):
            if Zero.Keyboard.KeyIsDown(Zero.Keys.W) or Zero.Keyboard.KeyIsPressed(Zero.Keys.W):
                self.hookobject = CollisionEvent.OtherObject
                self.hookobject.Hookable.Hook(self.Owner)
                
                self.Owner.AddComponentByName("GravityEffect")
                self.Owner.GravityEffect.Strength = 5
                self.Owner.GravityEffect.Direction = VectorMath.Vec3(0,-1,0)
                
                self.Owner.AddComponentByName("DragEffect")
                if not self.Owner.Blowable:
                    self.Owner.AddComponentByName("Blowable")
                
                self.Owner.PlayerController.JumpActive = False
                self.Owner.PlayerGravityModifier.Active = False
                
                self.hooked = True
    def IsHooked(self):
        return self.hooked
        
    def ForceUnhooked(self):
        if self.hookobject:
            self.hookobject.Hookable.NonActivatable = True
    def OnLogicUpdate(self, UpdateEvent):
        if self.hooked and (not Zero.Keyboard.KeyIsDown(Zero.Keys.W) or (self.hookobject and self.hookobject.Hookable.NonActivatable)):
            if self.hookobject:
                self.hookobject.Hookable.UnHook()
                self.hookobject = None
            
            if self.Owner.Blowable:
                self.Owner.Blowable.Active = False
                self.Owner.RemoveComponentByName("Blowable")
            if self.Owner.GravityEffect:
                self.Owner.RemoveComponentByName("GravityEffect")
            if self.Owner.DragEffect:
                self.Owner.RemoveComponentByName("DragEffect")
            if self.Owner.PlayerGravityModifier:
                self.Owner.PlayerGravityModifier.Active = True
                
            
            self.Owner.PlayerController.JumpActive = True
            self.hooked = False
            
        
        

Zero.RegisterComponent("CanHook", CanHook)