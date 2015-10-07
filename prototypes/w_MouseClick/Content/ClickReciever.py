import Zero
import Events
import Property
import VectorMath

class ClickReciever:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "heroClickEvent", self.OnHeroClick)

    def OnHeroClick(self, clickEvent):
        print("I am " + self.Owner.Name)
        range = self.Owner.Transform.Translation - clickEvent.Target.Transform.Translation;
        # Range Square bettween hero and monster
        if((range.x * range.x + range.y * range.y) < clickEvent.MaxRangeSqrt):
            print("withInRange...Attack!!")

Zero.RegisterComponent("ClickReciever", ClickReciever)