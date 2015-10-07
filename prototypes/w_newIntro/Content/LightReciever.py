import Zero
import Events
import Property
import VectorMath
import math
import random
import Action
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class LightReciever:
    DefaultAlpha = 0
    CurrentAlpha = 1
    PreviousAlpha = 1
    
    def Initialize(self, initializer):
        self.sequence = Action.Sequence(self.Owner.Actions)

        Zero.Connect(self.Owner, "LightStartEvent", self.OnLightStartEvent)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Sprite.Color = Vec4(self.Owner.Sprite.Color.x, self.Owner.Sprite.Color.y, self.Owner.Sprite.Color.z, self.DefaultAlpha)
        self.CurrentAlpha = self.DefaultAlpha
        pass
        
    def OnLightStartEvent(self, LightEnterEvent):
        MinRange = LightEnterEvent.Min
        MaxRange = LightEnterEvent.Max
        Lamda = MaxRange - MinRange
        Center = LightEnterEvent.Source.Transform.WorldTranslation
        MyPos = self.Owner.Transform.WorldTranslation 
        
        VecToward = (Center - MyPos)
        VecToward.z = 0
        
        Length = VecToward.length()
        
        result = 1
        if Length <= MinRange :
            result = 0
            pass
        elif Length <= MaxRange :
            result = (Length - MinRange) / Lamda
        else:
            return

        if result > self.DefaultAlpha : result = self.DefaultAlpha    
        
        self.PreviousAlpha = self.CurrentAlpha
        self.CurrentAlpha = result
        if self.PreviousAlpha < self.CurrentAlpha:
            self.CurrentAlpha = self.PreviousAlpha
            
        self.Owner.Sprite.Color = Vec3(self.Owner.Sprite.Color.x, self.Owner.Sprite.Color.y, self.Owner.Sprite.Color.z, self.CurrentAlpha)    



Zero.RegisterComponent("LightReciever", LightReciever)