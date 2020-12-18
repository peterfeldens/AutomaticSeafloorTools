#Import modules and define functions for parameter calculations
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calc_tau_0(Ustar, rho_water = 1.03):
    rho_water = rho_water * 1000
    tau_0 = rho_water * Ustar**2   
    return tau_0

def calc_s(rho_material,rho_water):
    return rho_material / rho_water

def calc_Ustar(U,h,d):
    d = d/1000
    exponent = 1./7.
    Ustar_U = 1./7. * (d/h)**exponent
    Ustar = Ustar_U * U
    return Ustar

def calc_shields(tau_0, g, rho_water, s, d):
    rho_water = rho_water * 1000
    d = d/1000
    shields = tau_0 / (g * rho_water * (s -1) * d)
    return shields

def calc_shields_cr(Dstar):
    shields_cr = (0.3 / ( 1. + 1.2*Dstar)) + 0.055 * (1 - np.exp(-0.02*Dstar))
    return shields_cr

def calc_tau_cr(shields_cr, rho_water, rho , d):
    g=9.81
    rho_water = rho_water * 1000
    rho = rho * 1000
    d = d/1000
    tau_cr = shields_cr * g * (rho - rho_water) * d
    return tau_cr

def  calc_Dstar(d,g,s,v=1.36 * 10**-6):
    d = d/1000
    return d * (g*(s-1) / v**2.)**(1./3.)

def calc_bedload_nielsen(shields, shields_cr):
    return 12. * shields**0.5 * (shields - shields_cr)

def calc_qb(bedload,g,s,d):
    d=d/1000
    qb = bedload* (g*(s-1)*d**3.)**0.5
    return qb

def calc_settling_velocity(v,d,Dstar):
    d=d/1000
    ws = v/d * ((10.36**2 + 1.049*Dstar**3)**0.5 -10.36)
    return ws



##test case sand to reproduce numbers from soulsby 1997 example
## qb should be ~4.3*10**-5
g = 9.82 #m/s^2
U = 1.0 #m/s depth averaged current speed
h = 5.0 #m
d = 1.0 #mm
rho_quartz = 2.65 #g/cm^3
rho_water = 1.03 #g/cm^3
s =  calc_s(rho_quartz,rho_water) #density ratio

# We assume a flat bed with no bedforms and calculate bed shear stress
Ustar = calc_Ustar(U,h,d)
print(Ustar)
tau_0 = calc_tau_0(Ustar, rho_water)
print(tau_0)
shields = calc_shields(tau_0,g,rho_water,s,d)
print(shields)
Dstar = calc_Dstar(d,g,s)
print(Dstar)
shields_cr = calc_shields_cr(Dstar)
print(shields_cr)


# Calculation
g = 9.82 #m/s^2
h = 3.5 #m
rho_water = 1.02 #g/cm^3
rho_sand = 2.65 #g/cm^3

U_array = np.arange(0.01,1,0.01) #m/s depth averaged current speed
d_array_plastic = [0.063,0.1, 0.2,0.3,0.4,0.5,0.63,1.0,1.5,2.0, 3.0, 4.0, 5.0] #mm
rho_array_plastic = [1.2,1.6] #g/cm^3
d_array_sand = [0.01, 0.016, 0.03, 0.05, 0.063,0.1, 0.2,0.3,0.4,0.5,0.63,1.0,1.5,2.0] #mm

def calculate_parameters(U,h,d,rho_water, rho_material):    
    s=calc_s(rho_material,rho_water)
    Ustar = calc_Ustar(U,h,d)
    tau_0 = calc_tau_0(Ustar, rho_water)
    shields = calc_shields(tau_0,g,rho_water,s,d)
    Dstar = calc_Dstar(d,g,s)
    shields_cr = calc_shields_cr(Dstar)
    bedload = calc_bedload_nielsen(shields, shields_cr)
    qb = calc_qb(bedload,g,s,d)
    tau_cr = calc_tau_cr(shields_cr, rho_water, rho_material, d)

    return shields, shields_cr, bedload, qb, Dstar, tau_0, tau_cr


results = []
# Calculate for plastic
for U in U_array:
    for d in d_array_plastic:
        for rho in rho_array_plastic:
            shields, shields_cr, bedload, qb, Dstar, tau_0, tau_cr = calculate_parameters(U, h, d, rho_water, rho)
            results.append(['Plastic',shields_cr, shields, bedload,qb,U,rho,d, Dstar, tau_0, tau_cr])
            
# Calculate for sand
for U in U_array:
    for d in d_array_sand:
        shields, shields_cr, bedload_result, qb_result, Dstar, tau_0, tau_cr = calculate_parameters(U, h, d, rho_water, rho_sand)
        results.append(['Sand',shields_cr, shields, bedload,qb,U,rho_sand,d, Dstar, tau_0, tau_cr])

df = pd.DataFrame(results, columns=['Type','Shields_cr', 'Shields','Bedload','qb','U','rho','d','Dstar','tau_0', 'tau_cr'])

df['PHI'] = -np.log2(df.d)

#Remove entries where shields < shields_cr : No transport

df = df[(df['Shields'] > df['Shields_cr'])]

df.to_csv('results.txt')



#Plot
plt.figure(figsize=(5,4))
#plt.style.use('bmh')
plt.scatter(df.d, df.tau_cr, c=df.rho)
plt.colorbar()
plt.xlim((0.005,6))
plt.ylim((0.01,3))
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Quartz / plastic grain size [mm]')
plt.ylabel('Thresold bed shear stress [Nm^-2]')
plt.savefig('threshold.svg', format='svg', dpi=1200)
plt.show()


bedload = calc_bedload_nielsen(shields, shields_cr)
qb = calc_qb(bedload,g,s,d)
print(qb)