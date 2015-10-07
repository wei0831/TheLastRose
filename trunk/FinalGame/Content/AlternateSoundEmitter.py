import Zero
import Events
import Property
import VectorMath
import Action
class AlternateSoundEmitter:
    SoundCue1 = Property.SoundCue("WalkCue")
    SoundCue2 = Property.SoundCue("WalkCue2")
    Active = Property.Bool(False)
    Duration = Property.Float(0.25)
    DynamicAdjustment = Property.Bool(True)
    
    def Initialize(self, initializer):
        self.seq = Action.Sequence(self.Owner.Actions)
        self.nextplay = self.SoundCue1
        self.nowplay = self.SoundCue2
        self.nextplay.Volume = 1
        self.nowplay.Volume = 1
        self.Play()
        
    def EnsureSoundEmitter(self):
        if not self.Owner.SoundEmitter:
            self.Owner.AddComponentByName("SoundEmitter")
        self.Owner.SoundEmitter.Positional = False
        
        def Null():
            pass
        self.EnsureSoundEmitter = Null
        
    def Play(self):
        self.EnsureSoundEmitter()
        if self.Active:
            self.Owner.SoundEmitter.PlayCue(self.nowplay)
            self.nowplay, self.nextplay = self.nextplay, self.nowplay
        
            if self.nowplay.Volume > 0.5:
                self.nowplay.Volume *= 0.9
            self.nextplay.Volume = self.nowplay.Volume
        else:
            self.nowplay.Volume *= 1.03 if self.nowplay.Volume <= 1 else 1
            self.nextplay.Volume = self.nowplay.Volume
        
        Action.Delay(self.seq, self.Duration)
        Action.Call(self.seq, self.Play)
            
    def PlayOne(self):
        self.Owner.SoundEmitter.PlayCue(self.nowplay)
        self.nowplay, self.nextplay = self.nextplay, self.nowplay
    
        

Zero.RegisterComponent("AlternateSoundEmitter", AlternateSoundEmitter)