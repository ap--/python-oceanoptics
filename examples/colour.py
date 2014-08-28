#!/usr/bin/env python2
# -*- coding: utf-8 -*-
""" File:		colour.py
    Author:		Ian Ross Williams
    Last change		2014/08/28
    
    Example usage of the oceanoptics python library to measure the visible colour of light.
    
    The user interface uses GTK3+ idle threads as this was necessary for the live display to remain
    responsive when running on slow computers like the Raspberry Pi.  
    
    Error checking of the USB connection state allows the spectrometer to be unplugged and replugged.
    
    The colour values reported are based on the CIE1931 colour standard (L*,a*,b* colour space).
    The reference light-source is set by pressing the "Set White-point" button.
    
    Requires the file CIE1931and1964.txt to be in the working directory.
"""
import oceanoptics
import os
import re
import time
import threading
import numpy as np
from scipy.interpolate import interp1d
from usb.core import USBError

#http://python-gtk-3-tutorial.readthedocs.org/en/latest/button_widgets.html
from gi.repository import Gtk, GLib, GObject

class mpl:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
    from matplotlib.patches import Rectangle
    
from oceanoptics.defines import OceanOpticsError as _OOError

class DynamicPlotter(Gtk.Window):
    spectrometer = None
    connected = False
    get_dark  = False
    get_white = False
    waiting_for_spectra = False
    spectra_ready = False
    temperature = 0
    line = None

    def __init__(self, sample_interval_sec=1., oversample=16, raw=False, size=(640,480)):
        self.sample_interval_sec = float(sample_interval_sec)
        self.oversample = int(oversample)
        self.raw = bool(raw)
                
        self.lock_connect = threading.Lock()
        self.lock_get_spectra = threading.Lock()
        
        # Prepare Gtk window
        Gtk.Window.__init__(self, title='Ocean Optics Spectrometer - Colour Measurement')
        self.connect("destroy", lambda x : Gtk.main_quit())
        self.set_default_size(*size)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.add(vbox)

        # Add a horizontal box to hold buttons and text entries along the top row
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, False, False, 0)
        
        # Add a button to set the dark-point
        self.buttonDarkPoint = Gtk.Button("Set Dark Point")
        self.buttonDarkPoint.connect("clicked", self.set_dark_point, None)
        hbox.pack_start(self.buttonDarkPoint, True, True, 0)
        
        # Add a button to set the white-point
        self.buttonWhitePoint = Gtk.Button("Set White Point")
        self.buttonWhitePoint.connect("clicked", self.set_white_point, None)
        hbox.pack_start(self.buttonWhitePoint, True, True, 0)        
        
        # Add a small vertical box in the top-right corner to set model parameters
        vbox_labels = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        vbox_entries = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)        
        hbox.pack_start(vbox_labels, True, True, 0)
        hbox.pack_start(vbox_entries, True, True, 0)
        
        # Add an entry box for exposure time
        timeLabel = Gtk.Label("Exposure time (s):")
        timeLabel.set_halign(Gtk.Align.END)        
        vbox_labels.pack_start(timeLabel, True, True, 0)

        self.time_entry = Gtk.Entry()
        self.time_entry.set_text(str(self.sample_interval_sec))
        self.time_entry.connect("focus_out_event", self.time_entry_focus_out)        
        vbox_entries.pack_start(self.time_entry, True, True, 0)
        
        # Add an entry box for number of oversamples
        oversampleLabel = Gtk.Label("Average this many samples:")
        oversampleLabel.set_halign(Gtk.Align.END)        
        vbox_labels.pack_start(oversampleLabel, True, True, 0)

        self.oversample_entry = Gtk.Entry()
        self.oversample_entry.set_text(str(self.oversample))
        self.oversample_entry.connect("focus_out_event", self.oversample_entry_focus_out)        
        vbox_entries.pack_start(self.oversample_entry, True, True, 0)

        # Prepare the Matplotlib graph for the spectrum
        self.figure = mpl.Figure()
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.grid(True)
        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Relative Intensity")
        self.canvas = mpl.FigureCanvas(self.figure)

        # Add the graph to the GTK window
        vbox.pack_start(self.canvas, True, True, 0)
        self.canvas.show()
        
        # Add status bars
        hbox_status = Gtk.HBox(spacing=6)
        vbox.pack_start(hbox_status, False, False, 0)
        
        self.statusbar = Gtk.Statusbar()
        hbox_status.pack_start(self.statusbar, True, True, 0)
        self.status_context = self.statusbar.get_context_id("status")

        # Finished, so show the window
        self.show_all()
       
    def time_entry_focus_out(self, entry, event):
        text = entry.get_chars(0, -1)
        try:
            number = float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", text)[0])
        except IndexError:
            number = 0
            
        number = max(1e-3,number)
        number = min(10. ,number)        
        self.sample_interval_sec = number
        self.time_entry.set_text(str(number))        

        try:
            self.spectrometer.integration_time(time_sec=self.sample_interval_sec)        
        except (USBError, oceanoptics.defines.OceanOpticsError), e:
            print e

        return False

    def oversample_entry_focus_out(self, entry, event):
        text = entry.get_chars(0, -1)
        try:
            number = float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", text)[0])
        except IndexError:
            number = 0
            
        number = max(1,number)
        number = min(60./self.sample_interval_sec, number)
        number = int(number)
        
        self.oversample = number
        self.oversample_entry.set_text(str(number))        
        return False

    def connect_spectrometer(self):
        if not self.lock_connect.acquire(False):
            return 
            
        self.statusbar.push(self.status_context, "Searching for spectrometer...")
        
        try:
            self.spectrometer = oceanoptics.get_a_random_spectrometer()
            self.spectrometer.integration_time(time_sec=self.sample_interval_sec)
            self.wl = self.spectrometer.wavelengths()

        except (USBError, oceanoptics.defines.OceanOpticsError), e:
            print e
            print "Reconnect the OceanOptics spectrometer to the USB port..."
            self.statusbar.push(self.status_context, "Reconnect the OceanOptics spectrometer to the USB port...")
            if self.spectrometer!=None: 
                del self.spectrometer
            self.lock_connect.release()
            return 

        self.statusbar.push(self.status_context, "Connected to spectrometer.")
        
        self.wl_300nm = np.searchsorted(self.wl,300)
        self.wl_830nm = np.searchsorted(self.wl,830)
        self.deltawl = np.diff(self.wl) 

        # Load the tristimulus data
        self.tristim = np.loadtxt("CIE1931and1964.txt")
        self.wl_tristim = self.tristim[:,0]
        self.cie1931 = self.tristim[:,1:4]
        self.cie1964 = self.tristim[:,4:]
        
        # Construct an interpolation function of the tristimulus data
        self.interp_cie1964_x = interp1d(self.wl_tristim, self.cie1964[:,0], 'cubic')
        self.interp_cie1964_y = interp1d(self.wl_tristim, self.cie1964[:,1], 'cubic')
        self.interp_cie1964_z = interp1d(self.wl_tristim, self.cie1964[:,2], 'cubic')
        
        self.empty_buffer()
                        
        # Set the initial dark point
        if os.path.exists("dark_point.txt"):
            self.sp_dark = np.loadtxt("dark_point.txt")[:,1]
        else:
            self.sp_dark = np.zeros(self.wl.shape)

        # Set the initial white point
        if os.path.exists("white_point.txt"):
            self.scaleFactor, self.Xn, self.Yn, self.Zn = np.loadtxt("white_point.txt")
        else:
            self.scaleFactor, self.Xn, self.Yn, self.Zn = 0.01, 1., 1., 1.

    
        # Plot the initial data
        if self.line==None:
            wl = self.wl[self.wl_300nm:self.wl_830nm]
            self.line,   = self.ax.plot(wl, np.zeros(len(wl)),c='black')
            self.rline, = self.ax.plot(wl, 0.5*self.interp_cie1964_x(wl), c='r')
            self.gline, = self.ax.plot(wl, 0.5*self.interp_cie1964_y(wl), c='g')
            self.bline, = self.ax.plot(wl, 0.5*self.interp_cie1964_z(wl), c='b')

            self.ax.set_ylim(bottom=0.0,top=1.2) 
            self.ax.set_xlim(left=350, right=830)
    
            # Display a text label of the colour coordinate
            self.text = self.ax.text(
                0.5, 0.8,'L*=%.2f\na*=%.2f\nb*=%.2f\n' % (0,0,0),
                horizontalalignment='center',
                verticalalignment='center',
                fontweight='bold',
                transform = self.ax.transAxes)

        self.connected = True
        
    def cie1976(self,r):
        if r>(24./116.)**3:
            return r**0.3
        else:
            return 841./108.*r  + 16./116.

    def set_white_point(self, widget, data=None):
        self.empty_buffer()
        self.get_white = True
            
    def set_dark_point(self, widget, data=None):
        self.empty_buffer()
        self.get_dark = True
        self.sp_dark = np.zeros(self.wl.shape)
	print "Get dark"

    def update_plot(self):
        if self.get_dark: return

        # Redraw the spectrum graph
        sp = self.average_spectra[self.wl_300nm:self.wl_830nm]
        scale = 1./max(1e-5,np.max(sp[self.wl_300nm:self.wl_830nm]))
        self.line.set_ydata(scale*sp)
        self.canvas.draw()

    def update_colour(self):
        if self.get_dark: return

        # Calculate the colour in XYZ space
        dw = self.deltawl[self.wl_300nm:self.wl_830nm]
        sp = self.average_spectra[self.wl_300nm:self.wl_830nm]
        X = self.scaleFactor*np.sum(self.interp_cie1964_x(self.wl[self.wl_300nm:self.wl_830nm])*sp*dw)
        Y = self.scaleFactor*np.sum(self.interp_cie1964_y(self.wl[self.wl_300nm:self.wl_830nm])*sp*dw)
        Z = self.scaleFactor*np.sum(self.interp_cie1964_z(self.wl[self.wl_300nm:self.wl_830nm])*sp*dw)
        
        # Relative tri-stimulus values
        rX = X/self.Xn
        rY = Y/self.Yn
        rZ = Z/self.Zn
        
        # Mapping for CIE1976 L,a*,b* coordinates
        fX = self.cie1976(rX)
        fY = self.cie1976(rY)        
        fZ = self.cie1976(rZ)
        L = 116.*fY - 16.
        a = 500.*(fX-fY)
        b = 200.*(fY-fZ)
        
        self.Lab = [L,a,b]
        
    def update_temperature(self):
        # Ask the spectrometer how hot it is.
        try:
            self.temperature = self.spectrometer._read_pcb_temperature()
        except _OOError:
            pass
        
    def empty_buffer(self):
        self.n_sample = 0
        self.sp = np.zeros( (len(self.wl), self.oversample) )
        self.buffer_mask = [False]*self.oversample

    def get_spectra(self):
        if not self.lock_get_spectra.acquire(False):
            return

        self.waiting_for_spectra = True
        
        #Try to read the next sample
        try:
            sample  = np.array(self.spectrometer.intensities(raw=self.raw))
            sample -= self.sp_dark            
                      
        except (USBError, oceanoptics.defines.OceanOpticsError), e:
            print e
            print "Reconnect the OceanOptics spectrometer to the USB port..."
            self.statusbar.push(self.status_context, "Reconnect the OceanOptics spectrometer to the USB port...")
            if self.spectrometer!=None: 
                del self.spectrometer
            self.connected = False
            self.waiting_for_spectra = False            
            self.lock_connect.release()
            self.lock_get_spectra.release()            
            return 
                       

        if self.connected:
            self.n_sample += 1
            if self.n_sample >= self.oversample: 
                self.n_sample=0

            self.sp[:,self.n_sample] = sample
            self.buffer_mask[self.n_sample] = True
            
            good_sp = np.array([self.sp[:,i] for i in xrange(len(self.buffer_mask)) if self.buffer_mask[i]]).T
            if len(good_sp.shape)>1:
                self.max_spectra = np.max(good_sp, axis=1)
                self.average_spectra = np.median(good_sp, axis=1)
            else:
                self.max_spectra     = sample
                self.average_spectra = sample
                
            self.max_spectra[self.max_spectra<1.e-10] = 1.e-10
            self.average_spectra[self.average_spectra<1.e-10] = 1.e-10
                        
            self.waiting_for_spectra = False
            self.spectra_ready = True

        self.lock_get_spectra.release()            
        
    def tick(self):
        if self.spectra_ready:
            self.spectra_ready = False
            # Spectra has been received so now process it.
            if self.get_dark:
                if np.all(self.buffer_mask):
                    self.get_dark = False
                    self.sp_dark = self.max_spectra
                    np.savetxt("dark_point.txt", zip(self.wl,self.sp_dark))
                else:
                    self.text.set_text('Setting dark-point: %d/%d\n\n' % ((self.n_sample+1), self.oversample))
                    self.statusbar.push(self.status_context,'Setting dark-point: %d/%d\n\n' % ((self.n_sample+1), self.oversample))

            elif self.get_white:
                if self.n_sample==0:
                    self.get_white = False
                    dw = self.deltawl[self.wl_300nm:self.wl_830nm]
                    sp = self.average_spectra[self.wl_300nm:self.wl_830nm]
                    self.scaleFactor = 100./np.sum(self.interp_cie1964_y(self.wl[self.wl_300nm:self.wl_830nm])*sp*dw)        
                    self.Xn = self.scaleFactor*np.sum(self.interp_cie1964_x(self.wl[self.wl_300nm:self.wl_830nm])*sp*dw)
                    self.Yn = self.scaleFactor*np.sum(self.interp_cie1964_y(self.wl[self.wl_300nm:self.wl_830nm])*sp*dw)
                    self.Zn = self.scaleFactor*np.sum(self.interp_cie1964_z(self.wl[self.wl_300nm:self.wl_830nm])*sp*dw)
                    np.savetxt("white_point.txt", [self.scaleFactor, self.Xn, self.Yn, self.Zn])
                else:
                    self.text.set_text('Setting white-point: %d/%d\n\n' % ((self.n_sample+1), self.oversample))

            else:
                self.update_colour()
                self.text.set_text('L*=%.2f\na*=%.2f\nb*=%.2f\n' % (self.Lab[0],self.Lab[1],self.Lab[2]))
                oversample_time = self.sample_interval_sec * self.oversample
                self.statusbar.push(self.status_context, "Temperature=%.1fC   The delay due to averaging is %ds" % (self.temperature,oversample_time))
                
            
            self.update_plot()
            self.update_temperature()            
        return True

    def tick_spectrometer(self):
        if not self.connected:
            # Reconnect to the spectrometer
            t1 = threading.Thread(target=self.connect_spectrometer())
            t1.start()
            
        elif not self.waiting_for_spectra:
            # Request the next spectra from the spectrometer
            t1 = threading.Thread(target=self.get_spectra)
            t1.start()
                        
        return True

    def run(self):
        GObject.threads_init()
        GObject.idle_add(self.tick_spectrometer)
        GObject.idle_add(self.tick)
        Gtk.main()
        
if __name__ == '__main__':
    m = DynamicPlotter(sample_interval_sec=1.0)
    m.run()

