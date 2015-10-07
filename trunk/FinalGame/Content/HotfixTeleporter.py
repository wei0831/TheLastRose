import Zero
import Events
import Property
import VectorMath
import Action

Vec4 = VectorMath.Vec4
class HotfixTeleporter:
    ActivateWhenTargetDestroy = Property.Cog()
    NextLevel = Property.Level()
    def Initialize(self, initializer):
        self.teleporting = False
        if self.ActivateWhenTargetDestroy:
            self.ActivateWhenTargetDestroy.DestroyInterface.RegisterObserver(self.Teleport)
    def Teleport(self):
        if not self.teleporting :
            if self.NextLevel.Name != "DefaultLevel":
                self.Space.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(1,1,1,0),Vec4(1,1,1,1),.03,0)
                
                ls = self.Space.FindObjectByName("LevelSettings").LevelStart
                if ls:
                    ls.HUDManager.HideBoxes()
                    hm = ls.HUDManager
                    hm.CacheSkills()
                
                sequence = Action.Sequence(self.Owner.Actions)
                
                Action.Delay(sequence, 1.5)
                Action.Call(sequence, lambda:self.Space.LoadLevel(self.NextLevel))
                self.teleporting = True

Zero.RegisterComponent("HotfixTeleporter", HotfixTeleporter)