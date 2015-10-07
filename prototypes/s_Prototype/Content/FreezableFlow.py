import Zero
import Events
import Property
import VectorMath
class FreezableFlow:
    FreezeDelay = Property.Float(1)
    def Initialize(self, initializer):
        self.StartFreezing = False
        self.FreezeCounter = 0
        self.Activated = False
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Activated:
            if self.StartFreezing:
                self.FreezeCounter += UpdateEvent.Dt
                self.Owner.DragEffect.Drag *= 1.1
                if self.FreezeCounter > self.FreezeDelay:
                    self.Activated = True
                    self.Owner.Collider.Ghost = False
                    self.Owner.DragEffect.Active = False
                    self.Owner.GravityEffect.Active = True
                    for contactholder in self.Owner.Collider.Contacts:
                        otherobj = contactholder.OtherObject
                        if otherobj.CannotBeFrozen:
                            continue
                        if otherobj.RigidBody:
                            otherobj.RigidBody.Kinematic= False
                            otherobj.RigidBody.Static= True
                        if otherobj.AIMovementInterface:
                            otherobj.AIMovementInterface.Deactivate()
                        if otherobj.BurnAnim:
                            otherobj.BurnAnim.Active = False
                        if otherobj.PoisonAnim:
                            otherobj.PoisonAnim.Active = False
                        if otherobj.FreezeAnim:
                            otherobj.FreezeAnim.Active = False
        else:
            effect_active = False
            for contactholder in self.Owner.Collider.Contacts:
                if contactholder.OtherObject.CannotBeFrozen:
                    effect_active = True
            if not effect_active:
                self.Owner.GravityEffect.Active = False
                Zero.Disconnect(self.Owner, Events.LogicUpdate, self.OnLogicUpdate)
                
            
                            
                            
            
            
        
    def OnCollision(self, CollisionEvent):
        if not self.Activated:
            if CollisionEvent.OtherObject.CanFreeze:
                if CollisionEvent.OtherObject.CanFreeze.Active:
                    self.StartFreezing = True
                    self.Owner.DragEffect.Active = True
                    self.Owner.BuoyancyEffect.Active = False
                    
            

Zero.RegisterComponent("FreezableFlow", FreezableFlow)