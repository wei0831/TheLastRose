import Zero
import Events
import Property
import VectorMath
class FreezableFlow:
    FreezeDelay = Property.Float(1)
    FreezingObject = Property.Cog()
    def Initialize(self, initializer):
        self.StartFreezing = False
        self.FreezeCounter = 0
        self.Activated = False
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, "FreezeFlowEvent", self.StartFreeze)
        
        
    def StartFreeze(self, FreezeEvent=None):
        if not self.Activated:
            self.StartFreezing = True
            self.Owner.DragEffect.Active = True
            if self.Owner.BuoyancyEffect:
                self.Owner.BuoyancyEffect.Active = False
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Activated:
            if self.StartFreezing:
                self.FreezeCounter += UpdateEvent.Dt
                self.Owner.DragEffect.Drag *= 1.1
                if self.Owner.FlowEffect:
                    self.Owner.FlowEffect.FlowSpeed *= 0.95
                
                #self.Owner.AddComponentByName("FreezeAnim")
                if self.FreezeCounter > self.FreezeDelay:
                    #freezeflow = Zero.ScriptEvent()
                    #self.Owner.Region.DispatchEvent("FreezeFlowEvent", freezeflow)
                    self.Activated = True
                    self.Owner.Collider.Ghost = False
                    self.Owner.DragEffect.Active = False
                    
                    if self.Owner.FlowEffect:
                        self.Owner.FlowEffect.Active = False
                        
                    self.Owner.GravityEffect.Active = True
                    for contactholder in self.Owner.Collider.Contacts:
                        
                        otherobj = contactholder.OtherObject
                        if otherobj.MouseLocationIndicator:
                            continue
                        elif otherobj.CannotBeFrozen:
                            continue
                        elif otherobj.GrowableGround:
                            continue
                        elif otherobj.PlantAnnihilator:
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
                        if otherobj.Hierarchy and not otherobj.FreezableFlow:
                            for child in otherobj.Hierarchy.Children:
                                if child.Sprite:
                                    child.Sprite.AnimationActive = False
                        if otherobj.FreezableFlow:
                            
                            otherobj.FreezableFlow.DirectActivate(self.Owner)
                            
                        otherobj.Transform.Translation *= VectorMath.Vec3(1,1,-1)


        else:
            effect_active = False
            for contactholder in self.Owner.Collider.Contacts:
                if contactholder.OtherObject.CannotBeFrozen:
                    effect_active = True

            if not effect_active:
                s = self.Owner.Sprite.Color
                self.Owner.Sprite.Color = VectorMath.Vec4(s.x * 2.3, s.y * 2.3, s.z * 2.3, 1)
                self.Owner.GravityEffect.Active = False
                if self.Owner.CanHurt:
                    self.Owner.CanHurt.Active = False
                
                self.Owner.WaterLayerGenerator.FreezeAt(self.FreezingObject.Transform.WorldTranslation)
                self.Owner.AddComponentByName("IsSentry")
                Zero.Disconnect(self.Space, Events.LogicUpdate, self)
                
                
    def DirectActivate(self, obj):
        if not self.Activated:
            self.FreezingObject = obj
            self.StartFreeze()
            
    def OnCollision(self, CollisionEvent):
        
        if not self.Activated:            
            otherobj = CollisionEvent.OtherObject
            if otherobj.CanFreeze and otherobj.CanFreeze.Active:
                self.FreezingObject = CollisionEvent.OtherObject
                self.StartFreeze()
                
                    
            

Zero.RegisterComponent("FreezableFlow", FreezableFlow)