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

el = ak.zip({
    "pt": events["Electron.PT"],
    "eta": events["Electron.Eta"],
    "phi": events["Electron.Phi"],
    "charge": events["Electron.Charge"],
}, with_name="Momentum4D")
        
mu = ak.zip({
    "pt": events["MuonTight.PT"],
    "eta": events["MuonTight.Eta"],
    "phi": events["MuonTight.Phi"],
    "charge": events["MuonTight.Charge"],
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

sel_el = el[el_mask]
sel_mu = mu[mu_mask]
sel_ph = ph[ph_mask]

# select 후 variable distribution 확인

plot_configs = [
    (ak.flatten(sel_el.pt),      "Selected Electron pT", 100,  (0, 200), "pT [GeV]", "selected_electron_pt.png"),
    (ak.flatten(sel_mu.pt),      "Selected Muon pT",     100,  (0, 200), "pT [GeV]", "selected_muon_pt.png"),
    (ak.flatten(sel_ph.pt),      "Selected Photon pT",   100,  (0, 200), "pT [GeV]", "selected_photon_pt.png"),
    (ak.flatten(sel_el.eta),     "Selected Electron Eta", 100, (-4, 4),   "Eta",      "selected_electron_eta.png"),
    (ak.flatten(sel_mu.eta),     "Selected Muon Eta",    100,  (-4, 4),   "Eta",      "selected_muon_eta.png"),
    (ak.flatten(sel_ph.eta),     "Selected Photon Eta",    100,  (-4, 4),   "Eta",      "selected_photon_eta.png")
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
