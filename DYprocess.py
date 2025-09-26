import uproot as up
import awkward as aw
import matplotlib.pyplot as plt
import numpy as np

tree = up.open('/u/user/yeobi97/SE_UserHome/jeontampeu/DY_genlevel.root')['LHEF']

pt=tree['Particle.PT'].array()
eta=tree['Particle.Eta'].array()
phi=tree['Particle.Phi'].array()
status=tree['Particle.Status'].array()
pid=tree['Particle.PID'].array()



mask_e = (status == 1) & (abs(pid) == 11)
mask_mu = (status ==1) & (abs(pid) == 13)

PT_e = pt[mask_e]
PT_mu = pt[mask_mu]

ETA_e = eta[mask_e]
ETA_mu = eta[mask_mu]

PHI_e = phi[mask_e]
PHI_mu = phi[mask_mu]

PT_e_flat = aw.flatten(PT_e)
ETA_e_flat = aw.flatten(ETA_e)
PHI_e_flat = aw.flatten(PHI_e)


plt.figure(figsize=(8,6))
plt.hist(PT_e_flat, bins=100, range=(0,100), color = 'blue')
plt.title('genlevel DY PT_e')
plt.xlabel('PT_e [Gev]')
plt.ylabel('Entries')
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('genlevel DY PT_e.png',dpi=300)
plt.close()

plt.figure(figsize=(8,6))
plt.hist(ETA_e_flat, bins=100, range=(-6,6), color = 'red')
plt.title('genlevel DY ETA_e')
plt.xlabel('ETA_e')
plt.ylabel('Entries')
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('genlevel DY ETA_e.png',dpi=300)
plt.close()

plt.figure(figsize=(8,6))
plt.hist(ETA_e_flat, bins=100, range=(-np.pi,np.pi), color = 'green')
plt.title('genlevel DY PHI_e')
plt.xlabel('PHI_e [rad]')
plt.ylabel('Entries')
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('genlevel DY PHI_e.png',dpi=300)
plt.close()