from SetupModels.CreateNetworkParameters import *
try:
    from __main__ import cfg
except:
    from cfg import cfg

gLs, ELs, CapsOrig, ConductWithGapJunct, ReversPotWithGapJunct, CapsMod, gNas, gKv3s, gKv7s, thm1s, thh2s, thn1s, tha1s, SharedParams, syns, delays, gms, synsgj, ggs = NetworkParams(NumNeurons=cfg.N, FactorTau=cfg.FactorTau, FactorKv3=cfg.FactorKv3, FactorKv7=cfg.FactorKv7, GapJunctProb=cfg.GapJunctProb, ChemycalConnProb=cfg.ChemycalConnProb, delaymin=.6, delaymax=1., meangms=0., sigmagms=1.,homogeneous=cfg.HOMOGENEOUS)
