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
        # self.out.branch("pass_selection1",  "B")
        # self.out.branch("pass_selection2",  "B")
        # self.out.branch("photon_selection",  "I")
        self.out.branch("njets_fake",  "I")
        self.out.branch("njets_fake_template",  "I")
        
        ########################################################
        self.out.branch("n_ele2_ismatch", "I")
        self.out.branch("n_muon2_ismatch", "I")
        self.out.branch("n_ele4_ismatch", "I")
        self.out.branch("n_muon4_ismatch", "I")

        self.out.branch("ele0_pt", "F")
        self.out.branch("ele0_eta", "F")
        self.out.branch("ele0_phi", "F")
        self.out.branch("ele1_pt", "F")
        self.out.branch("ele1_eta", "F")
        self.out.branch("ele1_phi", "F")
        self.out.branch("ele2_pt", "F")
        self.out.branch("ele2_eta", "F")
        self.out.branch("ele2_phi", "F")
        self.out.branch("ele3_pt", "F")
        self.out.branch("ele3_eta", "F")
        self.out.branch("ele3_phi", "F")

        self.out.branch("muon0_pt", "F")
        self.out.branch("muon0_eta", "F")
        self.out.branch("muon0_phi", "F")
        self.out.branch("muon1_pt", "F")
        self.out.branch("muon1_eta", "F")
        self.out.branch("muon1_phi", "F")
        self.out.branch("muon2_pt", "F")
        self.out.branch("muon2_eta", "F")
        self.out.branch("muon2_phi", "F")
        self.out.branch("muon3_pt", "F")
        self.out.branch("muon3_eta", "F")
        self.out.branch("muon3_phi", "F")
        ########################################################

        # self.out.branch("n_loose_mu", "I")
        # self.out.branch("n_loose_ele", "I")
        # self.out.branch("n_photon", "I")
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
        # self.out.branch("fakephoton_ismatch", "I")

        self.out.branch("controlphotonpt",  "F")
        self.out.branch("controlphotoneta",  "F")
        self.out.branch("controlphotonphi",  "F")
        self.out.branch("controlphotonchiso",  "F")
        self.out.branch("controlphotonsieie",  "F")
        # self.out.branch("controlphoton_ismatch", "I")




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
        if ((event.nMuon + event.nElectron) < 3): return False

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
            if muons[i].Muon_looseId and abs(muons[i].dxy)<0.5 and abs(muons[i].dz)<1:
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
        if len(electrons_select)==2 and len(muons_select)==2 and sum_eleCharge==0 and sum_muonCharge==0:
            lepChannel = "2e2mu"
        elif len(muons_select)==4 and sum_muonCharge==0:
            lepChannel = "4mu"
        elif len(electrons_select)==4 and sum_eleCharge==0:
            lepChannel = "4e"
        else:
            return False

        # select  prompt photons  from signal mc

        for i in range(0,len(photons)):
            if photons[i].pt < 12:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue
            if photons[i].cutBased <1:
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
       
        #  1     3         5          7           9       11       13
        #| pt | scEta | H over EM | sigma ieie | Isoch | IsoNeu | Isopho |
        mask_full = (1<<1) | (1<<3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13) 
        mask_sieie_chiso = (1<<1) | (1<<3) | (1 << 5) | (1 << 11) | (1 << 13)
        mask_HoverE = (1<<1) | (1<<3) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
        mask_sieie = (1<<1) | (1<<3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13)
        mask_chiso = (1<<1) | (1<<3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
        mask_neuiso = (1<<1) | (1<<3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 13)
        mask_phoiso = (1<<1) | (1<<3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11)
       
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

        isprompt_mask = (1 << 0) #isPrompt
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct
        isdirecttaudecayproduct_mask = (1 << 4) #isDirectTauDecayProduct
        isprompttaudecayproduct = (1 << 3) #isPromptTauDecayProduct
        isfromhardprocess_mask = (1 << 8) #isPrompt

        channel = 0 
        # 2e2mu:     1
        # 4e:        2
        # 4mu:       3

        # 2e2mu channel, lep mathcing to gen level ---------------------------------------------
        mll = -10
        ptll = -10
        n_ele2_ismatch =0
        n_muon2_ismatch=0
        n_ele4_ismatch = 0
        n_muon4_ismatch = 0
        

        # 2e2mu
        if lepChannel == "2e2mu": 
            if hasattr(event, 'nGenPart'):
                print 'calculate the lepton flag in channel 2e2mu'

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        n_ele2_ismatch += 1<<0
                        break
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == 11 and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        n_ele2_ismatch += 1<<1
                        break
                            
                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        n_muon2_ismatch += 1<<2
                        break
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == 13 and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[1]].eta,muons[muons_select[1]].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        n_muon2_ismatch += 1<<3
                        break

            channel = 1
            self.out.fillBranch("channel",channel)
            self.out.fillBranch("n_ele2_ismatch",n_ele2_ismatch)
            self.out.fillBranch("n_muon2_ismatch",n_muon2_ismatch)
            self.out.fillBranch("muon0_pt",muons[muons_select[0]].pt)
            self.out.fillBranch("muon0_eta",muons[muons_select[0]].eta)
            self.out.fillBranch("muon0_phi",muons[muons_select[0]].phi)
            self.out.fillBranch("muon1_pt",muons[muons_select[1]].pt)
            self.out.fillBranch("muon1_eta",muons[muons_select[1]].eta)
            self.out.fillBranch("muon1_phi",muons[muons_select[1]].phi)
            self.out.fillBranch("ele0_pt",electrons[electrons_select[0]].pt)
            self.out.fillBranch("ele0_eta",electrons[electrons_select[0]].eta)
            self.out.fillBranch("ele0_phi",electrons[electrons_select[0]].phi)
            self.out.fillBranch("ele1_pt",electrons[electrons_select[1]].pt)
            self.out.fillBranch("ele1_eta",electrons[electrons_select[1]].eta)
            self.out.fillBranch("ele1_phi",electrons[electrons_select[1]].phi)

        # 4e
        elif lepChannel == "4e":
            # if deltaR(electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi,electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi)<0.5:
            #    return False 
            # print 'test',len(genparts)
            if hasattr(event, 'nGenPart'):
                print 'calculate the lepton flag in channel 4e'

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        n_ele4_ismatch += 1 <<0
                        break 
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == 11 and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        n_ele4_ismatch += 1 <<1
                        break 
                for k in range(0,len(genparts)):
                    if genparts[k].pt > 5 and abs(genparts[k].pdgId) == 11 and ((genparts[k].statusFlags & isprompt_mask == isprompt_mask) or (genparts[k].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[2]].eta,electrons[electrons_select[2]].phi,genparts[k].eta,genparts[k].phi) < 0.3:
                        n_ele4_ismatch += 1 <<2
                        break 
                for m in range(0,len(genparts)):
                    if genparts[m].pt > 5 and abs(genparts[m].pdgId) == 11 and ((genparts[m].statusFlags & isprompt_mask == isprompt_mask) or (genparts[m].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[3]].eta,electrons[electrons_select[3]].phi,genparts[m].eta,genparts[m].phi) < 0.3:
                        n_ele4_ismatch += 1 <<3
                        break 

            channel = 2
            self.out.fillBranch("channel",channel)
            self.out.fillBranch("n_ele4_ismatch",n_ele4_ismatch)
            
            self.out.fillBranch("ele0_pt", electrons[electrons_select[0]].pt)
            self.out.fillBranch("ele0_eta",electrons[electrons_select[0]].eta)
            self.out.fillBranch("ele0_phi",electrons[electrons_select[0]].phi)
            self.out.fillBranch("ele1_pt", electrons[electrons_select[1]].pt)
            self.out.fillBranch("ele1_eta",electrons[electrons_select[1]].eta)
            self.out.fillBranch("ele1_phi",electrons[electrons_select[1]].phi)
            self.out.fillBranch("ele2_pt", electrons[electrons_select[2]].pt)
            self.out.fillBranch("ele2_eta",electrons[electrons_select[2]].eta)
            self.out.fillBranch("ele2_phi",electrons[electrons_select[2]].phi)
            self.out.fillBranch("ele3_pt", electrons[electrons_select[3]].pt)
            self.out.fillBranch("ele3_eta",electrons[electrons_select[3]].eta)
            self.out.fillBranch("ele3_phi",electrons[electrons_select[3]].phi)

        # 4mu 
        elif lepChannel == "4mu":
            # if deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,muons[muons_select[1]].eta,muons[muons_select[1]].phi)<0.5:
            #    return False 
            if hasattr(event, 'nGenPart'):
                print 'calculate the lepton flag in channel 4mu'

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        n_muon4_ismatch += 1<<0
                        break 
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == 13 and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[1]].eta,muons[muons_select[1]].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        n_muon4_ismatch += 1<<1
                        break 
                for k in range(0,len(genparts)):
                    if genparts[k].pt > 5 and abs(genparts[k].pdgId) == 13 and ((genparts[k].statusFlags & isprompt_mask == isprompt_mask) or (genparts[k].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[2]].eta,muons[muons_select[2]].phi,genparts[k].eta,genparts[k].phi) < 0.3:
                        n_muon4_ismatch += 1<<2
                        break 
                for m in range(0,len(genparts)):
                    if genparts[m].pt > 5 and abs(genparts[m].pdgId) == 13 and ((genparts[m].statusFlags & isprompt_mask == isprompt_mask) or (genparts[m].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[3]].eta,muons[muons_select[3]].phi,genparts[m].eta,genparts[m].phi) < 0.3:
                        n_muon4_ismatch += 1<<3
                        break 

            channel = 3
            self.out.fillBranch("channel",channel)
            self.out.fillBranch("n_muon4_ismatch",n_muon4_ismatch)
            self.out.fillBranch("muon0_pt",muons[muons_select[0]].pt)
            self.out.fillBranch("muon0_eta",muons[muons_select[0]].eta)
            self.out.fillBranch("muon0_phi",muons[muons_select[0]].phi)
            self.out.fillBranch("muon1_pt",muons[muons_select[1]].pt)
            self.out.fillBranch("muon1_eta",muons[muons_select[1]].eta)
            self.out.fillBranch("muon1_phi",muons[muons_select[1]].phi)
            self.out.fillBranch("muon2_pt",muons[muons_select[2]].pt)
            self.out.fillBranch("muon2_eta",muons[muons_select[2]].eta)
            self.out.fillBranch("muon2_phi",muons[muons_select[2]].phi)
            self.out.fillBranch("muon3_pt",muons[muons_select[3]].pt)
            self.out.fillBranch("muon3_eta",muons[muons_select[3]].eta)
            self.out.fillBranch("muon3_phi",muons[muons_select[3]].phi)

        else:
            return False
        
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