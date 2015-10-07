import Zero
import Events
import Property
import VectorMath
import Action

class Triggerer:
    Target = Property.Cog()
    TriggerDuration = Property.Float(0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.TriggerEvent = Zero.ScriptEvent()
        self.triggerable = True
        
        
    def OnCollision(self, CollisionEvent):
        if self.triggerable:
            if CollisionEvent.OtherObject.CanTrigger and CollisionEvent.OtherObject.CanTrigger.Active:
                self.triggerable = False
                self.Trigger()
                
                if self.TriggerDuration:
                    self.Owner.SoundEmitter.PlayCue("TickCue")
                    
                    
                        
                    
                    seq = Action.Sequence(self.Owner.Actions)
                    
                    def Untrigger():
                        self.Trigger(False)
                        self.Owner.SoundEmitter.Stop()
                        self.Owner.SoundEmitter.PlayCue("DingCue")
                        
                        def TurnTriggerable():
                            self.triggerable = True
                        Action.Delay(seq, .5)
                        Action.Call(seq, TurnTriggerable)
                        
                                            
                    Action.Delay(seq,self.TriggerDuration)
                    Action.Call(seq, Untrigger)

        
    def Trigger(self, trigger=True):
    
        self.TriggerEvent.Trigger = trigger
        self.Target.DispatchEvent("TriggerEvent", self.TriggerEvent)
        
        if self.Owner.AnimManager:
            anim = "In" if trigger else "Out"
            self.Owner.Sprite.SpriteSource = self.Owner.AnimManager.AnimTable.FindResource(anim)
        if self.Owner.Hierarchy:
            for child in self.Owner.Hierarchy.Children:
                if child.Triggerer:
                    child.Triggerer.Trigger(trigger)
        

Zero.RegisterComponent("Triggerer", Triggerer)