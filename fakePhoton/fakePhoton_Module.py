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
        self.out.branch("pass_selection1",  "B")
        self.out.branch("pass_selection2",  "B")
        self.out.branch("photon_selection",  "I")
        self.out.branch("njets_fake",  "I")
        self.out.branch("njets_fake_template",  "I")
        
        ########################################################
        self.out.branch("n_ele2_isprompt", "I")
        self.out.branch("n_muon2_isprompt", "I")
        self.out.branch("n_ele4_isprompt", "I")
        self.out.branch("n_muon4_isprompt", "I")

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

        self.out.branch("n_loose_mu", "I")
        self.out.branch("n_loose_ele", "I")
        self.out.branch("n_photon", "I")
        self.out.branch("photonet",  "F")
        self.out.branch("photoneta",  "F")
        self.out.branch("photonphi",  "F")
        self.out.branch("photonchiso",  "F")
        self.out.branch("photonsieie",  "F")
        self.out.branch("photon_isprompt", "I")
        # self.out.branch("photon_gen_matching", "I")
        self.out.branch("photonet_f",  "F")
        self.out.branch("photoneta_f",  "F")
        self.out.branch("photonphi_f",  "F")
        self.out.branch("photonchiso_f",  "F")
        self.out.branch("photonsieie_f",  "F")
        self.out.branch("photon_isprompt_f", "I")
        # self.out.branch("photon_gen_matching_f", "I")
        # self.out.branch("mll",  "F")
        # self.out.branch("ptll",  "F")
        # self.out.branch("mt",  "F")

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
        
        # self.out.branch("n_num", "I")
        # self.out.branch("MET_pass","I")
        # self.out.branch("n_bjets","I")
        # self.out.branch("njets","I")
        # self.out.branch("njets50","I")
        # self.out.branch("njets40","I")
        # self.out.branch("njets30","I")
        # self.out.branch("njets20","I")
        # self.out.branch("njets15","I")
        # self.out.branch("HLT_Ele1","I")
        # self.out.branch("HLT_Ele2","I")
        # self.out.branch("HLT_Mu1","I")
        # self.out.branch("HLT_Mu2","I")
        # self.out.branch("HLT_emu1","I")
        # self.out.branch("HLT_emu2","I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

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

        # HLT_Ele1 = event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL
        # HLT_Ele2 = event.HLT_Ele35_WPTight_Gsf

        # HLT_Mu1 = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8
        # HLT_Mu2 = event.HLT_IsoMu24

        # HLT_emu1 = event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ
        # HLT_emu2 = event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ

        pass_selection1 = False
        pass_selection2 = False

        # if not (HLT_Ele1 or HLT_Ele2 or HLT_Mu1 or HLT_Mu2 or HLT_emu1 or HLT_emu2):
        #    return False
        # self.out.fillBranch("HLT_Ele1",HLT_Ele1)
        # self.out.fillBranch("HLT_Ele2",HLT_Ele2)
        # self.out.fillBranch("HLT_Mu1",HLT_Mu1)
        # self.out.fillBranch("HLT_Mu2",HLT_Mu2)
        # self.out.fillBranch("HLT_emu1",HLT_emu1)
        # self.out.fillBranch("HLT_emu2",HLT_emu2)

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
        if hasattr(event, 'nGenPart'):
           genparts = Collection(event, "GenPart")

        electrons_select = []
        muons_select = [] 
        jets_select = []
        dileptonp4 = ROOT.TLorentzVector()
        selected_medium_photons = []
        selected_control_photons = []
        selected_medium_or_control_photons = []
        selected_fake_template_photons = []

        #selection on muons
        # muon_pass =0
        sum_muonCharge = 0
        for i in range(0,len(muons)):
            if muons[i].pt < 4:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].pfRelIso04_all > 0.35:
                continue   
            if muons[i].mediumId == True:
                sum_muonCharge = sum_muonCharge + muons[i].charge
                muons_select.append(i)

        # selection on electrons
        sum_eleCharge = 0
        for i in range(0,len(electrons)):
            if electrons[i].pt < 4:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) > 2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
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

        # select medium photons, prompt photons  
        photon_pass=0
        for i in range(0,len(photons)):
            if photons[i].pt < 20:
                continue
            if abs(photons[i].eta) > 2.5:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            #| pt | scEta | H over EM | sigma ieie | Isoch | IsoNeu | Isopho |
            mask1 = 0b10101010101010 # full medium ID
            mask2 = 0b00101010101010 # fail Isopho
            mask3 = 0b10001010101010 # fail IsoNeu
            mask4 = 0b10100010101010 # fail Isoch
            mask5 = 0b10101000101010 # fail sigma ieie

            bitmap = photons[i].vidNestedWPBitmap & mask1

            # the photon pass the full ID
            if not (bitmap == mask1):
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
            selected_medium_photons.append(i)  #append the medium photons passing full ID
            selected_medium_or_control_photons.append(i)

        # select control photons
        for i in range(0,len(photons)):
            if photons[i].pt < 20:
                continue
            if abs(photons[i].eta) > 2.5:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            #| pt | scEta | H over EM | sigma ieie | Isoch | IsoNeu | Isopho |
            mask1 = 0b10101010101010 # full medium ID
            mask2 = 0b00101010101010 # fail Isopho
            mask3 = 0b10001010101010 # fail IsoNeu
            mask4 = 0b10100010101010 # fail Isoch
            mask5 = 0b10101000101010 # fail sigma ieie

            bitmap = photons[i].vidNestedWPBitmap & mask1

            #not pass the full ID
            if (bitmap == mask1):
                continue

            #fail one of varaible in the ID
            if not ((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
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
            selected_medium_or_control_photons.append(i)

        # select fake photons, nonprompt photons
        for i in range(0,len(photons)):
            if photons[i].pt < 20:
                continue
            if abs(photons[i].eta) > 2.5:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            #| pt | scEta | H over EM | sigma ieie | Isoch | IsoNeu | Isopho |
            mask1 = 0b10100000101010 # remove the Isoch and sigma ieie
            bitmap = photons[i].vidNestedWPBitmap & mask1
            #save photons pass the ID without sigma ieie and Isoch
            if not (bitmap == mask1):
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
            selected_fake_template_photons.append(i) #for fake template from data



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
        n_ele2_isprompt =0
        n_muon2_isprompt=0
        n_ele4_isprompt = 0
        n_muon4_isprompt = 0
        

        # 2e2mu
        if lepChannel == "2e2mu": 
            if hasattr(event, 'nGenPart'):
                print 'calculate the lepton flag in channel 2e2mu'

            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    n_ele2_isprompt += 1
                    break
            for j in range(0,len(genparts)):
                if genparts[j].pt > 5 and abs(genparts[j].pdgId) == 11 and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                    n_ele2_isprompt += 1
                    break
                        
            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    n_muon2_isprompt += 1
                    break
            for j in range(0,len(genparts)):
                if genparts[j].pt > 5 and abs(genparts[j].pdgId) == 13 and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[1]].eta,muons[muons_select[1]].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                    n_muon2_isprompt += 1
                    break

            channel = 1
            self.out.fillBranch("channel",channel)
            self.out.fillBranch("n_ele2_isprompt",n_ele2_isprompt)
            self.out.fillBranch("n_muon2_isprompt",n_muon2_isprompt)
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
                    n_ele4_isprompt += 1 
                    break 
            for j in range(0,len(genparts)):
                if genparts[j].pt > 5 and abs(genparts[j].pdgId) == 11 and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                    n_ele4_isprompt += 1 
                    break 
            for k in range(0,len(genparts)):
                if genparts[k].pt > 5 and abs(genparts[k].pdgId) == 11 and ((genparts[k].statusFlags & isprompt_mask == isprompt_mask) or (genparts[k].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[2]].eta,electrons[electrons_select[2]].phi,genparts[k].eta,genparts[k].phi) < 0.3:
                    n_ele4_isprompt += 1 
                    break 
            for m in range(0,len(genparts)):
                if genparts[m].pt > 5 and abs(genparts[m].pdgId) == 11 and ((genparts[m].statusFlags & isprompt_mask == isprompt_mask) or (genparts[m].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[3]].eta,electrons[electrons_select[3]].phi,genparts[m].eta,genparts[m].phi) < 0.3:
                    n_ele4_isprompt += 1 
                    break 


                

            channel = 2
            self.out.fillBranch("channel",channel)
            self.out.fillBranch("n_ele4_isprompt",n_ele4_isprompt)
            
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
                    n_muon4_isprompt += 1
                    break 
            for j in range(0,len(genparts)):
                if genparts[j].pt > 5 and abs(genparts[j].pdgId) == 13 and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[1]].eta,muons[muons_select[1]].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                    n_muon4_isprompt += 1
                    break 
            for k in range(0,len(genparts)):
                if genparts[k].pt > 5 and abs(genparts[k].pdgId) == 13 and ((genparts[k].statusFlags & isprompt_mask == isprompt_mask) or (genparts[k].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[2]].eta,muons[muons_select[2]].phi,genparts[k].eta,genparts[k].phi) < 0.3:
                    n_muon4_isprompt += 1
                    break 
            for m in range(0,len(genparts)):
                if genparts[m].pt > 5 and abs(genparts[m].pdgId) == 13 and ((genparts[m].statusFlags & isprompt_mask == isprompt_mask) or (genparts[m].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[3]].eta,muons[muons_select[3]].phi,genparts[m].eta,genparts[m].phi) < 0.3:
                    n_muon4_isprompt += 1
                    break 

            channel = 3
            self.out.fillBranch("channel",channel)
            self.out.fillBranch("n_muon4_isprompt",n_muon4_isprompt)

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

        pass_selection1 = (len(selected_control_photons) + len(selected_medium_photons)) >= 1 # select medium and control photons
        pass_selection2 = len(selected_fake_template_photons) == 1     # select fake photons ? == 1

        self.out.fillBranch("pass_selection1",pass_selection1) # select medium and control photons
        self.out.fillBranch("pass_selection2",pass_selection2) # select fake photons
        
        if pass_selection1:
            # photon_gen_matching=-10
            photon_isprompt =-10
        
            if hasattr(event, 'nGenPart') :
                for j, genpart in enumerate(genparts):
                    if photons[selected_medium_or_control_photons[0]].genPartIdx >=0 and genpart.pt > 5 and abs(genpart.pdgId) == 22 and ((genparts[photons[selected_medium_or_control_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_medium_or_control_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask) or (genparts[photons[selected_medium_or_control_photons[0]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask)) and deltaR(photons[selected_medium_or_control_photons[0]].eta,photons[selected_medium_or_control_photons[0]].phi,genpart.eta,genpart.phi) < 0.3:
                        photon_isprompt =1
                        break
            mask1 = 0b10101010101010 # full medium ID
            mask2 = 0b00101010101010 # fail Isopho
            mask3 = 0b10001010101010 # fail IsoNeu
            mask4 = 0b10100010101010 # fail Isoch
            mask5 = 0b10101000101010 # fail sigma ieie
        
            bitmap = photons[selected_medium_or_control_photons[0]].vidNestedWPBitmap & mask1   
            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",1) #all cuts applied
            elif (bitmap == mask2):
                self.out.fillBranch("photon_selection",2) # fail Isopho
            elif (bitmap == mask3):
                self.out.fillBranch("photon_selection",3) # fail IsoNeu
            elif (bitmap == mask4):
                self.out.fillBranch("photon_selection",4) # fail Isoch
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",5) # fail sigma ieie
            #pass_selection1 && (photon_selection==1 || photon_selection==5) -> remove the sieie requirement in the full ID that can build data/true template
            #pass_selection1 && (photon_selection==2 || photon_selection==3 || photon_selection==4 || photon_selection ==5 )->build fake photon enriched sample
            else:
                assert(0)
        self.out.fillBranch("photonet",photons[selected_medium_or_control_photons[0]].pt)
        self.out.fillBranch("photoneta",photons[selected_medium_or_control_photons[0]].eta)
        self.out.fillBranch("photonphi",photons[selected_medium_or_control_photons[0]].phi)
        self.out.fillBranch("photonchiso",photons[selected_medium_or_control_photons[0]].pfRelIso03_chg*photons[selected_medium_or_control_photons[0]].pt)
        self.out.fillBranch("photonsieie",photons[selected_medium_or_control_photons[0]].sieie)
        self.out.fillBranch("photon_isprompt",photon_isprompt)

        if pass_selection2: # pass_selection1 and pass_selection1 can appear meantime
            # photon_gen_matching=-10
            photon_isprompt =-10
            if hasattr(event, 'nGenPart') :
                for j, genpart in enumerate(genparts):
                    if photons[selected_fake_template_photons[0]].genPartIdx >=0 and genpart.pt > 5 and abs(genpart.pdgId) == 22 and ((genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask)) and deltaR(photons[selected_fake_template_photons[0]].eta,photons[selected_fake_template_photons[0]].phi,genpart.eta,genpart.phi) < 0.3:
                        photon_isprompt =1
                        break
        self.out.fillBranch("photonet_f",photons[selected_fake_template_photons[0]].pt)
        self.out.fillBranch("photoneta_f",photons[selected_fake_template_photons[0]].eta)
        self.out.fillBranch("photonphi_f",photons[selected_fake_template_photons[0]].phi)
        self.out.fillBranch("photonchiso_f",photons[selected_fake_template_photons[0]].pfRelIso03_chg*photons[selected_fake_template_photons[0]].pt)
        self.out.fillBranch("photonsieie_f",photons[selected_fake_template_photons[0]].sieie)
        self.out.fillBranch("photon_isprompt_f",photon_isprompt)

        if hasattr(event,'Pileup_nPU'):    
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)
    
        if hasattr(event,'Pileup_nTrueInt'):    
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)

        print 'channel', channel,'mu_pass:',len(muons_select),' ele_pass:',len(electrons_select),
        print 'photon_pass:',len(selected_medium_or_control_photons),' is photon real ',photon_isprompt

        # self.out.fillBranch("njets50",njets50)
        # self.out.fillBranch("njets40",njets40)
        # self.out.fillBranch("njets30",njets30)
        # self.out.fillBranch("njets20",njets20)
        # self.out.fillBranch("njets15",njets15)
        # self.out.fillBranch("n_bjets",n_bjets)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("metup",sqrt(pow(event.MET_pt*cos(event.MET_phi) + event.MET_MetUnclustEnUpDeltaX,2) + pow(event.MET_pt*sin(event.MET_phi) + event.MET_MetUnclustEnUpDeltaY,2)))
        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimetphi",event.PuppiMET_phi)
        self.out.fillBranch("rawmet",event.RawMET_pt)
        self.out.fillBranch("rawmetphi",event.RawMET_phi)
        self.out.fillBranch("metphi",event.MET_phi)
        # self.out.fillBranch("njets_fake", njets_fake)
        # self.out.fillBranch("njets_fake_template", njets_fake)
        return True

fakePhoton_Module = lambda: ZZG_Producer()

