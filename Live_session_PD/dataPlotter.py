import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as ml

plt.ion()
class dataplotter:
    def __init__(self):
        self.rows = 4
        self.columns = 1
        self.fig ,self.axis = plt.subplots(self.rows,self.columns,sharex = True)
        self.t = []
        self.output = []
        self.outputref = []
        self.control = []
        self.first_ref = True
        self.first_out = True
        self.first_cnt = True
        self.plot_store = []
        self.y_labels = ["z(m)","h(m)","theta(rad)", "Fh(N)","Tau(Nm)"]
        self.x_labels = ["time(s)"]
        self.title = ["VTOL"]
        for i in range(self.rows):
            if i ==0:
                self.plot_store.append(plotdesign(self.axis[i],y_lable = self.y_labels[i],title=self.title[0]))
            elif i == (self.rows -1):
                self.plot_store.append(plotdesign(self.axis[i],x_lable=self.x_labels[0], y_lable = self.y_labels[i]))
            else:
                self.plot_store.append(plotdesign(self.axis[i],y_lable = self.y_labels[i]))
        
    def update(self,t,ref,output,control):  #   ref = [href,zref,thref], output = vtol.state,control = [Fh,tau]
        self.t.append(t)
        for i in range(len(ref)):
            if self.first_ref == False:
                self.outputref[i].append(ref[i]) 
            else:
                self.outputref.append([ref[i]])
                if len(self.outputref) == len(ref):
                    self.first_ref = False

        for i in range(int(len(output)/2)):
            if self.first_out == False:
                self.output[i].append(output.item(i))
            else:
                self.output.append([output.item(i)])
                if len(self.output) == int(len(output)/2):
                    self.first_out = False
        for i in range(len(control)):
            if self.first_cnt == False:
                self.control[i].append(control[i]) 
            else:
                self.control.append([control[i]])
                if len(self.control) == len(control):
                    self.first_cnt = False

        for i in range(len(self.plot_store)):
            if i<len(self.outputref):    
                self.plot_store[i].plot_update(self.t,[self.output[i],self.outputref[i]])
            elif i==len(self.outputref):    
                self.plot_store[i].plot_update(self.t,[self.output[i]])
            else:
                self.plot_store[i].plot_update(self.t,[self.control[i-int(len(output)/2)]])



class plotdesign:
    def __init__(self,ax='',x_lable='',y_lable='',title='',legend = None):
        self.line_style = ["-","-","-.","--"]
        self.color = ["blue","green","red","black","yellow","orange"]
        self.legend = legend
        self.ax = ax
        self.ax.set_xlabel(x_lable)
        self.ax.set_ylabel(y_lable)
        self.ax.set_title(title)
        self.ax.grid(True)
        self.first = True
        self.line_store = []

    def plot_update(self,t,data):
        if self.first == True:
            for i in range(len(data)):
                self.line_store.append(ml.Line2D(t,data[i],ls = self.line_style[i],color = self.color[i],label = self.legend))
                self.ax.add_line(self.line_store[i])
            self.first = False

        else:
            for i in range(len(data)):
                self.line_store[i].set_xdata(t)
                self.line_store[i].set_ydata(data[i])
        
        self.ax.relim()
        self.ax.autoscale()
