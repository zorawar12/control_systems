import numpy as np

# system parameters
mc = 1
ml = 0.25
mr = 0.25
d = 0.3
Jc = 0.0042
g = 9.81
b = 0.1


# initialization
zv0 = 1.0
h0 = 0.0
theta0 = 0.0 # rad
zvdot0 = 0.0
hdot0 = 0.0
thetadot0 = 0.0

# simulation details

start_t = 0.0
end_t = 50.0
step_t = 0.01
plot_step = 0.1

# limits

u_limit = 30.0
v_limit = 25.0
th_limit = np.pi/4

# Animation

pod_height = 0.4
pod_width = 0.5

# PID controller
kph = 0.075625*(mc+ml+mr)
kdh = 0.38885*(mc+ml+mr)
kih = 0.00007
kpz = 0.075625/g
kdz = (0.38885*(mc+ml+mr) - b)/((mc+ml+mr)*g)
kiz = 0.000001#0.0334321497515
kpth = 7.5625*(Jc+(ml+mr)*d**2)
kdth = 3.885*(Jc+(ml+mr)*d**2)


# Dirty derivative
sigma = 0.5
sigma_th = 0.05