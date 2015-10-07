import Zero
import Events
import Property
import VectorMath
import random
import Action
class TriggerDoor:
    def Initialize(self, initializer):
        
        Zero.Connect(self.Owner, "TriggerEvent", self.OnTrigger)
        
        
    def OnTrigger(self, TriggerEvent):     
        should_trigger = TriggerEvent.Trigger
        
        target_list = [self.Owner]
        if self.Owner.Hierarchy:
            target_list += list(self.Owner.Hierarchy.Children)

        seq = Action.Sequence(self.Owner.Actions)


        def ReUntrigger(target):
            
            for ch in target.Collider.Contacts:
                if ch.OtherObject.PlayerController:
                    target.Collider.Ghost = True
                    Action.Delay(seq,0.05)
                    Action.Call(seq, ReUntrigger, target)
                    return
            target.Collider.Ghost = False
                            

        def startfade(target):
            target.FadeAnim.Active = True
            target.FadeAnim.FadeDirection = -3 if should_trigger else +3
            if target.Collider:
                if should_trigger:
                    target.Collider.Ghost = True
                else:
                    target.Collider.Ghost = False
                    for ch in target.Collider.Contacts:
                        if ch.OtherObject.PlayerController:
                            ReUntrigger(target)
                
            if should_trigger and target.IsSentry:
                target.RemoveComponentByName("IsSentry")
            elif not should_trigger and not target.IsSentry:
                target.AddComponentByName("IsSentry")
        
        
        for target in target_list:
            if target.FadeAnim:
                Action.Delay(seq, random.random()/5)
                Action.Call(seq, startfade, target)
            elif target.Sprite:
                c = target.Sprite.Color
                target.Sprite.Color = Vec4(c.x,c.y,c.z,0) if should_trigger else Vec4(c.x,c.y,c.z,1)

            

            
Zero.RegisterComponent("TriggerDoor", TriggerDoor)