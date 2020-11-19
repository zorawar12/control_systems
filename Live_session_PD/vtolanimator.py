import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np
import vtolparam as P
import matplotlib as mpl

class vtolanimator:
    def __init__(self):
        self.pod_h = P.pod_height
        self.pod_w = P.pod_width
        self.first = True
        self.comp = []
        self.fig, self.ax = plt.subplots()
        plt.axis([-2*self.pod_w, 20.0*self.pod_w, -2*self.pod_w,
                  20.0*self.pod_w])
        plt.plot([-50.0*self.pod_w, 50.0*self.pod_w], [0, 0], 'b--')


    def update(self,z,h,theta):
        self.pod(z,h,theta)
        self.arm_l(z,h,theta)
        self.arm_r(z,h,theta)
        self.fan_l(z,h,theta)
        self.fan_r(z,h,theta)

    
    def pod(self,z,h,theta):
        x = z-self.pod_w/2
        y = h-self.pod_h/2
        corner = (x,y)
        if self.first == True:
            self.comp.append(pat.Rectangle(corner,width= self.pod_w, height=self.pod_h,edgecolor = "blue",facecolor = "blue"))
            self.ax.add_patch(self.comp[0])
        else:
            self.comp[0].set_xy(corner)
            # t2 = mpl.transforms.Affine2D().rotate_around(corner[0]+self.pod_w/2, corner[1]+self.pod_h/2,theta)+ plt.gca().transData
            # self.comp[0].set_transform(t2)

    def fan_l(self,z,h,theta):
        x = z - (P.d+self.pod_w/2)*np.cos(theta)
        y = h - (P.d+self.pod_w/2)*np.sin(theta)
        center = (x,y)
        if self.first ==True:
            self.comp.append(pat.Ellipse(center,width= 2*self.pod_w/3, height=self.pod_h/4,edgecolor = "black",facecolor = "black"))
            self.ax.add_patch(self.comp[3])
        else:
            self.comp[3].set_center(center)
            # t2 = mpl.transforms.Affine2D().rotate_around(center[0], center[1],theta)+ plt.gca().transData
            # self.comp[3].set_transform(t2)

    def fan_r(self,z,h,theta):
        x = z + (P.d+self.pod_w/2)*np.cos(theta)
        y = h + (P.d+self.pod_w/2)*np.sin(theta)
        center = (x,y)
        if self.first ==True:
            self.comp.append(pat.Ellipse(center,width= 2*self.pod_w/3, height=self.pod_h/4,edgecolor = "black",facecolor = "black"))
            self.ax.add_patch(self.comp[4])
            self.first = False
        else:
            self.comp[4].set_center(center)
            # t2 = mpl.transforms.Affine2D().rotate_around(center[0], center[1],theta)+ plt.gca().transData
            # self.comp[4].set_transform(t2)

    def arm_l(self,z,h,theta):
        x1 = z - (self.pod_w/2)*np.cos(theta)
        y1 = h - (self.pod_w/2)*np.sin(theta)
        x2 = z - (P.d+self.pod_w/2)*np.cos(theta)
        y2 = h - (P.d+self.pod_w/2)*np.sin(theta)
        if self.first == True:    
            line, = self.ax.plot([x1,x2],[y1,y2],color = "black")
            self.comp.append(line) 
        else:
            self.comp[1].set_xdata([x1,x2])
            self.comp[1].set_ydata([y1,y2])
        
    def arm_r(self,z,h,theta):
        x1 = z + (self.pod_w/2)*np.cos(theta)
        y1 = h + (self.pod_w/2)*np.sin(theta)
        x2 = z + (P.d+self.pod_w/2)*np.cos(theta)
        y2 = h + (P.d+self.pod_w/2)*np.sin(theta)
        if self.first == True:    
            line, = self.ax.plot([x1,x2],[y1,y2],color = "black")
            self.comp.append(line)      
        else:
            self.comp[2].set_xdata([x1,x2])
            self.comp[2].set_ydata([y1,y2])


