import uproot as up
import numpy as np
import awkward as ak
import matplotlib.pyplot as plt
import vector
import glob

vector.register_awkward()

path = "/u/user/ab0633/Original"

the_list = glob.glob(path + '/*.root')


# print(the_list)

# pt_e_arrays = []

# for sample in the_list :
#     with up.open(sample) as file :
#         tree = file['Delphes;1']
        
#         pt_e=tree['Electron.PT'].array()
#         eta_e=tree['Electron.Eta'].array()
#         phi_e=tree['Electron.Phi'].array()
#         charge_e=tree['Electron.Charge'].array()
        
#         pt_mu=tree['MuonTight.PT'].array()
#         eta_mu=tree['MuonTight.Eta'].array()
#         phi_mu=tree['MuonTight.Phi'].array()
#         charge_mu=tree['MuonTight.Charge'].array()

#         pt_gam=tree['PhotonTight.PT'].array()
#         eta_gam=tree['PhotonTight.Eta'].array()
#         phi_gam=tree['PhotonTight.Phi'].array()

#         pt_MET = tree['PuppiMissingET.MET'].array()
#         phi_MET = tree['PuppiMissingET.Phi'].array()

#         pt_j = tree['Jet.PT'].array()
#         eta_j = tree['Jet.Eta'].array()
#         phi_j = tree['Jet.Phi'].array()
#         BTag_j = tree['Jet.BTag'].array()
        

#!!!ak.zip 공부 및 도전!!! 

branches = [
    "Electron.PT", "Electron.Eta", "Electron.Phi", "Electron.Charge",
    "MuonTight.PT", "MuonTight.Eta", "MuonTight.Phi", "MuonTight.Charge",
    "PhotonTight.PT", "PhotonTight.Eta", "PhotonTight.Phi",
    "PuppiMissingET.MET", "PuppiMissingET.Phi",
    "Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.BTag",
]

all_events_data = []

for sample in the_list:
    with up.open(sample) as file:
        tree = file['Delphes;1']
        all_events_data.append(tree.arrays(branches))



events = ak.concatenate(all_events_data)

#zip 으로 mass 만드는 방법 익히기.


ELECTRON_MASS = 0.000511

el = ak.zip({
    "pt": events["Electron.PT"],
    "eta": events["Electron.Eta"],
    "phi": events["Electron.Phi"],
    "charge": events["Electron.Charge"],
    "mass": ak.full_like(events["Electron.PT"], ELECTRON_MASS)
}, with_name="Momentum4D")

MUON_MASS = 0.1057

mu = ak.zip({
    "pt": events["MuonTight.PT"],
    "eta": events["MuonTight.Eta"],
    "phi": events["MuonTight.Phi"],
    "charge": events["MuonTight.Charge"],
    "mass": ak.full_like(events["MuonTight.PT"], MUON_MASS)
}, with_name="Momentum4D")

ph = ak.zip({
    "pt": events["PhotonTight.PT"],
    "eta": events["PhotonTight.Eta"],
    "phi": events["PhotonTight.Phi"],
}, with_name="Momentum4D")

jet = ak.zip({
    "pt": events["Jet.PT"],
    "eta": events["Jet.Eta"],
    "phi": events["Jet.Phi"],
    "btag": events["Jet.BTag"],
}, with_name="Momentum4D")

met = ak.zip({
    "pt": events["PuppiMissingET.MET"],
    "phi": events["PuppiMissingET.Phi"],
}, with_name="Momentum4D")
        
# 디버깅 시도 - 문제 없음
    
# check = 10

# for i in range(check):
#     n_e = len(el[i])
#     n_mu = len(mu[i])
#     n_ph = len(ph[i])
    
#     print(f"--- 이벤트 {i} ---")
#     print(f"전자 수: {n_e}, PT: {el[i].pt if n_e > 0 else '없음'}")
#     print(f"뮤온 수: {n_mu}, PT: {mu[i].pt if n_mu > 0 else '없음'}")
#     print(f"포톤 수: {n_ph}, PT: {ph[i].pt if n_ph > 0 else '없음'}\n")

# object selection

el_mask = (el.pt > 15) \
        & ((abs(el.eta) < 1.442) | (abs(el.eta) > 1.566)) & (abs(el.eta) < 2.5)

mu_mask = (mu.pt > 15) \
        & (abs(mu.eta)<2.5)

ph_mask = (ph.pt > 20) \
        & ((abs(ph.eta) < 1.442) | (abs(ph.eta) > 1.566)) & (abs(ph.eta) < 2.5)

jet_mask = (jet.pt > 30) \
         & (abs(jet.eta)<2.5)

sel_el = el[el_mask]
sel_mu = mu[mu_mask]
sel_ph = ph[ph_mask]
sel_jet = jet[jet_mask]


# select 후 variable distribution 확인

