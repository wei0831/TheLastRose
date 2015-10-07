import Zero
import Events
import Property
import VectorMath
import random
import Action
Vec3 = VectorMath.Vec3

class ThunderTest:
    CurrentUpdate = None
    Active = True
    Times = 3
    CD_Lower = 0.05
    CD_Upper = 0.25
    Alpha_Lower = 0
    Alpha_Upper = 0.75
    ActiveCD = Property.Float(3)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        pass
        #if Zero.Keyboard.KeyIsPressed(Zero.Keys.Space):
        #    self.ActivateThunder()
    
    def ActivateThunder(self):
        if not self.Active: return
        
        self.Active = False
        self.NumberTimes = self.Times
        self.Thunder_1()

    def Thunder_1(self):
        self.NumberTimes -= 1
        if self.NumberTimes < 0:
            self.CurrentUpdate = None
            self.Space.SoundSpace.PlayCue("Thunder")
            sequence = Action.Sequence(self.Owner.Actions)
            Action.Delay(sequence, self.ActiveCD)
            Action.Call(sequence, self.ActiveThunder)
            return
         
        self.Owner.Sprite.Color = Vec3(self.Owner.Sprite.Color.x, self.Owner.Sprite.Color.y, self.Owner.Sprite.Color.z, self.Alpha_Upper)
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, random.uniform(self.CD_Lower, self.CD_Upper))
        Action.Call(sequence, self.Thunder_2)
        
    def Thunder_2(self):
        self.Owner.Sprite.Color = Vec3(self.Owner.Sprite.Color.x, self.Owner.Sprite.Color.y, self.Owner.Sprite.Color.z, self.Alpha_Lower)
        
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, random.uniform(self.CD_Lower, self.CD_Upper))
        Action.Call(sequence, self.Thunder_1)
     
    def ActiveThunder(self):
        self.Active = True
        
Zero.RegisterComponent("ThunderTest", ThunderTest)