import Zero
import Events
import Property
import VectorMath
import Action
import math
import itertools
Vec3 = VectorMath.Vec3

class WaterLayerGenerator:
    RecsInX = Property.Int(10)
    RecsInY = Property.Int(10)
    Rec_W = Property.Float(0.5)
    Rec_H = Property.Float(0.5)
    CreateWaterRing = Property.Bool(False)
    
    def Initialize(self, initializer):
        self.xnum = int(self.Owner.Transform.Scale.x * 2)
        self.ynum = int(self.Owner.Transform.Scale.y * 2)
        self.RecArray = [[None for x in range(self.xnum)] for x in range(self.ynum)] 
        self.freeze_event = Zero.ScriptEvent()
        self.frozen_set = set()
        self.curious_offset = Vec3(0,0.035,0)
        
        if self.CreateWaterRing:
            self.cache_ring = dict()
            self.cache_ring2 = dict()
        
        onlytop = "WaterTopOnly"
        for i, col in enumerate(self.RecArray):
            for j, item in enumerate(col):
                boxwidth = self.Owner.Sprite.Size.x * self.Owner.Transform.Scale.x
                boxheight = self.Owner.Sprite.Size.y * self.Owner.Transform.Scale.y
                
                self.origin = self.Owner.Transform.Translation + Vec3(-boxwidth/2 + self.Rec_W * 0.5, + boxheight/2 - self.Rec_W * 0.5, 0.1)
                
                v3 = Vec3((self.Rec_W+0.0000001)*j, -1*(self.Rec_H+0.0000001)*i, 0)
                objname = "WaterTop" if i == 0 else "WaterMid"
                item = self.Space.CreateAtPosition(objname, self.origin + v3)
                item.AttachToRelative(self.Owner)
                self.RecArray[i][j] = item
                
                if self.CreateWaterRing:
                    # manage side waves
                    obj = None
                    if j == self.xnum - 1:
                        obj = self.Space.CreateAtPosition(onlytop, self.origin + v3 + Vec3(0,0,1))
                        obj.Transform.RotateByAngles(Vec3(0,0,-math.pi/2))
                        
                    if j == 0:
                        obj = self.Space.CreateAtPosition(onlytop, self.origin + v3 + Vec3(0,0,1))
                        obj.Transform.RotateByAngles(Vec3(0,0,math.pi/2))
                        
                    if obj:
                        self.cache_ring[(j,i)] = obj
                        
                    # manage bottom waves
                    if i == self.ynum-1:
                        obj = self.Space.CreateAtPosition(onlytop, self.origin + v3 + self.curious_offset + Vec3(0,0,1))
                        obj.Transform.RotateByAngles(Vec3(0,0,math.pi))
                        self.cache_ring2[(j,i)] = obj

    def GetNeighbor(self, pair):
        cand_x = (pair[0] - 1, pair[0], pair[0] + 1)
        cand_y = (pair[1] - 1, pair[1], pair[1] + 1)
        return tuple((x, y) for x in cand_x if x >= 0 and x < self.xnum for y in cand_y if y >= 0 and y < self.ynum)
        
    
    def FreezeAt(self, pos):
        idx_x = int((pos.x - self.origin.x) / self.Rec_W)
        idx_y = int((self.origin.y-pos.y) / self.Rec_H)
        
        if idx_x < 0:
            idx_x = 0
        elif idx_x >= self.xnum:
            idx_x = self.xnum-1
        if idx_y < 0:
            idx_y = 0
        elif idx_y >= self.ynum:
            idx_y = self.ynum-1
            
        self.FreezeThem(((idx_x, idx_y),))
                
    def FreezeThem(self, poss):
        def FreezeHelper(target):
            if not target.FreezeAnimReceiver.IsActivated():
                target.FreezeAnimReceiver.Freeze()
                ice = self.Space.CreateAtPosition("IceParticle", target.Transform.WorldTranslation)
                ice.TimedDeath.Active = True
               
                ice.SphericalParticleEmitter.EmitRate = 3
                ice.SphericalParticleEmitter.EmitCount = 1
                ice.SphericalParticleEmitter.ResetCount()

        for pair in poss:
            target = self.RecArray[pair[1]][pair[0]]
            FreezeHelper(target)
                
        if self.CreateWaterRing:
            for pair in poss:
                if pair in self.cache_ring:
                    FreezeHelper(self.cache_ring[pair])
                if pair in self.cache_ring2:
                    FreezeHelper(self.cache_ring2[pair])
                    self.cache_ring2[pair].Transform.Translation -= self.curious_offset
            
                
        nextset = set(sum([self.GetNeighbor(pair) for pair in poss], tuple()))
        nextset -= self.frozen_set
        self.frozen_set.update(nextset)
        
        if nextset:
            seq = Action.Sequence(self.Owner.Actions)
            Action.Delay(seq, 0.1)
            Action.Call(seq, self.FreezeThem, (nextset,))

Zero.RegisterComponent("WaterLayerGenerator", WaterLayerGenerator)