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


class PIDController:
    def __init__(self,kp,kd,ki,kp1=None,kd1 = None):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.kpth = kp1
        self.kdth = kd1
        self.sigma = P.sigma
        self.Fh_limits = P.u_limit
        self.tau_limit = P.v_limit
        self.integrator = 0.0
        self.e_delay_1 = 0.0
        self.beta = (2*P.sigma - P.step_t)/(2*P.sigma + P.step_t)
        self.xdot_delay_1 = 0.0
        self.x_delay_1 = 0.0
        self.integrator_th = 0.0
        self.beta_th = (2*P.sigma_th - P.step_t)/(2*P.sigma_th + P.step_t)
        self.th_delay_1 = 0.0
        self.th_dot_delay_1 = 0.0

    def updateh(self,xref,x):
        e = xref-x
        self.integrator += P.step_t*(e + self.e_delay_1)/2

        self.xdot_delay_1 = self.beta*self.xdot_delay_1 + (1-self.beta)*(x-self.x_delay_1)/P.step_t
        u_unsat = (P.mc+P.ml+P.mr)*P.g + self.kp *e +self.ki*self.integrator -self.kd*self.xdot_delay_1
        u_sat = self.saturate(u_unsat,P.u_limit)
        
        self.integrator += (u_sat-u_unsat)/self.ki

        self.e_delay_1 = e
        self.x_delay_1 = x

        return u_sat
    
    def updatelat(self,zref,z,th):
        erz = zref - z
        self.integrator += P.step_t*(erz  + self.e_delay_1)/2

        self.xdot_delay_1 = self.beta*self.xdot_delay_1 +(1-self.beta)* (z-self.x_delay_1)/P.step_t
        th_unsat = self.kp*erz + self.ki*self.integrator -self.kd*self.xdot_delay_1
        th_sat = self.saturate(th_unsat,P.th_limit)
        self.integrator += (th_sat-th_unsat)/self.ki
        self.e_delay_1 = erz
        self.x_delay_1 = z
        
        eth = th_sat + th
        self.th_dot_delay_1 = self.beta_th*self.th_dot_delay_1 +(1-self.beta_th)* (th-self.th_delay_1)/P.step_t
        tau_unsat = -self.kpth*eth -self.kdth*self.th_dot_delay_1
        tau_sat = self.saturate(tau_unsat,P.v_limit)
        self.th_delay_1 = th

        return tau_sat



    def saturate(self,u,lim):
        if abs(u) > lim:
            u = u*lim/abs(u)
        return u