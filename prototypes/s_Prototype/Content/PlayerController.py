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
    HorizontalSpeedLimit = Property.Float(5)

    def Initialize(self, initializer):
        self.TempTick = 5
        self.slope_tangent = Vec3(1,0,0)
        self.OnGround = True
        self.OnSlope = False
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Sprite.AnimationSpeed = abs(self.Owner.RigidBody.Velocity.x)
        self.UpdateGroundInfo()

        # Calculate horizontal movement
        force = Vec3(0,0,0)
        impulse = Vec3(0,0,0)
        if Zero.Keyboard.KeyIsDown(Zero.Keys.D):
            self.Owner.Sprite.FlipX = False
            force = self.slope_tangent
            
        elif Zero.Keyboard.KeyIsDown(Zero.Keys.A):
            self.Owner.Sprite.FlipX = True
            force = - self.slope_tangent
        
        # Modify behavior on the slope
        if self.OnSlope:
            if force.y > 0:
                force *= Vec3(1, 0.005,1)
            elif force.y < 0:
                force *= Vec3(0.5,1,1)
        #if not self.OnGround:
        #    force *= 0.2
        
        # Apply horizontal movement
        if force.x * self.Owner.RigidBody.Velocity.x < self.HorizontalSpeedLimit:
            self.Owner.RigidBody.ApplyLinearImpulse(force * self.MoveForce)
        
        # Update vertical jumping
        my_v = self.Owner.RigidBody.Velocity
        jumper = my_v.y

        if self.OnGround:
            if Zero.Keyboard.KeyIsPressed(Zero.Keys.W) and self.JumpActive:
                jumper = self.JumpStrength        
            my_v *= 0.9

        # Apply decay
        
        self.Owner.RigidBody.Velocity = Vec3(my_v.x * 0.998, jumper, 0)
        
    def UpdateGroundInfo(self):
        self.OnGround = False       
        self.slope_tangent = Vec3(1,0,0)

        for ContactHolder in self.Owner.Collider.Contacts:
            if ContactHolder.OtherObject.Collider.Ghost == False:
                normal = - ContactHolder.FirstPoint.WorldNormalTowardsOther
                if normal.y >= 0 and not self.IsSteep(normal):
                    self.OnGround = True
                    if self.IsSlope(normal):
                        self.slope_tangent = Vec3(normal.y, -normal.x, 0)
                        self.OnSlope = True
                    else:
                        self.OnSlope = False
                    return 
                        

    def IsSlope(self, normal):
        # if slope degree > 22.5
        return abs(normal.y) <= abs(normal.x) * 4
        
    def IsSteep(self, normal):
        # if slope degree > 45 + 12.5
        return abs(normal.y) * 1.5 < abs(normal.x)

Zero.RegisterComponent("PlayerController", PlayerController)