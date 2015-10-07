import Zero
import Events
import Property
import VectorMath

class HiderScript:
    TeleportDistance = Property.Vector3(VectorMath.Vec3(4,0,0))
    def Initialize(self, initializer):
        self.initial_loc = self.Owner.Transform.WorldTranslation
        self.destination_loc = self.Owner.Transform.WorldTranslation + self.TeleportDistance
        
        self.hided = False
        
        
    def HidingUpdate(self, UpdateEvent):
        self.Owner.Transform.WorldTranslation = 0.95*self.Owner.Transform.WorldTranslation + 0.05*self.destination_loc
        if (self.Owner.Transform.WorldTranslation - self.destination_loc).length() < 0.1:
            Zero.Disconnect(self.Space, Events.LogicUpdate, self)
            
    def UnhidingUpdate(self, UpdateEvent):
        self.Owner.Transform.WorldTranslation = 0.95*self.Owner.Transform.WorldTranslation + 0.05*self.initial_loc
        #print("unhiding",(self.Owner.Transform.WorldTranslation - self.initial_loc).length())
        if (self.Owner.Transform.WorldTranslation - self.initial_loc).length() < 0.1:
            Zero.Disconnect(self.Space, Events.LogicUpdate, self)
            
    def Hide(self):
        if not self.hided:
            self.hided = True
            Zero.Disconnect(self.Owner, Events.LogicUpdate, self)
            Zero.Connect(self.Space, Events.LogicUpdate, self.HidingUpdate)
    def Unhide(self):
        if self.hided:
            self.hided = False
            Zero.Disconnect(self.Owner, Events.LogicUpdate, self)
            Zero.Connect(self.Space, Events.LogicUpdate, self.UnhidingUpdate)

Zero.RegisterComponent("HiderScript", HiderScript)