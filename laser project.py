'''
Input laser information: 
    Wavelength: lam (nm)
    Exposure time: t (s)
    Beam divergence: bd (radians)

Continous wave lasers:
    Radiant power: rp (W)
    Spectral reflectance: sr (unitless)

Repetitive pulse lasers:
    Pulse width: pw (s)
    Energy per pulse: epp (J)
    Frequency: f (Hz)
    
Calculated variables for continous wave:
    Nominal ocular hazard distance: NOHD (m)
    Nominal Hazard Zone: NHZ (m)
    
Calculated variables for repetitive pulse:    
    Average power: ap (W)
    Number of pulses contained within an exposure duration: N (unitless)
    
Calculated variables:
    Diameter of limiting apeture: df (m)
    Maximum permissible exposure: MPE (W / m^-2)
    Irradiance: e (W / m^2)
    Optical density: od (unitless)
    
'''  
import math

#variable inputs:
mode = input('Enter c for continuous wavelength, r for repetitive pulse or h for help: ')

#if mode != ('c' or 'r' or 'h'):
#   raise Exception ('Error, you must choose between c, r or h')

if (mode == 'c') or (mode == 'r') or (mode == 'h'):
    pass
else:
    raise TypeError('Error, you must choose between c, r or h')

if mode == 'h':
    raise Exception('The minimum required inputs for a continuous wavelength laser is wavelentgh and radiant power. The rest of the variables could be left blank if unknown. For a repetitive pulse laser, the minimum required variables are wavelength, energy per pulse, frequency and pulse width.')

lam = float(input("Enter wavelength in nanometers: "))

if lam < 180:
    raise Exception('Error, the wavelength must be greater than or equal to 180 nm')   
elif 180 <= lam < 400:
    td = 100 #default time, s
elif 400 <= lam < 700:
    td = 0.25
elif 700 <= lam < 1e6:
    td = 10
elif 1e6 < lam:
    raise Exception('Error, the wavelength must be less than or equal to 1000000 nm')

t = float(input("Enter exposure time in seconds or leave blank: ") or td)

#diameter of limiting aperture:
if 180 <= lam < 400:
    df = 0.001
elif 400 <= lam < 1400:
    df = 0.007
elif 1400 <= lam < 1e5:
    if t <= 0.35:
        df = 0.001
    elif 0.35 <= t < 10:
        df = 0.0015 * pow(t,(3/8))
    elif 10 <= t:
        df = 0.0035
elif 1e5 <= lam < 1e6:
    df = 0.011

la = float(input("Enter diameter of limiting aperture in meters or leave blank: ") or df)
print("Diameter of limiting aperture is {0:.3f} {1}".format(la, " m"))

bd = float(input("Enter beam divergence in radians or leave blank: ") or 0.001)

if mode == 'c': #continuous wave inputs
    rp = float(input("Enter radiant power in Watts: "))
    sr = float(input("Enter spectral reflectance or leave blank: ") or 0.5)
    reflectance = input('Reflectance? Enter d for diffuse or s for specular or leave blank: ') or 's'
elif mode == 'r': #repetitive pulse inputs
    pw = float(input("Enter pulse width in seconds: "))
    epp = float(input("Enter energy per pulse in Joules: "))
    f = float(input("Enter frequency of pulses in Hertz: "))
    ap = epp * f #average power, W

#set variables:
bdmin = 0.0015 #minumum beam divergence, radians
bdmax = 0.1 #maximum beam divergence, radians
df = 0 #diameter of limiting aperture, meters
t1 = 0 #time correction factor 1
t2 = 0 #time correction factor 2
c3 = 0 #correction factor 3
c4 = 0 # correction factor 4
c6 = 0 #correction factor 6
c7 = 0 #correction factor 7
MPE = 0 #maximum permissible exposure, watts per square meter
e = 0 #irradiance, watts per square meter

#correction factors below

if 302.5 <= lam < 315:
    t1 = 1e-15 * pow(10,0.8*(lam-295))

if bd < bdmin:
    t2 = 10
elif bdmin <= bd <= bdmax:
    t2 = 10 * pow(10,(bd-bdmin) / 98.5)
elif bdmax < bd:
    t2 = 100
    
if 400 <= lam < 450:
    c3 = 1
elif 450 <= lam < 600:
    c3 = pow(10, 0.02*(lam-450))
    
if 700 <= lam < 1050:
    c4 = pow(10,0.002*(lam - 700))
elif lam > 1050:
    c4 = 5

if bd <= bdmin:
    c6 = 1
elif bdmin < bd <= bdmax:
    c6 = bd / bdmin
elif bdmax < bd:
    c6 = bdmax / bdmin

if 700 <= lam < 1150:
    c7 = 1
elif 1150 <= lam < 1200:
    c7 = pow(10,0.018*(lam-1150))
