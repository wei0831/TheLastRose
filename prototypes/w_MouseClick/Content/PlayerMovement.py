import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class PlayerMovement:
    mousePos = Vec3(0, 0, 0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)

        
    def OnLogicUpdate(self, UpdateEvent):
        if(Zero.Keyboard.KeyIsDown(Zero.Keys.D)):
            self.Owner.RigidBody.ApplyLinearVelocity(Vec3(1,0,0))
        if(Zero.Keyboard.KeyIsDown(Zero.Keys.A)):
            self.Owner.RigidBody.ApplyLinearVelocity(Vec3(-1,0,0))
        if(Zero.Keyboard.KeyIsDown(Zero.Keys.W)):
            self.Owner.RigidBody.ApplyLinearVelocity(Vec3(0,1,0))
        if(Zero.Keyboard.KeyIsDown(Zero.Keys.S)):
            self.Owner.RigidBody.ApplyLinearVelocity(Vec3(0,-1,0))


Zero.RegisterComponent("PlayerMovement", PlayerMovement)