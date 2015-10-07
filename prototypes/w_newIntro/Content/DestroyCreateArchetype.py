import Zero
import Events
import Property
import VectorMath

class DestroyCreateArchetype:
    Archetype = Property.Archetype()
    EffectLifeTime = Property.Float(0)
    DieDelay = Property.Float(0)
    
    def Initialize(self, initializer):
        self.activated = False
        if not self.Owner.DestroyInterface:
            self.Owner.AddComponentByName("DestroyInterface")
        
    def Destroy(self):
        if not self.activated:
            self.activated = True
            
            created = self.Space.CreateAtPosition(self.Archetype, self.Owner.Transform.Translation)
                    
            if self.EffectLifeTime > 0:
                self.AddDestroyAction(created, self.EffectLifeTime)

            if self.DieDelay > 0:
                self.AddDestroyAction(self.Owner, self.DieDelay)
            else:
                self.Owner.Destroy()
            
    def AddDestroyAction(self, target, countdown):
        def Destroy(self):
            self.Owner.Destroy()
                
        if not target.ActionList:
            target.AddComponentByName("ActionList")
            target.ActionList.EmptyAll()
            target.ActionList.AddCallback(Destroy, has_self=True, blocking=False, countdown=countdown)

Zero.RegisterComponent("DestroyCreateArchetype", DestroyCreateArchetype)