elif 1200 <= lam < 1400:
    c7 = 8

#MPE below

if t < 1e-13:
    raise Exception('Error, time must be greater than or equal to 1 x 10^-13 s')
elif 180 <= lam < 400 and 1e-13 <= t < 1e-9:
    MPE = 3e10
elif 180 <= lam < 302.5 and 1e-9 <= t < 3e4:
    MPEH = 30 
    MPE = MPEH / t
elif 302.5 <= lam < 315 and 1e-9 <= t < 10:
        if t <= t1:
            MPEH = 5.6 *pow(t,0.25) * 1e3
            MPE = MPEH / t
        elif t > t1:
            MPEH = pow(10, 0.2*(lam-295))
            MPE = MPEH / t
elif 302.5 <= lam < 315 and 10 <= t < 3e4:
    MPEH = pow(10,0.2*(lam-295))
    MPE = MPEH / t
elif 315 <= lam < 400 and 1e-9 <= t < 10:
    MPEH = 5.6 * 1e-3 * pow(t,0.25)
    MPE = MPEH / t
elif 315 <= lam < 400 and 10 <= t < 1e3:
    MPE = 1e4 / t
elif 315 <= lam < 400 and 1e3 <= t < 3e4:
    MPE = 10
elif 400 <= lam < 700 and 1e-13 <= t < 1e-11:
    MPEH = 1.5 * c6 * 1e-4
    MPE = MPEH / t
elif 400 <= lam < 700 and 1e-11 <= t < 1e-9:
    MPEH = 2.7 * 1e4 * pow(t,0.75) * c6
    MPE = MPEH / t
elif 400 <= lam < 700 and 1e-9 <= t < 1.8e-5:
    MPEH = 5e-3 * c6
    MPE = MPEH / t
elif 400 <= lam < 700 and 1.8e-5 <= t < 10:
    MPEH = 18 * pow(t,0.75) * c6
    MPE = MPEH / t
elif 400 <= lam < 484 and 10 <= t < 3e4:
    raise Exception('This combination of wavelength and exposure time is a retinal photochemical hazard')
elif 484 <= lam < 600 and 10 <= t < 100:
    MPEH = 100 * c3 #gammap = 11 mrad
    MPE = MPEH / t
elif 484 <= lam < 600 and 100 <= t < 1e4:
    MPE = c3 #gammap = 1.1*(t^0.5) mrad
elif 484 <= lam < 600 and 1e4 <= t < 3e4:
    MPE = c3 #gammap = 110 mrad
elif 600 <= lam < 700 and 10 <= t < 3e4:
    if bd <= bdmin:
        MPE = 10
    elif bd > bdmin and t <= t2:
        MPEH = 18 * pow(t,0.75) * c6
        MPE = MPEH / t
    elif bd > bdmin and t > t2:
        MPE = 18 * c6 * pow(t2, -0.25)
elif 700 <= lam < 1050 and 1e-13 <= t < 1e-11:
    MPEH = 1.5e-4 * c4 * c6
    MPE = MPEH / t
elif 700 <= lam < 1050 and 1e-11 <= t < 1e-9:
    MPEH = 2.7e4 * c4 * c6 * pow(t,0.75)
    MPE = MPEH / t
elif 700 <= lam < 1050 and 1e-9 <= t < 1.8e-5:
    MPEH = 5e-3 * c4 * c6
    MPE = MPEH / t
elif 700 <= lam < 1050 and 1.8e-5 <= t < 10:
    MPEH = 18 * pow(t,0.75) * c4 * c6
    MPE = MPEH / t
elif 700 <= lam < 1400 and 10 <= t < 3e4:
    if bd <= bdmin:
        MPE = 10 * c4 * c7
    elif bd > bdmin and t <= t2:
        MPEH = 18 * c4 * c6 * c7 * pow(t,0.75)
        MPE = MPEH / t
    elif bd > bdmin and t > t2:
        MPE = 18 * c4 * c6 * c7 * pow(t2, -0.25)
elif 1050 <= lam < 1400 and 1e-13 <= t < 1e-11:
    MPEH = 1.5e-3 * c6 * c7
    MPE = MPEH / t
elif 1050 <= lam < 1400 and 1e-11 <= t < 1e-9:
    MPEH = 2.7e5 * pow(t,0.75) * c6 * c7
    MPE = MPEH / t
elif 1050 <= lam < 1400 and 1e-9 <= t < 5e-5:
    MPEH = 5e-2 * c6 * c7
    MPE = MPEH / t
elif 1050 <= lam < 1400 and 5e-5 <= t < 10:
    MPEH = 90 * pow(t,0.75) * c6 * c7
    MPE = MPEH / t
elif 1400 <= lam < 1500 and 1e-13 <= t < 1e-9:
    MPE = 1e12
