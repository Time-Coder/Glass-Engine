from enum import Enum
import pytweening

class EasingCurve(Enum):

    Linear = 0
    InQuad = 1
    OutQuad = 2
    InOutQuad = 3
    OutInQuad = 4
    InCubic = 5
    OutCubic = 6
    InOutCubic = 7
    OutInCubic = 8
    InQuart = 9
    OutQuart = 10
    InOutQuart = 11
    OutInQuart = 12
    InQuint = 13
    OutQuint = 14
    InOutQuint = 15
    OutInQuint = 16
    InSine = 17
    OutSine = 18
    InOutSine = 19
    OutInSine = 20
    InExpo = 21
    OutExpo = 22
    InOutExpo = 23
    OutInExpo = 24
    InCirc = 25
    OutCirc = 26
    InOutCirc = 27
    OutInCirc = 28
    InElastic = 29
    OutElastic = 30
    InOutElastic = 31
    OutInElastic = 32
    InBack = 33
    OutBack = 34
    InOutBack = 35
    OutInBack = 36
    InBounce = 37
    OutBounce = 38
    InOutBounce = 39
    OutInBounce = 40

    def __call__(self, progress:float)->float:
        if self == EasingCurve.Linear:
            return progress
        
        func_name = "ease" + str(self)[len("EasingCurve."):]
        func = getattr(pytweening, func_name)
        return func(progress)
        