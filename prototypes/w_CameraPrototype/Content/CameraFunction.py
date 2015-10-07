import Zero
import Events
import Property
import VectorMath
import Action
import math
import random

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class CameraFunction:
    # Shaking Variables
    ShakeEnable = False
    ShakeInX = False
    ShakeRadiusX = 0
    ShakeInY = False
    ShakeRadiusY = 0
    ShakeDelay = 0
    ShakeTimer = 0
    ShakeCenter = Vec3(0, 0, 0)
    
    # Fading Variables
    FadeEnable = False
    FadeColorStart = Vec4(0, 0, 0, 0)
    FadeColorEnd = Vec4(0, 0, 0, 0)
    FadeDelay = 0
    FadeTimer = 0
    FadeRDelta = 0
    FadeGDelta = 0
    FadeBDelta = 0
    FadeADelta = 0
    FadeEndFlag = False
    
    # Follow Variables
    FollowEnable = False
    FollowTarget = None
    
    # Chase Variables
    ChaseEnable = False
    ChaseTarget = None
    ChaseSpeed = 0
    
    # Shift Variables
    ShiftEnable = False
    ShiftStartPos = Vec3(0, 0, 0)
    ShiftTargetPos = Vec3(0, 0, 0)
    ShiftSpeed = 0
    ShiftTimer = 0
    ShiftDelay = 0
    ShiftTravelBack = False
    ShiftAction = None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.FadeLayer = self.Owner.FindChildByName("AlphaLayer")

        
    def OnLogicUpdate(self, UpdateEvent):
        if self.ShiftEnable: 
            self.ShiftUpdate(UpdateEvent)
        else:
            if self.FollowEnable: self.FollowUpdate(UpdateEvent)
            if self.ChaseEnable: self.ChaseUpdate(UpdateEvent)
        if self.ShakeEnable: self.ShakeUpdate(UpdateEvent)
        if self.FadeEnable: self.FadeUpdate(UpdateEvent)
    
    def FollowUpdate(self, UpdateEvent):
        if not self.FollowTarget == None:
            self.Owner.Transform.Translation = Vec3(self.FollowTarget.Transform.Translation.x, self.FollowTarget.Transform.Translation.y, self.Owner.Transform.Translation.z)
            if self.ShakeEnable:
                self.ShakeCenter = self.Owner.Transform.Translation
            
    def SetFollowTarget(self, target):
        self.ChaseEnable = False
        self.FollowEnable = True
        self.FollowTarget = target
        
    def TurnOffCameraFollow(self):
        self.FollowEnable = False
        self.FollowTarget = None
        
    def ChaseUpdate(self, UpdateEvent):
        if self.ChaseTarget == None: return
        
        towardVec = self.ChaseTarget.Transform.Translation - self.Owner.Transform.Translation
        towardVec.z = 0
        
        if(math.fabs(towardVec.length()) > 0.5):
            self.Owner.Transform.Translation += towardVec * self.ChaseSpeed
        else:
            self.Owner.Transform.Translation = Vec3(self.ChaseTarget.Transform.Translation.x, self.ChaseTarget.Transform.Translation.y, self.Owner.Transform.Translation.z)
        
        if self.ShakeEnable:
            self.ShakeCenter = self.Owner.Transform.Translation
            
    def SetChaseTarget(self, target, speed):
        self.FollowEnable = False
        self.ChaseEnable = True
        self.ChaseTarget = target
        self.ChaseSpeed = speed
        
    def TurnOffCameraChase(self):
        self.ChaseEnable = False
        self.ChaseTarget = None
    
    def ShiftUpdate(self, UpdateEvent):
        if not self.ShiftAction == None:
            self.ShiftAction(UpdateEvent)

    def ShitfStage1(self, UpdateEvent):
        towardVec = self.ShiftTargetPos - self.Owner.Transform.Translation
        towardVec.z = 0
        
        if(math.fabs(towardVec.length()) > 0.5):
            self.Owner.Transform.Translation += towardVec * self.ShiftSpeed
        else:
            self.ShiftAction = self.ShitfStage2
   
    def ShitfStage2(self, UpdateEvent):
        self.ShiftTimer += UpdateEvent.Dt
        if self.ShiftTimer > self.ShiftDelay:
            self.ShiftAction = self.ShitfStage3
            
    def ShitfStage3(self, UpdateEvent):
        if self.ShiftTravelBack :
            towardVec = self.ShiftStartPos - self.Owner.Transform.Translation
            towardVec.z = 0

            if(math.fabs(towardVec.length()) > 0.5):
                self.Owner.Transform.Translation += towardVec * self.ShiftSpeed
            else:
                self.TurnOffCameraShift()
        else:
            self.Owner.Transform.Translation = Vec3(self.ShiftStartPos.x, self.ShiftStartPos.y, self.Owner.Transform.Translation.z)
            self.TurnOffCameraShift()
                      
    def SetShiftTarget(self, targetPos, speed, cd, travelback):
        if self.ShiftEnable: return
        self.ShiftEnable = True
        self.ShiftStartPos = Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y, 0)
        self.ShiftTargetPos = targetPos
        self.ShiftSpeed = speed
        self.ShiftDelay = cd
        self.ShiftTimer = 0
        self.ShiftTravelBack = travelback
        self.ShiftAction = self.ShitfStage1
    
    def TurnOffCameraShift(self):
        self.ShiftAction = None
        self.ShiftTimer = 0
        self.ShiftEnable = False
    
    def ShakeUpdate(self, UpdateEvent):
        if(self.ShakeDelay > 0):
            self.ShakeTimer += UpdateEvent.Dt
            if(self.ShakeTimer < self.ShakeDelay):
                return
            else:
                self.ShakeTimer = 0
        
        result = Vec3(0, 0, 0)
        
        if self.ShakeInX :
            result += Vec3(random.uniform(-self.ShakeRadiusX, self.ShakeRadiusX), 0, 0)
        if self.ShakeInY :
            result += Vec3(0, random.uniform(-self.ShakeRadiusY, self.ShakeRadiusY), 0)

        self.Owner.Transform.Translation = self.ShakeCenter + result    
        
    def SetCameraShake(self, x_Enable, x_Radius, y_Enable, y_Radius, time, cd):
        if self.ShakeEnable: return
        
        self.ShakeEnable = True
        self.ShakeCenter = self.Owner.Transform.Translation
        self.ShakeInX = x_Enable
        self.ShakeInY = y_Enable
        self.ShakeRadiusX = x_Radius
        self.ShakeRadiusY = y_Radius
        self.ShakeDelay = cd
        self.ShakeTimer = 0
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, time)
        Action.Call(sequence, self.TurnOffCameraShake)
    
    def SetCameraShakeCenter(self, center):
        self.ShakeCenter = center
    
    def TurnOffCameraShake(self):
        self.ShakeEnable = False
        self.ShakeInY = False
        self.ShakeInX = False
        self.ShakeTimer = 0
        self.ShakeDelay = 0
        self.Owner.Transform.Translation = self.ShakeCenter
    
    def FadeUpdate(self, UpdateEvent):
        if(self.FadeDelay > 0):
            self.FadeTimer += UpdateEvent.Dt
            if(self.FadeTimer < self.FadeDelay):
                return
            else:
                self.FadeTimer = 0    
        
        result = self.FadeLayer.Sprite.Color + Vec4(self.FadeRDelta, self.FadeGDelta, self.FadeBDelta, self.FadeADelta)
        
        self.FadeEndFlag = self.clampCheck(0.0, result.x, 1.0)
        if self.FadeEndFlag: self.clamp(0.0, result.x, 1.0)   
        self.FadeEndFlag = self.clampCheck(0.0, result.y, 1.0)
        if self.FadeEndFlag: self.clamp(0.0, result.y, 1.0)
        self.FadeEndFlag = self.clampCheck(0.0, result.z, 1.0)
        if self.FadeEndFlag: self.clamp(0.0, result.z, 1.0)
        self.FadeEndFlag = self.clampCheck(0.0, result.a, 1.0)
        if self.FadeEndFlag: self.clamp(0.0, result.a, 1.0)
        
        if self.FadeEndFlag:
            self.FadeLayer.Sprite.Color = self.FadeColorEnd
            self.TurnOffCameraFade()
        else:
            self.FadeLayer.Sprite.Color = result
        
    def SetCameraFade(self, startColor, endColor, deltaRate, cd):
        if self.FadeEnable: return
        
        self.FadeColorStart = startColor
        self.FadeColorEnd = endColor
        delta = endColor - startColor
        self.FadeRDelta = delta.x * deltaRate
        self.FadeGDelta = delta.y * deltaRate
        self.FadeBDelta = delta.z * deltaRate
        self.FadeADelta = delta.a * deltaRate
        self.FadeLayer.Sprite.Color = startColor
        self.FadeDelay = cd
        self.FadeEnable = True

    def TurnOffCameraFade(self):
        self.FadeEnable = False
        self.FadeColorStart = Vec4(0, 0, 0, 0)
        self.FadeColorEnd = Vec4(0, 0, 0, 0)
        self.FadeDelay = 0
        self.FadeTimer = 0
        self.FadeRDelta = 0
        self.FadeGDelta = 0
        self.FadeBDelta = 0
        self.FadeADelta = 0
        self.FadeEndFlag = False
    
    # Helper
    def clampCheck(self, minimum, x, maximum):
        return x > maximum or x < minimum
        
    def clamp(self, minimum, x, maximum):
        return max(minimum, min(x, maximum))
        
Zero.RegisterComponent("CameraFunction", CameraFunction)