#!/usr/bin/env python
# Analyzer for WWG Analysis based on nanoAOD tools

import os, sys
import math
import ROOT
from math import sin, cos, sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

class ZZG_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree

        self.out.branch("event",  "F")
        self.out.branch("lumi",  "F")
        self.out.branch("run",  "F")
        self.out.branch("gen_weight","F")
        self.out.branch("n_pos", "I")
        self.out.branch("n_minus", "I")
        self.out.branch("channel",  "I")
        
        ########################################################
        self.out.branch("loose_electron_ismatch", "O", 4)
        self.out.branch("loose_electron_idx", "I", 4)
        self.out.branch("loose_electron_pdgId","I",4)
        self.out.branch("loose_electron_pt","F",4)
        self.out.branch("loose_electron_eta","F",4)
        self.out.branch("loose_electron_phi","F",4)
        self.out.branch("loose_electron_mass","F",4)

        self.out.branch("loose_muon_ismatch", "O", 4)
        self.out.branch("loose_muon_idx", "I", 4)
        self.out.branch("loose_muon_pdgId","I",4)
        self.out.branch("loose_muon_pt","F",4)
        self.out.branch("loose_muon_eta","F",4)
        self.out.branch("loose_muon_phi","F",4)
        self.out.branch("loose_muon_mass","F",4)

        ########################################################

        self.out.branch("promptphotonpt",  "F")
        self.out.branch("promptphotoneta",  "F")
        self.out.branch("promptphotonphi",  "F")
        self.out.branch("promptphotonchiso",  "F")
        self.out.branch("promptphotonsieie",  "F")
        self.out.branch("promptphoton_ismatch", "I")

        self.out.branch("fakephotonpt",  "F")
        self.out.branch("fakephotoneta",  "F")
        self.out.branch("fakephotonphi",  "F")
        self.out.branch("fakephotonchiso",  "F")
        self.out.branch("fakephotonsieie",  "F")

        self.out.branch("controlphotonpt",  "F")
        self.out.branch("controlphotoneta",  "F")
        self.out.branch("controlphotonphi",  "F")
        self.out.branch("controlphotonchiso",  "F")
        self.out.branch("controlphotonsieie",  "F")

        self.out.branch("dataphotonpt",  "F")
        self.out.branch("dataphotoneta",  "F")
        self.out.branch("dataphotonphi",  "F")
        self.out.branch("dataphotonchiso",  "F")
        self.out.branch("dataphotonsieie",  "F")

        self.out.branch("npu",  "I")
        self.out.branch("ntruepu",  "F")
        self.out.branch("npvs","I")
        self.out.branch("met",  "F")
        self.out.branch("metup",  "F")
        self.out.branch("puppimet","F")
        self.out.branch("puppimetphi","F")
        self.out.branch("rawmet","F")
        self.out.branch("rawmetphi","F")
        self.out.branch("metphi","F")
    

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        # PV selection
        if (event.PV_npvsGood<1): return False

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
        genparts = None
        if hasattr(event, 'nGenPart'):
           genparts = Collection(event, "GenPart")

        electrons_select = []
        muons_select = [] 
        # jets_select = []
        # dileptonp4 = ROOT.TLorentzVector()
        selected_prompt_photons = []
        selected_data_photons = []
        selected_control_photons = []
        selected_fake_photons = []

        #selection on muons
        sum_muonCharge = 0
        for i in range(0,len(muons)):
            if muons[i].pt < 4:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].pfRelIso04_all > 0.25:
                continue   
            if muons[i].looseId and abs(muons[i].dxy)<0.5 and abs(muons[i].dz)<1:
                sum_muonCharge = sum_muonCharge + muons[i].charge
                muons_select.append(i)

        # selection on electrons
        sum_eleCharge = 0
        for i in range(0,len(electrons)):
            if electrons[i].pt < 4:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) > 2.5:
                continue
            if electrons[i].cutBased >= 2 and abs(electrons[i].dz) < 1 and abs(electrons[i].dxy) < 0.5:
                sum_eleCharge = sum_eleCharge + electrons[i].charge
                electrons_select.append(i)

        lepChannel = ""
        channel = 0 
        if len(electrons_select)==2 and len(muons_select)==2 and sum_eleCharge==0 and sum_muonCharge==0:
            lepChannel = "2e2mu"
            channel = 1
        elif len(muons_select)==4 and sum_muonCharge==0:
            lepChannel = "4mu"
            channel = 2
        elif len(electrons_select)==4 and sum_eleCharge==0:
            lepChannel = "4e"
            channel = 3
        elif len(electrons_select)==2 and sum_eleCharge==0:
            lepChannel = "2e"
            channel = 4
        elif len(muons_select)==2 and sum_muonCharge==0:
            lepChannel = "2mu"
            channel = 5
        else:
            return False

        loose_electron_idx = [-1]*4
        loose_electron_pdgId = [0]*4
        loose_electron_pt = [-99]*4
        loose_electron_eta = [-99]*4
        loose_electron_phi = [-99]*4
        loose_electron_mass = [-99]*4  

        loose_muon_idx = [-1]*4
        loose_muon_pdgId = [0]*4
        loose_muon_pt = [-99]*4
        loose_muon_eta = [-99]*4
        loose_muon_phi = [-99]*4
        loose_muon_mass = [-99]*4
        for i in range(len(electrons_select)):
            idx = electrons_select[i]
            loose_electron_idx  [i]  = electrons_select[i]
            loose_electron_pdgId[i]  = electrons[idx].pdgId
            loose_electron_pt   [i]  = electrons[idx].pt 
            loose_electron_eta  [i]  = electrons[idx].eta
            loose_electron_phi  [i]  = electrons[idx].phi
            loose_electron_mass [i]  = electrons[idx].mass 

        for i in range(len(muons_select)):
            idx = muons_select[i]
            loose_muon_idx  [i] = muons_select[i]
            loose_muon_pdgId[i] = muons[idx].pdgId  
            loose_muon_pt   [i] = muons[idx].pt 
            loose_muon_eta  [i] = muons[idx].eta 
            loose_muon_phi  [i] = muons[idx].phi 
            loose_muon_mass [i] = muons[idx].mass 

        isprompt_mask = (1 << 0) #isPrompt
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct
        isdirecttaudecayproduct_mask = (1 << 4) #isDirectTauDecayProduct
        isprompttaudecayproduct = (1 << 3) #isPromptTauDecayProduct
        isfromhardprocess_mask = (1 << 8) #isPrompt

        # 2e2mu channel, lep mathcing to gen level ---------------------------------------------
        loose_electron_ismatch = [False]*4
        loose_muon_ismatch = [False]*4


        # lepton matching
        if hasattr(event, 'nGenPart'):
            # print 'calculate the lepton flag'
            for ilep in range(len(electrons_select)):
                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 \
                    and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) \
                    and deltaR(electrons[electrons_select[ilep]].eta,electrons[electrons_select[ilep]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        loose_electron_ismatch[ilep] = True
                        break             
            for ilep in range(len(muons_select)):               
                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 \
                    and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) \
                    and deltaR(muons[muons_select[ilep]].eta,muons[muons_select[ilep]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        loose_muon_ismatch[ilep] = True
                        break


        self.out.fillBranch("channel",channel) 
        self.out.fillBranch("loose_electron_idx",loose_electron_idx) 
        self.out.fillBranch("loose_electron_ismatch",loose_electron_ismatch) 
        self.out.fillBranch("loose_electron_pdgId",loose_electron_pdgId)
        self.out.fillBranch("loose_electron_pt",loose_electron_pt)
        self.out.fillBranch("loose_electron_eta",loose_electron_eta)
        self.out.fillBranch("loose_electron_phi",loose_electron_phi)
        self.out.fillBranch("loose_electron_mass",loose_electron_mass)

        self.out.fillBranch("loose_muon_idx",loose_muon_idx)  
        self.out.fillBranch("loose_muon_ismatch",loose_muon_ismatch)  
        self.out.fillBranch("loose_muon_pdgId",loose_muon_pdgId)
        self.out.fillBranch("loose_muon_pt",loose_muon_pt)
        self.out.fillBranch("loose_muon_eta",loose_muon_eta)
        self.out.fillBranch("loose_muon_phi",loose_muon_phi)
        self.out.fillBranch("loose_muon_mass",loose_muon_mass)


        #  1     3         5          7           9       11       13
        #| pt | scEta | H over EM | sigma ieie | Isoch | IsoNeu | Isopho |
        mask_full = (1<<1) | (1<<3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13) 
        mask_sieie_chiso = (1<<1) | (1<<3) | (1 << 5) | (1 << 11) | (1 << 13)
        mask_HoverE = (1<<1) | (1<<3) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
        mask_sieie = (1<<1) | (1<<3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13)
        mask_chiso = (1<<1) | (1<<3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
        mask_neuiso = (1<<1) | (1<<3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 13)
        mask_phoiso = (1<<1) | (1<<3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11)

        # select  prompt photons  from signal mc
        for i in range(0,len(photons)):
            if photons[i].pt < 12:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue
            # if photons[i].cutBased <1:
            #     continue

            bitmap = photons[i].vidNestedWPBitmap & mask_sieie
            #save photons pass the ID without sigma ieie 
            if not (bitmap == mask_sieie):
                continue

            pass_lepton_dr_cut = True
            for j in range(0,len(muons_select)):
                if deltaR(muons[muons_select[j]].eta,muons[muons_select[j]].phi,  photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(electrons_select)):
                if deltaR(electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi,  photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue
            selected_prompt_photons.append(i)  #append the medium photons passing full ID
       
       
        # select data photons from data, open sieie
        for i in range(0,len(photons)):
            if photons[i].pt < 12:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            bitmap = photons[i].vidNestedWPBitmap & mask_sieie
            #save photons pass the ID without sigma ieie 
            if not (bitmap == mask_sieie):
                continue
             
            pass_lepton_dr_cut = True
            for j in range(0,len(muons_select)):
                if deltaR(muons[muons_select[j]].eta,muons[muons_select[j]].phi,   photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(electrons_select)):
                if deltaR(electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi,   photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue
            selected_data_photons.append(i) #for fake template from data

        # select nonprompt photons from data
        for i in range(0,len(photons)):
            if photons[i].pt < 12:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            bitmap = photons[i].vidNestedWPBitmap & mask_sieie_chiso
            #save photons pass the ID without sigma ieie and Isoch
            if not (bitmap == mask_sieie_chiso):
                continue
             
            pass_lepton_dr_cut = True
            for j in range(0,len(muons_select)):
                if deltaR(muons[muons_select[j]].eta,muons[muons_select[j]].phi,   photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(electrons_select)):
                if deltaR(electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi,   photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue
            selected_fake_photons.append(i) #for fake template from data

        # select control photons from data
        for i in range(0,len(photons)):
            if photons[i].pt < 12:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            photon_bitmap_full = photons[i].vidNestedWPBitmap & mask_full
            photon_bitmap_HoverE = photons[i].vidNestedWPBitmap & mask_HoverE
            photon_bitmap_sieie = photons[i].vidNestedWPBitmap & mask_sieie
            photon_bitmap_chiso = photons[i].vidNestedWPBitmap & mask_chiso
            photon_bitmap_neuiso = photons[i].vidNestedWPBitmap & mask_neuiso
            photon_bitmap_phoiso = photons[i].vidNestedWPBitmap & mask_phoiso

            #not pass the full ID
            if photons[i].cutBased >0:
                continue
            # if (photon_bitmap_full == mask_full):
            #     continue

            #fail one of varaible in the ID
            if not ((photon_bitmap_HoverE==mask_HoverE) or (photon_bitmap_sieie==mask_sieie) or (photon_bitmap_chiso==mask_chiso) or (photon_bitmap_neuiso==mask_neuiso) or (photon_bitmap_phoiso==mask_phoiso)):
                continue

            pass_lepton_dr_cut = True
            for j in range(0,len(muons_select)):
                if deltaR(muons[muons_select[j]].eta,muons[muons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(electrons_select)):
                if deltaR(electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue
            selected_control_photons.append(i)  # append the control photons

        
        if len(selected_prompt_photons)>0:
            photon_ismatch = -10
            if hasattr(event, 'nGenPart') :
                for j, genpart in enumerate(genparts):
                    if photons[selected_prompt_photons[0]].genPartIdx >=0 and genpart.pt > 5 and abs(genpart.pdgId) == 22 and ((genparts[photons[selected_prompt_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_prompt_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask) or (genparts[photons[selected_prompt_photons[0]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask)) and deltaR(photons[selected_prompt_photons[0]].eta,photons[selected_prompt_photons[0]].phi,genpart.eta,genpart.phi) < 0.3:
                        photon_ismatch =1
                        break
            self.out.fillBranch("promptphotonpt",photons[selected_prompt_photons[0]].pt)
            self.out.fillBranch("promptphotoneta",photons[selected_prompt_photons[0]].eta)
            self.out.fillBranch("promptphotonphi",photons[selected_prompt_photons[0]].phi)
            self.out.fillBranch("promptphotonchiso",photons[selected_prompt_photons[0]].pfRelIso03_chg*photons[selected_prompt_photons[0]].pt)
            self.out.fillBranch("promptphotonsieie",photons[selected_prompt_photons[0]].sieie)
            self.out.fillBranch("promptphoton_ismatch",photon_ismatch)
        
        if len(selected_control_photons)>0:
            self.out.fillBranch("controlphotonpt",photons[selected_control_photons[0]].pt)
            self.out.fillBranch("controlphotoneta",photons[selected_control_photons[0]].eta)
            self.out.fillBranch("controlphotonphi",photons[selected_control_photons[0]].phi)
            self.out.fillBranch("controlphotonchiso",photons[selected_control_photons[0]].pfRelIso03_chg*photons[selected_control_photons[0]].pt)
            self.out.fillBranch("controlphotonsieie",photons[selected_control_photons[0]].sieie)


        if len(selected_fake_photons)>0:  
            self.out.fillBranch("fakephotonpt",photons[selected_fake_photons[0]].pt)
            self.out.fillBranch("fakephotoneta",photons[selected_fake_photons[0]].eta)
            self.out.fillBranch("fakephotonphi",photons[selected_fake_photons[0]].phi)
            self.out.fillBranch("fakephotonchiso",photons[selected_fake_photons[0]].pfRelIso03_chg*photons[selected_fake_photons[0]].pt)
            self.out.fillBranch("fakephotonsieie",photons[selected_fake_photons[0]].sieie)

        if len(selected_data_photons)>0:  
            self.out.fillBranch("dataphotonpt",photons[selected_data_photons[0]].pt)
            self.out.fillBranch("dataphotoneta",photons[selected_data_photons[0]].eta)
            self.out.fillBranch("dataphotonphi",photons[selected_data_photons[0]].phi)
            self.out.fillBranch("dataphotonchiso",photons[selected_data_photons[0]].pfRelIso03_chg*photons[selected_data_photons[0]].pt)
            self.out.fillBranch("dataphotonsieie",photons[selected_data_photons[0]].sieie)



        if hasattr(event,'Pileup_nPU'):    
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)
    
        if hasattr(event,'Pileup_nTrueInt'):    
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)

        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("metup",sqrt(pow(event.MET_pt*cos(event.MET_phi) + event.MET_MetUnclustEnUpDeltaX,2) + pow(event.MET_pt*sin(event.MET_phi) + event.MET_MetUnclustEnUpDeltaY,2)))
        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimetphi",event.PuppiMET_phi)
        self.out.fillBranch("rawmet",event.RawMET_pt)
        self.out.fillBranch("rawmetphi",event.RawMET_phi)
        self.out.fillBranch("metphi",event.MET_phi)


        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)
        # print event.event,event.luminosityBlock,event.run
        if hasattr(event,'Generator_weight'):
            if event.Generator_weight > 0 :
                n_pos=1
                n_minus=0
            else:
                n_minus=1
                n_pos=0
            self.out.fillBranch("gen_weight",event.Generator_weight)
            self.out.fillBranch("n_pos",n_pos)
            self.out.fillBranch("n_minus",n_minus)
        else:    
            self.out.fillBranch("gen_weight",0)
            self.out.fillBranch("n_pos",0)
            self.out.fillBranch("n_minus",0)

        return True

fakePhoton_Module = lambda: ZZG_Producer()