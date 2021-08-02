import kivy
from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.label import Label 
from kivy.uix.boxlayout import BoxLayout 
from plyer import accelerometer
from plyer import gyroscope
from kivy.clock import Clock
from kivy.uix.widget import Widget
from matplotlib import pyplot as plt 
from gardens.backend_kivyagg import FigureCanvasKivyAgg
import numpy as np 
import os


class Plotting(Widget):

	def __init__(self):
		super(Plotting, self).__init__()
		self.fig = plt.figure()
		self.axis = self.fig.add_axes([0.07,0.05,0.9,0.9])
		
		self.x_val, self.y_val, self.z_val  = [0],[0],[0]
		self.x_time = [0] 
		self.i = 0

	def start_plot(self,values,xLabel,yLabel):

		self.axis.set_xlabel(xLabel)
		self.axis.set_ylabel(yLabel)
		self.x_time.append(self.x_time[-1]+1)
		
		self.x_val.append(values[0])
		line, = self.axis.plot(self.x_time,self.x_val,'r-',label='X')
		self.x_val = self.x_val[1:]
		
		
		self.y_val.append(values[1])
		line, = self.axis.plot(self.x_time,self.y_val,'g-',label='Y')
		self.y_val = self.y_val[1:]
		
		self.z_val.append(values[2])
		line, = self.axis.plot(self.x_time,self.z_val,'b-',label='Z')
		self.z_val = self.z_val[1:]
		
		self.x_time = self.x_time[1:]
		
		if self.axis.get_legend() == None:
			self.axis.legend()

		self.fig.canvas.draw()
		
	def sine_plot(self,xLabel,yLabel):
		self.axis.set_xlabel(xLabel)
		self.axis.set_ylabel(yLabel)
		self.axis.set_xlim((0,30))
		self.axis.set_ylim((-1,1))
		x = np.arange(0,90,0.5)
		y = np.sin(x)
		line, = self.axis.plot(x[self.i:self.i+2],y[self.i:self.i+2],'b-',label='Sine')
		if self.axis.get_legend() == None :
			self.axis.legend()
		self.i += 1
		self.fig.canvas.draw()
		
	def square_plot(self,xLabel,yLabel):
		self.axis.set_xlabel(xLabel)
		self.axis.set_ylabel(yLabel)
		self.axis.set_xlim((0,22))
		self.axis.set_ylim((-0.5,1.3))
		x = np.linspace(0,20,100)
		y = np.array([1 if np.floor(2 * t) % 2 == 0 else 0 for t in x])
		line, = self.axis.plot(x[self.i:self.i+2],y[self.i:self.i+2],'b-',label='Sine')
		if self.axis.get_legend() == None :
			self.axis.legend()
		self.i += 1
		self.fig.canvas.draw()

	def clear_plot(self):
		self.axis.cla()
		self.fig.canvas.draw()

