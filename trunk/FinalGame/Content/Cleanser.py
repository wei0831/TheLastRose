import Zero
import Events
import Property
import VectorMath
Vec4 = VectorMath.Vec4
import Action

class Cleanser:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)

    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.AbilityStatus:
            CollisionEvent.OtherObject.AbilityStatus.SwapPhysSkill("")
            CollisionEvent.OtherObject.AbilityStatus.SwapTreeSkill("")
            camera = self.Space.FindObjectByName("Camera")
                
            seq = Action.Sequence(self.Owner.Actions)
            camera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 0), Vec4(1, 0, 0, .9), .2, 0)
            Action.Delay(seq, .3)
            Action.Call(seq, lambda: camera.CameraFunction.SetCameraFade(Vec4(1, 0, 0, .9), Vec4(0, 0, 0, 0), .03, 0))
            
            
Zero.RegisterComponent("Cleanser", Cleanser)