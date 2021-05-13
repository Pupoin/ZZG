#! /bin/bash
# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
# export Proxy_path=/afs/cern.ch/user/s/sdeng/.krb5/x509up_u109738
# voms-proxy-info -all
# voms-proxy-info -all -file $Proxy_path
. mygz-cmssw_setup.sh

# LHEGen
echo "____ start lhegen ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-f71bc09.tar.gz

SEED=$(($(date +%s) % 100 + 1)) && echo $SEED
sed -i "s/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int.*$/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int(${SEED})/" SMP-RunIISummer20UL16wmLHEGEN-00004_1_cfg.py 
cmsRun  SMP-RunIISummer20UL16wmLHEGEN-00004_1_cfg.py 


# Sim
echo "____ start Sim ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-f71bc09.tar.gz
cmsRun SMP-RunIISummer20UL16SIM-00021_1_cfg.py 


# digipremix
echo "____ start premix ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-f71bc09.tar.gz
cmsRun SMP-RunIISummer20UL16DIGIPremix-00018_1_cfg.py 

# HLT
echo "____ start HLT ____"
cmssw_setup sandbox-CMSSW_8_0_33_UL-43f25c9.tar.gz
cmsRun SMP-RunIISummer20UL16HLT-00021_1_cfg.py 


# reco
echo "____ start reco ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-f71bc09.tar.gz
cmsRun SMP-RunIISummer20UL16RECO-00021_1_cfg.py 

# miniAod
echo "____ start miniAod ____"
cmssw_setup sandbox-CMSSW_10_6_17_patch1-f71bc09.tar.gz
cmsRun SMP-RunIISummer20UL16MiniAOD-00021_1_cfg.py 

# NanoAod
echo "____ start NanoAod ____"
cmssw_setup sandbox-CMSSW_10_6_19_patch2-66a0ccf.tar.gz
cmsRun SMP-RunIISummer20UL16NanoAODv2-00047_1_cfg.py 

