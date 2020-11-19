import numpy as np
import vtolparam as P

class vtolDynamics:
    def __init__(self):
        self.g = P.g
        self.mc = P.mc
        self.m = P.mr
        self.b = P.b
        self.d = P.d
        self.Jc = P.Jc
        self.state = np.array([[P.zv0],[P.h0]\
            ,[P.theta0],[P.zvdot0],[P.hdot0]\
                ,[P.thetadot0]])
        self.u_lim = P.u_limit
        self.v_lim = P.v_limit
        self.Ts = P.step_t
    
    def update(self,u,v):
        u = self.saturate(u,self.u_lim)
        v = self.saturate(v,self.v_lim)

        self.rk4_step(u,v)

        y = self.h()

        return y


    def f(self,state,u,v):
        zv = state.item(0)
        h = state.item(1)
        theta = state.item(2)
        zvdot = state.item(3)
        hdot = state.item(4)
        thetadot = state.item(5)
        
        M = np.array([[self.mc +self.m +self.m , 0, 0 ],
                      [0, self.mc +self.m +self.m, 0],
                      [0, 0, self.Jc + (self.m +self.m)*(self.d**2)]])
        C = np.array([-u*np.tan(theta)-self.b*zvdot,
                      (u-((self.mc +self.m +self.m)*self.g)),
                      v])
        
        dummy = np.linalg.inv(M) @ C
        xdot = np.array([[state.item(3)],[state.item(4)]\
            ,[state.item(5)],[dummy[0]],[dummy[1]],[dummy[2]]])
        
        return xdot

    def h(self):
        z = self.state.item(0)
        h = self.state.item(1)
        th = self.state.item(2)
        zdot = self.state.item(3)
        hdot = self.state.item(4)
        thdot = self.state.item(5)
        y = np.array([[z],[h],[th],[zdot],[hdot],[thdot]])
        return y

    
    def rk4_step(self,u,v):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        F1 = self.f(self.state,u,v)
        F2 = self.f(self.state + self.Ts / 2 * F1,u,v)
        F3 = self.f(self.state + self.Ts / 2 * F2,u,v)
        F4 = self.f(self.state + self.Ts * F3,u,v)
        self.state += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

    def saturate(self,u,lim):
        if abs(u) > lim:
            u = u*lim/abs(u)
        return u