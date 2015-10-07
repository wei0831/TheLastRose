import Zero
import Events
import Property
import VectorMath
import Action
import random

class LightSource:
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        if self.Space.FindObjectByName("Camera").LightLayer:                
            self.DefaultAlpha = self.Space.FindObjectByName("Camera").LightLayer.DefaultAlpha
            
            Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
            Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnded)
            Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStarted)
            self.sequence = Action.Sequence(self.Owner.Actions)
        
        
    def OnCollisionStarted(self, CollisionEvent):
        CollisionEvent.OtherObject.LightReceiver.AddObserver()
    def OnCollision(self, CollisionEvent):

        c = CollisionEvent.OtherObject.Sprite.Color
        dist = (self.Owner.Transform.WorldTranslation - CollisionEvent.OtherObject.Transform.WorldTranslation)
        dist = abs(dist.x) + abs(dist.y)
        
        ld = CollisionEvent.OtherObject.LightReceiver.last_dist
        should_update = dist < ld or (dist >= ld and CollisionEvent.OtherObject.LightReceiver.last_dominator == self.Owner)
        
        a = dist/5 
        if a > self.DefaultAlpha:
            a = self.DefaultAlpha
        
        if should_update:
            CollisionEvent.OtherObject.LightReceiver.last_dominator = self.Owner
            CollisionEvent.OtherObject.LightReceiver.last_dist = dist
        
            CollisionEvent.OtherObject.Sprite.Color = VectorMath.Vec4(0,0,0,a)
        elif a < 0.8:
            now_a = CollisionEvent.OtherObject.Sprite.Color.a
            modifier = now_a - (1-a)/5
            modifier = 0 if modifier < 0 else modifier
            CollisionEvent.OtherObject.Sprite.Color = VectorMath.Vec4(0,0,0,modifier)
            
        
    def OnCollisionEnded(self, CollisionEvent):
        CollisionEvent.OtherObject.LightReceiver.RemoveObserver(self.DefaultAlpha)
            
    def Destroyed(self):        
        for ch in self.Owner.Collider.Contacts:
            ch.OtherObject.LightReceiver.RemoveObserver(self.DefaultAlpha)
                   

        

Zero.RegisterComponent("LightSource", LightSource)