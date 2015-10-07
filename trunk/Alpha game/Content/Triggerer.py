import Zero
import Events
import Property
import VectorMath

class Triggerer:
    Target = Property.Cog()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.TriggerEvent = Zero.ScriptEvent()
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.CanTrigger:
            self.Trigger()
        
    def Trigger(self):
        self.Target.DispatchEvent("TriggerEvent", self.TriggerEvent)
        if self.Owner.AnimManager:
            self.Owner.Sprite.SpriteSource = self.Owner.AnimManager.AnimTable.FindResource("In")
        if self.Owner.Hierarchy:
            for child in self.Owner.Hierarchy.Children:
                if child.Triggerer:
                    child.Triggerer.Trigger()
            
        
        

Zero.RegisterComponent("Triggerer", Triggerer)