class ReadAccelerometer(App):
	
	def build(self):
		B = BoxLayout(orientation = 'horizontal')
		b1 = BoxLayout(size_hint=(1.7,1))
		b2 = BoxLayout(orientation='vertical')
		b3 = BoxLayout(orientation='horizontal')
		b4 = BoxLayout(orientation= 'horizontal')
		
		self.plot = Plotting()
		
		self.accelerometerBtn = Button(text='Accelerometer',font_size='15sp',background_color=(1,2,1,1), color=(1,1,1,1), size=(64,64),size_hint=(.1,.2))
		self.gyroscopeBtn = Button(text='Gyroscope',font_size='15sp',background_color=(1,2,1,1), color=(1,1,1,2), size=(64,64),size_hint=(.1,.2))
		self.sineBtn = Button(text='Sine',font_size='15sp',background_color=(1,2,1,1), color=(1,1,1,2), size=(64,64),size_hint=(.2,.2))
		self.squareBtn = Button(text='Square',font_size='15sp',background_color=(1,2,1,1), color=(1,1,1,2), size=(64,64),size_hint=(.2,.2))

		self.pauseBtn = Button(text='Pause',font_size='20sp',background_color=(1,1,2,1), color=(1,1,1,2), size=(32,32),size_hint=(.05,.2))
		self.clearBtn = Button(text='Clear',font_size='20sp',background_color=(1,1,2,1), color=(1,1,1,2), size=(32,32),size_hint=(.05,.2))
		
		self.textLabel = Label(text='Displayed here')
		self.textBtn = Button(text='display')
		
	
		self.accelerometerBtn.bind(on_press = self.accelerometerData)	
		self.gyroscopeBtn.bind(on_press = self.gyroscopeData)
		self.sineBtn.bind(on_press = self.sineData)
		self.squareBtn.bind(on_press = self.squareData)
		self.textBtn.bind(on_press = self.displayData)
		self.pauseBtn.bind(on_press = self.pauseData)	
		self.clearBtn.bind(on_press = self.clearData)

		b1.add_widget(FigureCanvasKivyAgg(plt.gcf()))
		b3.add_widget(self.pauseBtn)
		b3.add_widget(self.clearBtn)
		b4.add_widget(self.accelerometerBtn)
		b4.add_widget(self.gyroscopeBtn)
		b2.add_widget(b4)
		b2.add_widget(self.sineBtn)
		b2.add_widget(self.squareBtn)
		b2.add_widget(self.textLabel)
		b2.add_widget(self.textBtn)
		b2.add_widget(b3)
		B.add_widget(b1)
		B.add_widget(b2)
		
		#b.add_widget(self.label2)
		#b.add_widget(self.label3)
		return B 

	def accelerometerData(self,event):
		self.accelerometerBtn.disabled = True
		self.gyroscopeBtn.disabled = True
		self.sineBtn.disabled = True
		self.squareBtn.disabled = True
		accelerometer.enable()	
		val = accelerometer.acceleration[:3] 
		if val is not (None, None, None):
			self.plot.start_plot(val,xLabel='Time',yLabel='Acceleration')
		self.c1 = Clock.schedule_once(self.accelerometerData,1)

	def gyroscopeData(self,event):
		self.accelerometerBtn.disabled = True
		self.gyroscopeBtn.disabled = True
		self.sineBtn.disabled = True
		self.squareBtn.disabled = True
		gyroscope.enable()	
		val = gyroscope.rotation[:3] 
		if val is not (None, None, None):
			self.plot.start_plot(val,xLabel='Time',yLabel='gyroscope')  
		self.c1 = Clock.schedule_once(self.gyroscopeData,1)	
		
	def sineData(self,event):
		self.accelerometerBtn.disabled = True
		self.gyroscopeBtn.disabled = True
		self.sineBtn.disabled = True
		self.squareBtn.disabled = True
		self.plot.sine_plot(xLabel='Time',yLabel='Sine')
		self.c1 = Clock.schedule_once(self.sineData,0.5)
		
	def squareData(self,event):
		self.accelerometerBtn.disabled = True
		self.gyroscopeBtn.disabled = True
		self.sineBtn.disabled = True
		self.squareBtn.disabled = True
		self.plot.square_plot(xLabel='Time',yLabel='Voltage')
		self.c1 = Clock.schedule_once(self.squareData,0.5)
		
	def displayData(self,event):
		'''text = open('monoFile.txt','w+')
		text.write('written')
		text.close()'''
		#self.textLabel.text = os.getcwd()
		text = open('Phone Storage/miniProject/data.txt').readline()
		self.textLabel.text = text

	def pauseData(self,event):
		#accelerometer.disable()
		self.accelerometerBtn.disabled = False
		self.gyroscopeBtn.disabled = False
		self.sineBtn.disabled = False
		self.squareBtn.disabled = False
		self.c1.cancel() 
		#self.plot.clear_plot()

	def clearData(self,event):	
		self.accelerometerBtn.disabled = False
		self.gyroscopeBtn.disabled = False
		self.sineBtn.disabled = False
		self.squareBtn.disabled = False
		self.c1.cancel()
		self.plot.clear_plot()

root = ReadAccelerometer()
root.run()
