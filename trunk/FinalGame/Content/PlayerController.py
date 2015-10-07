import Zero
import Events
import Property
import VectorMath
import math
import Action
Vec3 = VectorMath.Vec3

class PlayerController:
    JumpStrength = Property.Float(2.0)
    MoveForce = Property.Float(3.0)
    JumpActive = Property.Bool(True)
    HorizontalSpeedLimit = Property.Float(5)
    VerticalSpeedLimit = Property.Float(20)
    Mouse = Property.Cog()
    FallKillLimit = Property.Float(-60)
    DontUpdateAnim = Property.Bool(False)
    
    AnimTable = Property.ResourceTable("PlayerAnimTable")

    def Initialize(self, initializer):
        self.TempTick = 10
        self.slope_tangent = Vec3(1,0,0)
        self.OnGround = True
        self.OnSlope = False
        self.OnGroundUpdateEnabled = True
        self.CanJump = True
        self.IsBounced = False
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.Mouse = self.Space.FindObjectByName("MouseIndicator")
        
        self.animstate = "Stand"
        
        self.HorizontalLocked = False
    def TriggerBounced(self):
        self.IsBounced = True
        self.CanJump = False
        
    def IsOnGround(self):
        return self.OnGround
        
    def PlayPainAnim(self):
        self.Owner.Sprite.SpriteSource = self.AnimTable.FindValue("Pain")
        
    def OnLogicUpdate(self, UpdateEvent):
        #self.Owner.Sprite.AnimationSpeed = abs(self.Owner.RigidBody.Velocity.x)
        self.UpdateGroundInfo()
        if self.Owner.CanHook and self.Owner.CanHook.IsHooked():
            self.CanJump = False
        if not self.OnGroundUpdateEnabled or not self.OnGround:
            self.TempTick -= 1
            if not self.IsBounced and self.TempTick < 10 and self.CanJump:
                self.Owner.RigidBody.Velocity *= Vec3(0.75,1,1)
            if self.TempTick == 0:
                self.TempTick = 10
                self.OnGroundUpdateEnabled = True
                if self.CanJump:
                    self.CanJump = False
                    if not self.IsBounced:
                        self.Owner.RigidBody.Velocity *= Vec3(0.65,1,1)
                    else:
                        self.IsBounced=False
        else:
            self.TempTick = 10
            
        if self.Owner.Transform.Translation.y < self.FallKillLimit:
            self.Owner.HealthStatus.AddHealth(-10000)
                
        
        #UpdateAnimation
        self.UpdateAnimation()
        
        
        # Calculate horizontal movement
        force = Vec3(0,0,0)
        impulse = Vec3(0,0,0)
        if Zero.Keyboard.KeyIsDown(Zero.Keys.D):
            if not self.DontUpdateAnim and not self.Mouse or not self.Mouse.MouseLocationIndicator.AbsorbActive:
                self.Owner.Sprite.FlipX = False
            if (not self.HorizontalLocked) or self.Owner.RigidBody.Velocity.x >= 0:
                force = self.slope_tangent

        elif Zero.Keyboard.KeyIsDown(Zero.Keys.A):
            #if not self.Owner.CanHook.IsHooked():
            if not self.DontUpdateAnim and not self.Mouse or not self.Mouse.MouseLocationIndicator.AbsorbActive:
                self.Owner.Sprite.FlipX = True
            
            if (not self.HorizontalLocked) or self.Owner.RigidBody.Velocity.x <= 0:
                force = - self.slope_tangent
        
        


        if self.Owner.AlternateSoundEmitter:
            if self.OnGround and (Zero.Keyboard.KeyIsDown(Zero.Keys.D) or Zero.Keyboard.KeyIsDown(Zero.Keys.A)) and abs(self.Owner.RigidBody.Velocity.x)>0.5:
                self.Owner.AlternateSoundEmitter.Active = True
            else:
                self.Owner.AlternateSoundEmitter.Active = False
            
        # Modify behavior on the slope
        if self.OnSlope:
            if force.y > 0:
                force *= Vec3(1, 0.005,1)
            elif force.y < 0:
                force *= Vec3(0.5,1,1)
                
        
        # Apply horizontal movement
        hinderer = .75 if self.OnGround else 0.5
        if force.x * self.Owner.RigidBody.Velocity.x < self.HorizontalSpeedLimit * hinderer:
            self.Owner.RigidBody.ApplyLinearImpulse(force * hinderer * self.MoveForce)
        
        # Update vertical jumping
        my_v = self.Owner.RigidBody.Velocity
        jumper = my_v.y
        
        if self.CanJump:
            if (Zero.Keyboard.KeyIsPressed(Zero.Keys.W) or Zero.Keyboard.KeyIsPressed(Zero.Keys.Space)) and self.JumpActive:
                jumper = self.JumpStrength        
                my_v *= Vec3(0.8,1,1)
                self.CanJump = False
                self.OnGroundUpdateEnabled = False
                
                if not self.Owner.DoorEnterer.IsAtDoor():
                    self.EnsureSoundEmitter()
                    self.Owner.SoundEmitter.PlayCue("JumpCue")
                    self.Owner.SoundEmitter.Volume *= 0.9
                
                    def RecoverSound():
                        self.Owner.SoundEmitter.Volume /= 0.9
                        
                    seq = Action.Sequence(self.Owner.Actions)
                    Action.Delay(seq, 6)
                    Action.Call(seq, RecoverSound)
                
        if self.OnGround:
            my_v *= 0.9

        # Apply Jumping
        self.Owner.RigidBody.Velocity = Vec3(my_v.x * 0.998, jumper, 0)
        
        
        # Regulate speed
        v = self.Owner.RigidBody.Velocity
        new_vx = v.x
        new_vy = v.y
        if abs(self.Owner.RigidBody.Velocity.y) > self.VerticalSpeedLimit:
            sign = 1 if self.Owner.RigidBody.Velocity.y > 0 else -1
            new_vy = self.VerticalSpeedLimit * sign
        self.Owner.RigidBody.Velocity = Vec3(new_vx, new_vy,0)
    def EnsureSoundEmitter(self):
        if not self.Owner.SoundEmitter:
            self.Owner.AddComponentByName("SoundEmitter")
        def Null():
            pass
            
        self.EnsureSoundEmitter = Null
    def UpdateAnimation(self):
        if not self.DontUpdateAnim:
            if self.Owner.CanHook and self.Owner.CanHook.IsHooked():
                animstate = "Grab"
            else:
                if self.Mouse and self.Mouse.MouseLocationIndicator.AbsorbActive:
                    
                    if (self.Owner.RigidBody.Velocity.x > 0.5 and self.Owner.Sprite.FlipX) or (self.Owner.RigidBody.Velocity.x < -0.5 and not self.Owner.Sprite.FlipX):
                        animstate = "AttackLeft"
                    else:
                        animstate = "Attack"
                    
                else: 
                    if not self.OnGround:
                        if self.Owner.RigidBody.Velocity.y < 0:
                            animstate = "Fall"
                        else:
                            animstate = "Jump"
                    else:
                        if abs(self.Owner.RigidBody.Velocity.x) > 2:
                            animstate = "Walk"
                        else:
                            animstate = "Stand"
            if self.animstate != animstate:
                self.animstate = animstate
                self.Owner.Sprite.SpriteSource = self.AnimTable.FindValue(self.animstate)
            
            
            if self.Mouse and self.Mouse.MouseLocationIndicator.AbsorbActive:
                self.Owner.Sprite.FlipX =  self.Mouse.Transform.WorldTranslation.x - self.Owner.Transform.WorldTranslation.x < 0
                    
        
    def UpdateGroundInfo(self):
        prefalse = not self.OnGround
            
        self.OnGround = False       
        self.slope_tangent = Vec3(1,0,0)

        if self.OnGroundUpdateEnabled:
            for ContactHolder in self.Owner.Collider.Contacts:
                if ContactHolder.OtherObject.Collider.Ghost == False:
                    normal = - ContactHolder.FirstPoint.WorldNormalTowardsOther
                    if normal.y >= 0 and not self.IsSteep(normal):
                        self.OnGround = True
                        self.CanJump = True
                        if prefalse and self.Owner.AlternateSoundEmitter:
                            self.Owner.AlternateSoundEmitter.PlayOne()
                            
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
    
    def LockHorizontal(self):
        self.HorizontalLocked = True
    def UnlockHorizontal(self):
        self.HorizontalLocked = False
Zero.RegisterComponent("PlayerController", PlayerController)