import Zero
import Events
import Property
import VectorMath
import math

Vec3 = VectorMath.Vec3

class CameraMovement:
    CameraFollowSpeed = Property.Float(0.1)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.player = self.Space.FindObjectByName("Hero")
        
    def OnLogicUpdate(self, OnLogicUpdate):       
        towardVec = self.player.Transform.LocalTranslation - self.Owner.Transform.LocalTranslation 
        towardVec.z = 0
        if(math.fabs(towardVec.length()) > 0.01): 
            self.Owner.Transform.Translation += towardVec * self.CameraFollowSpeed

Zero.RegisterComponent("CameraMovement", CameraMovement)