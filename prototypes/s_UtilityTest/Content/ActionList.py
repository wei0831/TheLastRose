import Zero
import Events
import Property
import VectorMath

class ActionList:
    Active = Property.Bool(True)
    
    def Initialize(self, initializer):
        self.EnsureListExist()
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate) 
        
    def Activate(self):
        self.Active = True
    
    def EnsureListExist(self):
        # prevent initialize order problem so that TimedCallbacks don't need to be
        # place before other calling components
        if not "Callbacks" in self.__dict__:
            self.Callbacks = []
        
    def PopCurrentAction(self):
        if len(self.Callbacks) > 0:
            self.Callbacks.pop(0)
            
    def AddCurrentAction(self, callback=None, has_self=False, blocking=False, countdown=None):
        self.AddCallback(callback, has_self, blocking, countdown, index=0)
        
    def AddCallback(self, 
                    callback = None, 
                    has_self = False, 
                    blocking = False, 
                    countdown = None,
                    index = None):
        
        self.EnsureListExist()
        if not index:
            self.Callbacks.append([callback, has_self, blocking, countdown])
        else:
            self.Callbacks.insert(index, [callback, has_self, blocking, countdown])
    
    def callback_helper(self, callback, has_self):
        if not callback: 
            return None
        if has_self:
            return callback(self)
        else:
            return callback()
    
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            
            for idx, callback_pair in enumerate(self.Callbacks):
                callback, has_self, blocking, countdown = callback_pair
                done = False
                
                if not countdown is None:
                    callback_pair[3] -= UpdateEvent.Dt
                    if callback_pair[3] < 0:
                        self.callback_helper(callback, has_self)
                        done = True
                else:
                    done = self.callback_helper(callback, has_self)
                    
                if done:
                    self.Callbacks.pop(idx)
                elif blocking:
                    break


Zero.RegisterComponent("ActionList", ActionList)