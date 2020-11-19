import numpy as np
import vtolparam as P

class PDController:
    def __init__(self,kp,kd,kp1=None,kd1=None):
        self.kp = kp
        self.kd = kd
        self.kpth = kp1
        self.kdth = kd1

    def updateh(self,xref,x,xdot):
        e = xref - x
        Fh = (P.mc+P.ml+P.mr)*P.g + self.kp*e - self.kd * xdot
        return Fh

    def updatelat(self,zref,z,th,zdot,thdot):
        e = zref - z
        thref = self.kp * e - self.kd *zdot
        eth = thref + th    #   Nm
        tau = -self.kpth*eth - self.kdth * thdot
        return tau