elif 1400 <= lam < 1500 and 1e-9 <= t < 1e-3:
    MPEH = 1e3
    MPE = MPEH / t
elif 1400 <= lam < 1500 and 1e-3 <= t < 10:
    MPEH = 5600 * pow(t,0.75)
    MPE = MPEH / t
elif 1400 <= lam < 1e6 and 10 <= t < 3e4:
    MPE = 1000
elif 1500 <= lam < 1800 and 1e-13 <= t < 1e-9:
    MPE = 1e13
elif 1500 <= lam < 1800 and 1e-9 <= t < 10:
    MPEH = 1e4
    MPE = MPEH / t
elif 1800 <= lam < 2600 and 1e-13 <= t < 1e-9:
    MPE = 1e12
elif 1800 <= lam < 2600 and 1e-9 <= t < 1e-3:
    MPEH = 1e3
    MPE = MPEH / t
elif 1800 <= lam < 2600 and 1e-3 <= t < 10:
    MPEH = 5600 * pow(t,0.75)
    MPE = MPEH / t
elif 2600 <= lam < 1e6 and 1e-13 <= t < 1e-9:
    MPE = 1e11
elif 2600 <= lam < 1e6 and 1e-9 <= t < 1e-7:
    MPEH = 100
    MPE = MPEH / t
elif 2600 <= lam < 1e6 and 1e-7 <= t < 1e-10:
    MPEH = 5600 * pow(t,0.75)
    MPE = MPEH / t
elif 3e4 < t:
    raise Exception('Error, the time must be less than 30,000 s')

if 600 <= lam < 1400 and 10 <= t < 3e4:
    print('This combination of wavelength and exposure time is a retinal thermal hazard')


#calculations below

if mode == 'c':
    
    print("MPE is {0:.3f} {1}".format(MPE, "W / m^2"))
    
    def NOHD(bd, MPE, rp):
        NOHD = 0 
        NOHD = (1 / bd)*pow(((1.27*rp)/MPE),0.5) 
        rounded = round(NOHD, 1)
        return rounded
    print(f"NOHD is {NOHD(bd, MPE, rp)} m ")
    
    def NHZd(sr, rp, bd, MPE):
        NHZd = 0 
        NHZd = pow(((sr*rp*math.cos(bd))/(math.pi*MPE)),0.5) / 100
        return NHZd
    #print("NHZ is", NHZd(sr, rp, bd, MPE))
    
    def NHZs(sr, rp, bd, MPE):
        NHZs = 0 
        NHZs = (1/bd)*pow(((1.27*sr*rp)/MPE),0.5) 
        return NHZs
    #print("NHZ is", NHZs(sr, rp, bd, MPE))
        
    #NHZ = 0 #nominal hazard zone
    
    if reflectance == str('d'):
        NHZ = NHZd(sr, rp, bd, MPE)
        print ("NHZ is {0:.5f}{1}".format(NHZ, " m"))
    elif reflectance == str('s'):
        NHZ = NHZs(sr, rp, bd, MPE)
        print ("NHZ is {0:.1f}{1}".format(NHZ, " m"))
        
    e = rp / (math.pi*pow((la/2),2))
    print(f"Irradiance is {e:.0f} W / m^2 ")
    
    od = 0 #optical density

    def od(e, MPE):
        od = 0
        od = math.log10 (e / MPE)
        rounded = round(od, 2)
        return rounded
    
    if od(e, MPE) < 0:
        print ('Optical density is 0.0')
    elif 0 <= od(e, MPE):
        print(f"Optical density is {od(e, MPE)} ")
    
elif mode == 'r':
    N = t * f #number of pulses contained within the applicable duration
    print(f"Number of pulses contained within the applicable duration is {N} ") 
    
    if 400 <= lam < 1050 and pw < 0.25:
        c5 = pow(N,-0.25)
    elif lam < 400 or 1050 <= lam or 0.25 <= pw:
        c5 = 1
    
    print(f"Average power is {ap:.3f} W ")    
        
    
    e = ap / (math.pi*pow((la/2),2))
    print(f"Irradiance is {e:.0f} W / m^2 ")
    
    NMPE = MPE * c5
    
    if NMPE < MPE:
        MPE2 = NMPE
        print("MPE is {0:.3f} {1}".format(MPE2, "W / m^2"))
    elif MPE <= NMPE:
        MPE2 = MPE
        print("MPE is {0:.3f} {1}".format(MPE2, "W / m^2"))
        
    od = 0 #optical density

    def od(e, MPE2):
        od = 0
        od = math.log10 (e / MPE2)
        rounded = round(od, 2)
        return rounded
    
    if od(e, MPE2) < 0:
        print ('Optical density is 0.0')
    elif 0 <= od(e, MPE2):
        print(f"Optical density is {od(e, MPE)} ")






