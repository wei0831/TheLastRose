import Zero
import Events
import Property
import VectorMath

class KeyRing:
    
    def Initialize(self, initializer):
       self.Keys = []
       Zero.Connect(self.Owner, "GetKeyEvent", self.OnGetKey)
       Zero.Connect(self.Owner, "TryKeyEvent", self.OnTryKey)
       
    def OnGetKey(self, GetKeyEvent):
        self.Keys.append(GetKeyEvent.KeyValue)
        if GetKeyEvent.Callback:
            GetKeyEvent.Callback()
            
    def OnTryKey(self, TryKeyEvent):
        if self.TryKey(TryKeyEvent.KeyHole):
            TryKeyEvent.Callback()
            
    def GetKeySet(self):
        return self.Keys
        
    def TryKey(self, KeyHole):
        if KeyHole in self.Keys:
            self.Keys.remove(KeyHole)
            return True
        elif KeyHole == "":
            return True
        else:
            return False
        

Zero.RegisterComponent("KeyRing", KeyRing)