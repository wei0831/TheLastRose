import Zero
import Events
import Property
import VectorMath
import random
import Action
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4
class ThunderGenerator:
    CurrentUpdate = None
    Active = True
    Times = Property.Int(3)
    CD_Lower = Property.Float(0.05)
    CD_Upper = Property.Float(0.25)
    Alpha_Lower = Property.Float(0)
    Alpha_Upper = Property.Float(0.75)
    ActiveCD = Property.Float(3)
    ThunderCue = Property.SoundCue("ThunderCue")
    ThunderLayerDeapth = Property.Float(-5)
    
    def Initialize(self, initializer):
        self.ThunderLayer = self.Space.Create("Sprite")
        
        self.ThunderLayer.AttachToRelative(self.Owner)
        self.ThunderLayer.Transform.LocalTranslation = Vec3(0, 0, self.ThunderLayerDeapth)
        self.ThunderLayer.Sprite.Color = Vec4(1,1,1,0)
        self.ThunderLayer.Transform.WorldScale = Vec3(self.Owner.Camera.Size * 2, self.Owner.Camera.Size * 2, 1)
        
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        #if Zero.Keyboard.KeyIsPressed(Zero.Keys.Space):
        #    self.ActivateThunder()
        pass
    
    def ActivateThunder(self):
        if not self.Active: return
        
        self.Active = False
        self.NumberTimes = self.Times
        self.Thunder_1()

    def Thunder_1(self):
        self.NumberTimes -= 1
        if self.NumberTimes < 0:
            self.CurrentUpdate = None
            self.Space.SoundSpace.PlayCue(self.ThunderCue)
            sequence = Action.Sequence(self.Owner.Actions)
            Action.Delay(sequence, self.ActiveCD)
            Action.Call(sequence, self.ActiveThunder)
            return
         
        self.ThunderLayer.Sprite.Color = Vec3(self.ThunderLayer.Sprite.Color.x, self.ThunderLayer.Sprite.Color.y, self.ThunderLayer.Sprite.Color.z, self.Alpha_Upper)
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, random.uniform(self.CD_Lower, self.CD_Upper))
        Action.Call(sequence, self.Thunder_2)
        
    def Thunder_2(self):
        self.ThunderLayer.Sprite.Color = Vec3(self.ThunderLayer.Sprite.Color.x, self.ThunderLayer.Sprite.Color.y, self.ThunderLayer.Sprite.Color.z, self.Alpha_Lower)
        
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, random.uniform(self.CD_Lower, self.CD_Upper))
        Action.Call(sequence, self.Thunder_1)
     
    def ActiveThunder(self):
        self.Active = True

Zero.RegisterComponent("ThunderGenerator", ThunderGenerator)