import Zero
import Events
import Property
import VectorMath
import random 
import Color

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class ClickReceiver:
    GrantTreeAbility = Property.String("")
    GrantPhysAbility = Property.String("")
    
    InitialNormalSoulSpeed = 10
    InitialDeadSoulSpeed = 20
    
    SoulTickInterval = 3
    DeadColor = Color.FloralWhite
    
    ColorDict = dict(TreeSkillMushroom=Vec3(132,65,255,255)*(1/255), TreeSkillWhirlingnut=Vec4(255,80,80,255)*(1/255), TreeSkillRootplant=Vec4(255,65,65,255)*(1/255), PhysSkillFire=Vec4(255,116,65,255)*(1/255), PhysSkillIce=Vec4(65,255,221,255)*(1/255), PhysSkillPoison=Vec4(80,255,65,255)*(1/255))
    
        
    def DestroyOwner(self):
        if self.Owner.DestroyInterface:
            self.Owner.DestroyInterface.Destroy()
        else:
            self.Owner.Destroy()
        
    
    def Initialize(self, initializer):
        self.soultick = 0
        Zero.Connect(self.Owner, "heroClickEvent", self.OnHeroClick)
        
    def ShootSoul(self, speed, target, color=None, size=None, WillDecay=False):
        newSoul = self.Space.CreateAtPosition("SoulEffect", self.Owner.Transform.Translation)
        newSoul.SoulBehavior.SetTarget(target)
        newSoul.RigidBody.Velocity = Vec3(random.uniform(-speed,speed),random.uniform(-speed,speed),0)  
        if color:
            newSoul.SpriteParticleSystem.Tint = color
        if not size is None:
            newSoul.SphericalParticleEmitter.Size = size
        newSoul.SoulBehavior.WillDecay = WillDecay
            
            

    def OnHeroClick(self, clickEvent):
        distance = self.Owner.Transform.Translation - clickEvent.Target.Transform.Translation
        player = clickEvent.Target
                    
        self.Owner.HealthStatus.AddHealth(-1)
        self.Owner.AIMovementInterface.SlowDownBy(0.1, 50)
        self.Owner.Transform.Translation += Vec3(random.uniform(-0.1,0.1),random.uniform(-0.05,0.05),0)
        self.soultick += 1
        
        if self.soultick >= self.SoulTickInterval:
            self.soultick = 0
            self.ShootSoul(self.InitialNormalSoulSpeed, player, size=0.3)

        if self.Owner.HealthStatus.IsDead():            
            for _ in range(20):
                self.ShootSoul(self.InitialDeadSoulSpeed, target=None, color=self.DeadColor, size=0.2, WillDecay=True)
                
            #set ability soul
            abilitysoul = self.Space.CreateAtPosition("AbilitySoul", self.Owner.Transform.Translation)
            callbacks = []
            
            if self.GrantTreeAbility:
                callbacks.append(lambda: player.AbilityStatus.SwapTreeSkill(self.GrantTreeAbility))
                abilitysoul.SpriteParticleSystem.Tint = self.ColorDict[self.GrantTreeAbility]

            if self.GrantPhysAbility:
                callbacks.append(lambda: player.AbilityStatus.SwapPhysSkill(self.GrantPhysAbility))
                abilitysoul.SpriteParticleSystem.Tint = self.ColorDict[self.GrantPhysAbility]
            if callbacks:
                def callbacker():
                    for callback in callbacks:
                        callback()
                abilitysoul.CanTransferAbility.SetCallback(callbacker)
            else:
                abilitysoul.AbilitySoulBehavior.NoMoving = True
            self.DestroyOwner()
                    
            

            
         

Zero.RegisterComponent("ClickReceiver", ClickReceiver)