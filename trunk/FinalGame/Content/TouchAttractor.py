import Zero
import Events
import Property
import VectorMath

class TouchAttractor:
    def Initialize(self, initializer):
        self.EnsureObserver()
        self.target = None
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def EnsureObserver(self):
        self.observers = []
        def Null():
            pass
        self.EnsureObserver = Null
        
        
    def OnCollision(self, CollisionEvent):
        self.target = CollisionEvent.OtherObject
        Zero.Disconnect(self.Owner, Events.CollisionStarted, self)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        self.target.RigidBody.Kinematic = True
        self.target.Transform.WorldTranslation = self.target.Transform.WorldTranslation * 0.8 + self.Owner.Transform.WorldTranslation * 0.2
        
        if (self.target.Transform.WorldTranslation-self.Owner.Transform.WorldTranslation).length() < 0.0001:
            Zero.Disconnect(self.Space, Events.LogicUpdate, self)
            
        if self.target.PlayerController:
            self.target.PlayerController.DontUpdateAnim = True
            self.target.PlayerController.PlayPainAnim()
            

Zero.RegisterComponent("TouchAttractor", TouchAttractor)