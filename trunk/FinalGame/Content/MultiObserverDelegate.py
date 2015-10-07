import Zero
import Events
import Property
import VectorMath

class MultiObserverDelegate:
    Target = Property.Cog()
    
    def Initialize(self, initializer):
        self.EnsureObservers()
        self.counter = 0
        
        def Activated():
            self.counter -= 1
            if self.counter == 0:
                for callback in self.observers:
                    callback()
                self.observers = None
        
        if self.Owner.Hierarchy:
            for child in self.Owner.Hierarchy.Children:
                if child.MultiObserverDelegate and child.MultiObserverDelegate.Target:
                    self.counter += 1
                    child.MultiObserverDelegate.RegisterObserver(Activated)
                    
        self.counter += 1
        if self.Target:
            self.Target.DestroyInterface.RegisterObserver(Activated)
    def EnsureObservers(self):
        self.observers = []
        def Null():
            pass
        self.EnsureObservers = Null
        
    def RegisterObserver(self, callback):
        self.EnsureObservers()
        self.observers.append(callback)

Zero.RegisterComponent("MultiObserverDelegate", MultiObserverDelegate)