import Zero
import Events
import Property
import math
import VectorMath
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4
class TypeScript:
    String = Property.String("")
    Delay = Property.Float(0)
    Active = Property.Bool(True)
    Repeat = Property.Bool(False)
    CollisionActivate = Property.Bool(True)
    EmphasizeStart = Property.Int(-1)
    EmphasizeEnd = Property.Int(-1)
    DestroyDelay = Property.Float(10)
    Reactivatable = Property.Bool(True)
    EmphasizerColor = Property.Color(Vec4(1,0,0,1))
    BoxColor = Property.Color(VectorMath.Vec4(.1,.1,.1,.9))
    WordColor = Property.Color(VectorMath.Vec4(1,1,1,1))
    CreateVisual = Property.Bool(False)
    VisualCueColor = Property.Color(VectorMath.Vec4(0.9,1,0.9,0.27))
    CharsPerLine = Property.Int(0)
    ActivateWhenTargetDestroyed = Property.Cog()
    ImmediatePlayMessage = Property.Bool(True)

    
    def Initialize(self, initializer):
        self.Activatable = True if not self.ActivateWhenTargetDestroyed else False
        
        self.hider = self.Space.CreateAtPosition("WhiteDot",self.Owner.Transform.Translation)
        self.hider.AttachToRelative(self.Owner)
        
        if self.EmphasizeStart >= 0 and self.EmphasizeEnd >= self.EmphasizeStart:
            self.emphasizer = self.Space.CreateAtPosition("WhiteDot",self.Owner.Transform.Translation)
        else:
            self.emphasizer = None
        
        self.visual_soul = None    
        if self.CreateVisual:
            self.visual_soul = self.Space.CreateAtPosition("VisualSoul", self.Owner.Transform.Translation + self.Owner.Collider.Offset)
            self.visual_soul.SpriteParticleSystem.Tint = self.VisualCueColor
            self.init_emit_rate = self.visual_soul.SphericalParticleEmitter.EmitRate
            
        self.Reset()

        self.destroy_registered = False            
        self.CurrentUpdate = self.TextBoxUpdate
        
        self.playSuccessful = False
        
        self.soul_size_changed = False
        
        if self.CollisionActivate:
            self.Active = False
            Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
            Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnded)
        
        if self.CharsPerLine:
            fontheight = self.TestFontSize().y
            fontwidth = self.TestFontSize().x
            
            boxheight = math.ceil(len(self.String) / self.CharsPerLine) * fontheight
            boxwidth = self.CharsPerLine * fontwidth
            self.Owner.SpriteText.Size = VectorMath.Vec2(boxwidth, boxheight)
        
        if self.ActivateWhenTargetDestroyed:
            self.Active = False
                
            if self.visual_soul:
                self.visual_soul.SphericalParticleEmitter.EmitRate = 0
            
            def activate():
                if self.visual_soul:
                    self.visual_soul.SphericalParticleEmitter.EmitRate = self.init_emit_rate
                self.Activatable=True
                if self.ImmediatePlayMessage:
                    self.Play()
                
            if self.ActivateWhenTargetDestroyed.KeyHoleDoor:
                self.ActivateWhenTargetDestroyed.KeyHoleDoor.RegisterObserver(activate)
            elif self.ActivateWhenTargetDestroyed.DestroyInterface:
                print("Registered")
                self.ActivateWhenTargetDestroyed.DestroyInterface.RegisterObserver(activate)
            elif self.ActivateWhenTargetDestroyed.ClickReceiver:
                self.ActivateWhenTargetDestroyed.ClickReceiver.RegisterObserver(activate)
                
        self.touched = False
        
        Zero.Connect(self.Space,Events.LogicUpdate, self.OnLogicUpdate)
    def ResizeVisualCue(self):
        if self.visual_soul and not self.soul_size_changed:
            self.soul_size_changed = True
            if not self.Reactivatable:
                self.visual_soul.SphericalParticleEmitter.Active = False
            else:
                self.visual_soul.SphericalParticleEmitter.EmitRate *= 0.5
                self.visual_soul.SphericalParticleEmitter.Size *= .5
                self.visual_soul.SphericalParticleEmitter.EmitterSize *= .5
    def OnCollision(self, CollisionEvent):
        
        if self.Activatable:
            self.touched = True
            if self.CurrentUpdate == self.TextBoxUpdate:
                self.Active = True
                if self.CreateVisual:
                    self.ResizeVisualCue()
                    
            if self.Reactivatable:
                if self.CurrentUpdate == self.WaitForDestroy:
                    self.CurrentUpdate = self.TextBoxUpdate
                    self.ResetColor()
                    self.destroy_registered = False
                elif self.CurrentUpdate == self.DestroyUpdate:
                    self.Reset()
                    self.Active = True
                    self.destroy_registered = False
                    self.CurrentUpdate = self.TextBoxUpdate
            
        
    def OnCollisionEnded(self, CollisionEvent):
        if self.Activatable:
            self.destroy_registered = True
    
    def Play(self):
        self.Active = True
        self.CurrentUpdate = self.TextBoxUpdate
    
    def Stop(self):
        self.Active = False
    
    def RetestSize(self):
        self.tested_size = None
        return self.TestFontSize()
    
    def TestFontSize(self):
        if not self.tested_size:
            now_text = self.Owner.SpriteText.Text
            now_size = self.Owner.SpriteText.Size
            
            self.Owner.SpriteText.Size *= 0
            self.Owner.SpriteText.Text = "A"
            size = self.Owner.SpriteText.MeasureText()
            
            self.Owner.SpriteText.Text = now_text
            self.Owner.SpriteText.Size = now_size
            self.tested_size = size
            
        
        return self.tested_size
        
    
    def ShowWord(self,i):
        length = len(self.String)
        i = length if i > length else i
        self.Owner.SpriteText.Text = self.String[:i]
        
    def TextBoxUpdate(self, UpdateEvent):
        s = self.hider.Sprite.Size
        if self.Active:
            self.hider.Sprite.Visible = True
            self.accum_dt += UpdateEvent.Dt
            if self.accum_dt > self.Delay:
                self.accum_dt = 0
                self.ShowWord(self.wordhead)
                if self.wordhead == len(self.String):
                    if self.Repeat:
                        self.wordhead = 1
                    else:
                        self.Active = False
                        self.playSuccessful = True
        
                self.wordhead += 1
        
            if self.emphasizer:
                lastwordidx = self.wordhead - 2
                if lastwordidx == self.EmphasizeStart:
                    self.emphasizer.Sprite.Visible = True
                if lastwordidx <= self.EmphasizeEnd+2 and lastwordidx > self.EmphasizeStart:
                    pos = self.Owner.SpriteText.GetCharacterPosition(self.EmphasizeStart-1)
                    self.emphasizer.Transform.Translation = Vec3(pos.x, pos.y - self.TestFontSize().y + 0.01, -0.005)
                
                    x1 = self.Owner.SpriteText.GetCharacterPosition(self.EmphasizeStart).x
                    x2 = self.Owner.SpriteText.GetCharacterPosition(lastwordidx).x
                    self.emphasizer.Transform.Scale = Vec3((x2-x1)/s.x, .75, 1)
            
        # Update hider size            

        ss = self.Owner.SpriteText.MeasureText()
        self.hider.Transform.Scale = Vec3(ss.x / s.x + 2.6, ss.y / s.y + 1,1)
            

        if self.destroy_registered and not self.Active:
            self.CurrentUpdate = self.WaitForDestroy
        
    def WaitForDestroy(self, UpdateEvent):
        self.accum_dt += UpdateEvent.Dt
        if self.accum_dt >= self.DestroyDelay:
            self.PerformDestroy()
        
    
    def OnLogicUpdate(self, UpdateEvent):
        if self.Activatable:
            self.CurrentUpdate(UpdateEvent)
        
        
        if self.playSuccessful:
            self.destroy_registered = True
            if self.touched and self.Activatable:
                for ch in self.Owner.Collider.Contacts:
                    if ch.OtherObject.PlayerController:        
                        self.destroy_registered = False
                        self.playSuccessful = False
            if self.touched and self.destroy_registered:
                self.ResizeVisualCue()
            
                
    
    def PerformDestroy(self):
        self.CurrentUpdate = self.DestroyUpdate
    
    def DestroyUpdate(self, UpdateEvent):
        self.Owner.SpriteText.Color *= VectorMath.Vec4(1,1,1,0.95)
        self.hider.Sprite.Color *= VectorMath.Vec4(1,1,1,0.95)
        if self.emphasizer:
            self.emphasizer.Sprite.Color *= VectorMath.Vec4(1,1,1,0.95)
    
    def ResetColor(self):
        if self.emphasizer:
            self.emphasizer.Sprite.Color = self.EmphasizerColor
        self.hider.Sprite.Color = self.BoxColor
        self.Owner.SpriteText.Color = self.WordColor
        
        
    def ResetScale(self):
        if self.emphasizer:
            self.emphasizer.Transform.Scale = Vec3(0,0,1)
        self.hider.Transform.Scale = Vec3(0,0,1)
        
    def ResetVisibility(self):
        if self.emphasizer:
            self.emphasizer.Sprite.Visible = False
        self.hider.Sprite.Visible = False
    
    
    def Rewind(self):
        self.wordhead = 1
        self.accum_dt = 0
        self.Owner.SpriteText.Text = ""
    
    def ResetColor(self):
        self.hider.Sprite.Color = self.BoxColor
        self.Owner.SpriteText.Color = self.WordColor
        if self.emphasizer:
            self.emphasizer.Sprite.Color = self.EmphasizerColor
        
    
    def ResetTranslation(self):
        self.hider.Transform.Translation = self.hider.Transform.Translation = Vec3(-0.1,0,-0.1)
        if self.emphasizer:
            self.emphasizer.Transform.Translation = self.hider.Transform.Translation = Vec3(-0.1,0,-0.05)
    
    def Reset(self):
        self.RetestSize()
        self.Rewind()
        self.ResetTranslation()
        self.ResetColor()
        self.ResetVisibility()
        self.ResetScale()
        self.ResetColor()
        
        
        
Zero.RegisterComponent("TypeScript", TypeScript)