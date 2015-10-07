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
        #self.MouseIndicator = self.Space.FindObjectByName("MouseIndicator")
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        tracked_vec = self.Tracker.Transform.Translation
        self_x = self.Owner.Transform.Translation.x
        self_y = self.Owner.Transform.Translation.y
        self_z = self.Owner.Transform.Translation.z
        self.Owner.Transform.Translation = Vec3(tracked_vec.x * self.FollowSpeed + self_x * (1 - self.FollowSpeed), tracked_vec.y * self.FollowSpeed + self_y * (1 - self.FollowSpeed), self_z)
        
        #self.MouseIndicator.Transform.Translation += Vec3(tracked_vec.x - self_x, tracked_vec.y - self_y, 0) * 2
        
    

Zero.RegisterComponent("CameraLogic", CameraLogic)