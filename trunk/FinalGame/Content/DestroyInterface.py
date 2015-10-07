import Zero
import Events
import Property
import VectorMath

class DestroyInterface:
    def Initialize(self, initializer):
        self.InitializeObserverList()
        if self.Owner.DestroyCreateArchetype:
            self.Destroyer = self.Owner.DestroyCreateArchetype
        elif self.Owner.DestroyPlayAnim:
            self.Destroyer = self.Owner.DestroyPlayAnim
        elif self.Owner.DestroyFadeAnim:
            self.Destroyer = self.Owner.DestroyFadeAnim
        elif self.Owner.DestroyTeleport:
            self.Destroyer = self.Owner.DestroyTeleport
        else: 
            self.Destroyer = None
    def Destroy(self):

        for callback in self.destroy_observers:
            callback()
        self.destroy_observers = []
    
        if self.Destroyer:
            self.Destroyer.Destroy()
        else:
            self.Owner.Destroy()
    def InitializeObserverList(self):
        self.destroy_observers = []
        def Null():
            pass
        self.InitializeObserverList = Null
    def RegisterObserver(self,callback):
        self.InitializeObserverList()        
        self.destroy_observers.append(callback)
        
Zero.RegisterComponent("DestroyInterface", DestroyInterface)