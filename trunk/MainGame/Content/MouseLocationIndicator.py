import Zero
import Events
import Property
import VectorMath
import random
Vec3 = VectorMath.Vec3
import math

class MouseLocationIndicator:
    Range = Property.Float(6.0)
    ShadeTable = Property.ResourceTable()
    Deactivated = Property.Bool(False)
    OverrideColliderSize = Property.Float(1.23)
    
    def Initialize(self, initializer):
        Zero.Mouse.Cursor = Zero.Cursor.Invisible
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, Events.MouseUpdate, self.OnMouseUpdate)
        Zero.Connect(self.Space, Events.MouseUp, self.OnMouseUp)
        Zero.Connect(self.Space, Events.MouseDown, self.OnMouseDown)
        Zero.Connect(self.Space, Events.RightMouseUp, self.OnRightMouseUp)
        Zero.Connect(self.Space, Events.RightMouseDown, self.OnRightMouseDown)
        
        if self.OverrideColliderSize:
            self.Owner.SphereCollider.Radius = self.OverrideColliderSize
        
        self.initial_size = self.Owner.Transform.Scale
        self.ball_size = self.Owner.SphereCollider.Radius
       
        self.hero = self.Space.FindObjectByName("Player")
        self.Active = False
        self.TouchAttackable = False
        self.TouchGrowable = False
        self.WithInRange = False
        self.MousePos = Vec3(0,0,0)
        
        self.touched_plant = None
        
        self.touch_point = Vec3(0,0,0)
        self.touch_normal = Vec3(0,1,0)
        self.init_rotate = self.Owner.Transform.Rotation
        
        self.scale_table = dict(TreeSkillMushroom=1,TreeSkillWhirlingnut=2, TreeSkillRootplant=2)
        self.color_table = dict(PhysSkillPoison=Vec3(.7,1,.7,0.75), PhysSkillFire=Vec3(1,.7,.7,0.8), PhysSkillIce=Vec3(.7,.7,1,0.8))
        self.anim_table = dict(PhysSkillPoison=self.Owner.PoisonAnim, PhysSkillFire=self.Owner.BurnAnim, PhysSkillIce=self.Owner.FreezeAnim)
        
        self.candidate_growable_penetrate = 0
        self.candidate_annihilator_penetrate = 0
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Transform.Translation = self.MousePos
        
        self.UpdateEnvironmentInfo()
        if self.Active and self.WithInRange:
            self.PerformAbsorb()
            
        target_color = VectorMath.Vec4(1, 1, 1, 0.25)
        target_scale = 2
        target_sprite = self.ShadeTable.FindValue("Circle")
        radius = 1.2
        self.Owner.Transform.Rotation = self.init_rotate
        
        skillname = self.hero.AbilityStatus.GetTreeSkillName()
        physskill = self.hero.AbilityStatus.GetPhysSkillName()
        if physskill:
            self.Owner.BurnAnim.Active = False
            self.Owner.FreezeAnim.Active = False
            self.Owner.PoisonAnim.Active = False
        
        if self.TouchPlant and not self.Deactivated:
                target_sprite = self.ShadeTable.FindValue("Cross")
                target_scale = 5
                target_color = VectorMath.Vec4(1,1,1,1)
                self.SetPlantAlpha(0.5)
                
        elif self.WithInRange and not self.Deactivated:
            if self.TouchAttackable:
                target_color = VectorMath.Vec4(1, 0, 0, 0.25)
                target_scale = 5        
                radius = 2.4
            elif self.TouchAnnihilator or not skillname:
                target_color = VectorMath.Vec4(1,1,1,1)
                target_scale = 0.5
            

            elif self.TouchGrowable and not self.hero.AbilityStatus.NoTreeSkill():
                target_color = VectorMath.Vec4(1, 1, 1, 0.75)
                target_scale = 5
                target_sprite = self.ShadeTable.FindValue(skillname)
                target_scale *= self.scale_table[skillname]
                
                if not skillname == "TreeSkillWhirlingnut":
                    self.Owner.Transform.RotateByAngles(VectorMath.Vec3(0,0,self.touch_normal.angleZ()-math.pi/2))
                
                if physskill:
                    target_color = self.color_table[physskill]
                    self.anim_table[physskill].Active = True
 
        else:
            target_color = VectorMath.Vec4(1,1,1,1)
            target_scale = 0.5
        
        self.Owner.SphereCollider.Radius = radius
        self.Owner.Sprite.Color = target_color
        self.Owner.Transform.Scale = self.initial_size * target_scale
        self.Owner.SphereCollider.Radius = self.ball_size / target_scale
        self.Owner.Sprite.SpriteSource = target_sprite
        
        
    def SetPlantAlpha(self, alpha):
        if self.touched_plant:
            if self.touched_plant.Sprite:
                self.touched_plant.Sprite.Color = VectorMath.Vec4(1,1,1,alpha)
            if self.touched_plant.Hierarchy:
                for child in self.touched_plant.Hierarchy.Children:
                    if child.Sprite:
                        child.Sprite.Color = VectorMath.Vec4(1,1,1,alpha)
                        
    def PerformAbsorb(self):
        if not self.Deactivated:
            heroClickEvent = Zero.ScriptEvent()
            heroClickEvent.Target = self.hero
            self.Owner.Region.DispatchEvent("heroClickEvent", heroClickEvent)
        
    def OnMouseUpdate(self, MouseUpdateEvent):
        self.MousePos = MouseUpdateEvent.ToWorldZPlane(0)
        
        if self.Space.TimeSpace.Paused:
            Zero.Mouse.Cursor = Zero.Cursor.Hand
            self.Owner.Sprite.Visible = False
        else:
            Zero.Mouse.Cursor = Zero.Cursor.Invisible
            self.Owner.Sprite.Visible = True
            
    def OnMouseDown(self, MouseDownEvent):
        self.Active = True
        
    def OnMouseUp(self, MouseUpEvent):
        self.Active = False
    
    def OnRightMouseDown(self, MouseDownEvent):
        if not self.Deactivated:
            
            if self.TouchPlant:
                    if self.touched_plant.RigidBody and (not self.touched_plant.RigidBody.Kinematic or not self.touched_plant.RigidBody.Static):
                        self.touched_plant.RigidBody.Kinematic = True
                    self.touched_plant.DestroyInterface.Destroy()
                    self.TouchPlant = False
                    
            elif self.WithInRange: 
                if not self.TouchAnnihilator and self.TouchGrowable:
                    pos = Vec3(self.touch_point.x - self.touch_normal.x/15, self.touch_point.y - self.touch_normal.y/15, 0.011)
                    self.hero.AbilityStatus.Perform(pos, pre_rotate = self.touch_normal)
                
                    
    def UpdateEnvironmentInfo(self):
        
        self.TouchAttackable = False
        self.TouchAnnihilator = False
        self.TouchGrowable = False
        self.TouchPlant = False
                
        self.candidate_growable_penetrate = 0
        self.candidate_annihilator_penetrate = 0
        
        annihilator_points = []

        for contactholder in self.Owner.Collider.Contacts:
            if contactholder.OtherObject.GrowableGround:
                self.TouchGrowable = True
                penetrate = contactholder.FirstPoint.Penetration
                if self.candidate_growable_penetrate < penetrate:
                    self.candidate_growable_penetrate = penetrate
                    self.touch_normal = -contactholder.FirstPoint.WorldNormalTowardsOther
                    self.touch_point= contactholder.FirstPoint.WorldPoint

            if not self.TouchAttackable and contactholder.OtherObject.ClickReceiver and contactholder.OtherObject.ClickReceiver.Receivable:
                self.TouchAttackable = True
                
            if contactholder.OtherObject.PlantAnnihilator:
                annihilator_points.append(contactholder.FirstPoint.WorldPoint)
                    
            
            if contactholder.OtherObject.Collider.CollisionGroup.Name == "Plant":
                if contactholder.OtherObject.DestroyPlayAnim and not contactholder.OtherObject.DestroyPlayAnim.IsActivated():
                    self.TouchPlant = True
                    self.SetPlantAlpha(1)
                    self.touched_plant = contactholder.OtherObject
        
        az = self.touch_normal.angleZ()
        pi2 = math.pi/2.
        right_angled =  any(tuple(abs(az - pi2 * idx) < 0.0001 for idx in  range(4)))
        
        #print(self.touch_normal)
        if not right_angled and annihilator_points:
            self.TouchAnnihilator = True
        else:
            for ap in annihilator_points:
                #print((ap - self.touch_point).length())
                if (ap - self.touch_point).length() < 0.01:
                    self.TouchAnnihilator = True
        
        x2 = (self.MousePos.x  - self.hero.Transform.Translation.x)**2
        y2 = (self.MousePos.y  - self.hero.Transform.Translation.y)**2
        self.WithInRange = x2 + y2 < self.Range**2
        
        if not self.TouchPlant:
            self.SetPlantAlpha(1)
            self.touched_plant = None
        
    def OnRightMouseUp(self, MouseUpEvent):
        pass

Zero.RegisterComponent("MouseLocationIndicator", MouseLocationIndicator)