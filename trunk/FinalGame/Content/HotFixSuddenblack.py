import Zero
import Events
import Property
import VectorMath
import Action
class HotFixSuddenblack:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        CollisionEvent.OtherObject.RigidBody.Kinematic = True
        seq = Action.Sequence(self.Owner.Actions)
        Action.Delay(seq,1)
        
        
        def Blacker():
            self.Space.FindObjectByName("Camera").CameraFunction.SetCameraFade(VectorMath.Vec4(0,0,0,0),VectorMath.Vec4(0,0,0,1),0.15,0)
            self.Space.FindObjectByName("LevelSettings").LevelStart.HUDManager.HideBoxes()
        Action.Call(seq, Blacker)
        
        Action.Delay(seq,3)
        
        def DestroyAll():
            self.Space.LoadLevel("MenuScreen")
            self.Space.FindObjectByName("LevelSettings").LevelStart.HUDManager.Space.Destroy()
        Action.Call(seq, DestroyAll)
        
        Zero.Disconnect(self.Owner, Events.CollisionStarted, self)
Zero.RegisterComponent("HotFixSuddenblack", HotFixSuddenblack)