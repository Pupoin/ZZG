#! /bin/bash
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
. mygz-cmssw_setup.sh

# LHEGen
echo "____ start lhegen ____"
cmssw_setup sandbox-CMSSW_10_6_18-e37c685.tar.gz

SEED=$(($(date +%s) % 100 + 1)) && echo $SEED
sed -i "s/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int.*$/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int(${SEED})/" SMP-RunIISummer20UL16wmLHEGENAPV-00004_1_cfg.py
cmsRun  SMP-RunIISummer20UL16wmLHEGENAPV-00004_1_cfg.py


# Sim
echo "____ start Sim ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-aa4ec67.tar.gz
cmsRun SMP-RunIISummer20UL16SIMAPV-00014_1_cfg.py


# digipremix
echo "____ start premix ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-aa4ec67.tar.gz
cmsRun SMP-RunIISummer20UL16DIGIPremixAPV-00007_1_cfg.py

# HLT
echo "____ start HLT ____"
cmssw_setup sandbox-CMSSW_8_0_33_UL-0e2eb95.tar.gz
cmsRun SMP-RunIISummer20UL16HLTAPV-00014_1_cfg.py


# reco
echo "____ start reco ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-aa4ec67.tar.gz
cmsRun SMP-RunIISummer20UL16RECOAPV-00014_1_cfg.py

# miniAod
echo "____ start miniAod ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-aa4ec67.tar.gz
cmsRun SMP-RunIISummer20UL16MiniAODAPV-00014_1_cfg.py

# NanoAod
echo "____ start NanoAod ____"
cmssw_setup sandbox-CMSSW_10_6_19_patch2-0147398.tar.gz
cmsRun SMP-RunIISummer20UL16NanoAODAPVv2-00034_1_cfg.py
echo "_____________________"
pwd
ls -lvh