# plot_configs = [
#     (ak.flatten(sel_el.pt),      "Selected Electron pT", 100,  (0, 200), "pT [GeV]", "selected_electron_pt.png"),
#     (ak.flatten(sel_mu.pt),      "Selected Muon pT",     100,  (0, 200), "pT [GeV]", "selected_muon_pt.png"),
#     (ak.flatten(sel_ph.pt),      "Selected Photon pT",   100,  (0, 200), "pT [GeV]", "selected_photon_pt.png"),
#     (ak.flatten(sel_el.eta),     "Selected Electron Eta", 100, (-4, 4),   "Eta",      "selected_electron_eta.png"),
#     (ak.flatten(sel_mu.eta),     "Selected Muon Eta",    100,  (-4, 4),   "Eta",      "selected_muon_eta.png"),
#     (ak.flatten(sel_ph.eta),     "Selected Photon Eta",    100,  (-4, 4),   "Eta",      "selected_photon_eta.png")
# ]

# for data, title, bins, plot_range, xlabel, filename in plot_configs:
#     plt.figure(figsize=(8, 6))
#     plt.hist(data, bins=bins, range=plot_range, histtype='step', lw=2)
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel('Number of Objects')
#     plt.grid(True, linestyle='--', alpha=0.5)
#     plt.savefig(filename, dpi=300)
#     plt.close()



# event selection

#bjet veto
wp_m_bit = 1 << 1
is_bjet_m = (sel_jet.btag & wp_m_bit) > 0
n_bjets = ak.sum(is_bjet_m, axis =1)
# axis = 1 은 이벤트 안에서 
# axis = 0 은 여러이벤트의 같은 번째끼리
bjet_veto_mask = (n_bjets == 0)

# lepton

lep = ak.concatenate([sel_el, sel_mu], axis=1)
n_lep_mask = (ak.num(lep) == 3)


# OSSF
#fields 옵션 name 부여하는 방법 익히기.

ee_pairs = ak.combinations(sel_el, 2, fields=["i0", "i1"])
os_e_mask = (ee_pairs.i0.charge * ee_pairs.i1.charge) == -1
os_ee_pairs = ee_pairs[os_e_mask]

mumu_pairs = ak.combinations(sel_mu, 2, fields=["i0", "i1"])
os_mu_mask = (mumu_pairs.i0.charge * mumu_pairs.i1.charge) == -1
os_mumu_pairs = mumu_pairs[os_mu_mask]

ossf_pairs = ak.concatenate([os_ee_pairs, os_mumu_pairs], axis=1)

ossf_mask = (ak.num(ossf_pairs, axis=1) >= 1)

# Z window

z_candidates_p4 = ossf_pairs.i0 + ossf_pairs.i1
z_mass = z_candidates_p4.mass
Z_MASS = 91.1876
z_window = abs(z_mass - Z_MASS) < 15
z_mass_mask = ak.any(z_window, axis=1)

# MET 
# firsts 하는 의미 생각하기.
met_mask = (ak.firsts(met.pt) > 30)


event_mask = (n_lep_mask & ossf_mask & z_mass_mask & bjet_veto_mask & met_mask )

# !!주의!! (틀렸던 점)
# 수 비교는 길이를 비교 해야하니까 ak.num 을 써야함.
# 리스트 자체를 합하는건 ak.sum 이 아니라 ak.concatenate 를 사용해야함.

print(f'이벤트 컷 전 이벤트 수 : {len(events)}')


events = events[event_mask]
sel_el = sel_el[event_mask]
sel_mu = sel_mu[event_mask]
sel_ph = sel_ph[event_mask]
sel_jet = sel_jet[event_mask]
met = met[event_mask]

print(f'이벤트 컷 후 이벤트 수 : {len(events)}')

plot_configs = [
    (ak.flatten(sel_el.pt),      "e_Selected Electron pT", 100,  (0, 200), "pT [GeV]", "selected_electron_pt.png"),
    (ak.flatten(sel_mu.pt),      "e_Selected Muon pT",     100,  (0, 200), "pT [GeV]", "selected_muon_pt.png"),
    (ak.flatten(sel_ph.pt),      "e_Selected Photon pT",   100,  (0, 200), "pT [GeV]", "selected_photon_pt.png"),
    (ak.flatten(sel_el.eta),     "e_Selected Electron Eta", 100, (-4, 4),   "Eta",      "selected_electron_eta.png"),
    (ak.flatten(sel_mu.eta),     "e_Selected Muon Eta",    100,  (-4, 4),   "Eta",      "selected_muon_eta.png"),
    (ak.flatten(sel_ph.eta),     "e_Selected Photon Eta",    100,  (-4, 4),   "Eta",      "selected_photon_eta.png")
]

for data, title, bins, plot_range, xlabel, filename in plot_configs:
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, range=plot_range, histtype='step', lw=2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Number of Objects')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(filename, dpi=300)
    plt.close()
