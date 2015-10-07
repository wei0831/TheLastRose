import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class CameraLogic:
    FollowSpeed = Property.Float(0.05)
    Tracker = Property.Cog()
    MouseIndicator = Property.Cog()
    def Initialize(self, initializer):
        self.Tracker = self.Space.FindObjectByName("Player")
        self.MouseIndicator = self.Space.FindObjectByName("MouseIndicator")
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        tracked_vec = self.Tracker.Transform.Translation
        old_vec = self.Owner.Transform.Translation
        tracked_vec.z = old_vec.z
        
        self.MouseIndicator.Transform.Translation -= self.Owner.Transform.Translation
        self.Owner.Transform.Translation = tracked_vec * self.FollowSpeed + old_vec * (1-self.FollowSpeed)
        self.MouseIndicator.Transform.Translation += self.Owner.Transform.Translation
        #self.MouseIndicator.Transform.Translation.z = -0.5
        
        
        
    

Zero.RegisterComponent("CameraLogic", CameraLogic)