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
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if(not self.Active): return
        
        force = Vec3(0,0,0)
        impulse = Vec3(0,0,0)
        if Zero.Keyboard.KeyIsDown(Zero.Keys.D):
            force += Vec3(1,0,0)
        if Zero.Keyboard.KeyIsDown(Zero.Keys.A):
            force -= Vec3(1,0,0)
        if Zero.Keyboard.KeyIsDown(Zero.Keys.W):
            impulse += Vec3(0,1,0) 
        if Zero.Keyboard.KeyIsDown(Zero.Keys.S):
            impulse += Vec3(0,-1,0)     
        
        self.Owner.RigidBody.ApplyLinearVelocity(force * self.MoveForce)
        self.Owner.RigidBody.ApplyLinearVelocity(impulse * self.JumpStrength)
            
Zero.RegisterComponent("PlayerController", PlayerController)