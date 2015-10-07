import Zero
import Events
import Property
import VectorMath
import math

Vec3 = VectorMath.Vec3

class PlayerController:
    JumpStrength = Property.Float(2.0)
    MoveForce = Property.Float(3.0)
    JumpActive = Property.Bool(True)
    
    Active = Property.Bool(True)
    
    
    def Initialize(self, initializer):
        self.Space.SoundSpace.PlayCue("RainCue")
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if(not self.Active): return
        self.Owner.Sprite.AnimationSpeed = abs(self.Owner.RigidBody.Velocity.x);
        
        force = Vec3(0,0,0)
        impulse = Vec3(0,0,0)
        if Zero.Keyboard.KeyIsDown(Zero.Keys.D):
            self.Owner.Sprite.FlipX = False
            force += Vec3(1,0,0)
        if Zero.Keyboard.KeyIsDown(Zero.Keys.A):
            self.Owner.Sprite.FlipX = True
            force -= Vec3(1,0,0)
        if Zero.Keyboard.KeyIsDown(Zero.Keys.W):
            impulse += Vec3(0,1,0) 
            
        
        self.Owner.RigidBody.ApplyLinearVelocity(force * self.MoveForce)
        self.Owner.RigidBody.ApplyLinearVelocity(impulse * self.JumpStrength)
            
Zero.RegisterComponent("PlayerController", PlayerController)