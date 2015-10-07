import Zero
import Events
import Property
import VectorMath

class MonsterMovement:
    MoveSpeed = 0.25
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def OnLogicUpdate(self, UpdateEvent):
        if Zero.Keyboard.KeyIsDown(Zero.Keys.Up):
            self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(0, self.MoveSpeed, 0))
        if Zero.Keyboard.KeyIsDown(Zero.Keys.Down):
            self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(0, -self.MoveSpeed, 0))
        if Zero.Keyboard.KeyIsDown(Zero.Keys.Left):
            self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(-self.MoveSpeed, 0, 0))
        if Zero.Keyboard.KeyIsDown(Zero.Keys.Right):
            self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(self.MoveSpeed, 0, 0))

Zero.RegisterComponent("MonsterMovement", MonsterMovement)