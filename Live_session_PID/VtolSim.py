import numpy as np
import signalGenerator as sg
import vtolanimator as anim
import dataPlotter as dp
import vtolcontroller as vc
import vtoldynamics as dyn
import vtolparam as P
import matplotlib.pyplot as plt

reference1 = sg.signalGenerator(amplitude=2,frequency=0.05,y_offset=1)
reference2 = sg.signalGenerator(amplitude=0.3,frequency=0.05,y_offset=1)

lon_controller = vc.PIDController(P.kph,P.kdh,P.kih)
lat_controller = vc.PIDController(P.kpz,P.kdz,P.kiz,P.kpth,P.kdth)

vtol = dyn.vtolDynamics()
animator = anim.vtolanimator()
dataplotter = dp.dataplotter()

t = P.start_t
y = vtol.h()
while t< P.end_t:
    t_plot = t + P.plot_step
    while t<t_plot:
        href = reference1.square(t)
        zv = reference2.square(t)
        f_lon = lon_controller.updateh(xref=href,x=y.item(1))
        tau = lat_controller.updatelat(zref=zv,z=y.item(0),th=y.item(2))
        y = vtol.update(f_lon,tau)
        t += P.step_t
    plt.pause(0.0001)
    animator.update(vtol.state[0],vtol.state[1],vtol.state[2])
    dataplotter.update(t=t,ref=[zv,href],output=vtol.state,control=[f_lon,tau])
plt.waitforbuttonpress()
plt.close()