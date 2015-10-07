import Zero
import Events
import Property
import VectorMath
import math
import random

Vec3 = VectorMath.Vec3

class LightReciever:
    DefaultAlpha = 0.95
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "LightStartEvent", self.OnLightStartEvent)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Sprite.Color = Vec3(self.Owner.Sprite.Color.x, self.Owner.Sprite.Color.y, self.Owner.Sprite.Color.z, self.DefaultAlpha) 

    def OnLightStartEvent(self, LightEnterEvent):
        MinRange = LightEnterEvent.Min
        MaxRange = LightEnterEvent.Max
        Lamda = MaxRange - MinRange
        Center = LightEnterEvent.Source.Transform.WorldTranslation
        MyPos = self.Owner.Transform.WorldTranslation 
        
        VecToward = (Center - MyPos)
        VecToward.z = 0
        
        Length = VecToward.length()
        
        if Length <= MinRange :
            self.Owner.Sprite.Color = Vec3(self.Owner.Sprite.Color.x, self.Owner.Sprite.Color.y, self.Owner.Sprite.Color.z, 0)
        elif Length <= MaxRange :
            result = (Length - MinRange) / Lamda
            if result > self.DefaultAlpha : result = self.DefaultAlpha
            self.Owner.Sprite.Color = Vec3(self.Owner.Sprite.Color.x, self.Owner.Sprite.Color.y, self.Owner.Sprite.Color.z, result)



Zero.RegisterComponent("LightReciever", LightReciever)