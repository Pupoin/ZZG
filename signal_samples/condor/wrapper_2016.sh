#! /bin/bash
# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
# export Proxy_path=/afs/cern.ch/user/s/sdeng/.krb5/x509up_u109738
# voms-proxy-info -all
# voms-proxy-info -all -file $Proxy_path


# LHEGen
echo "____ start lhegen ____"
export SCRAM_ARCH=slc7_amd64_gcc700
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SMP-RunIISummer20UL16wmLHEGEN-00004 --retry 3 --create-dirs -o Configuration/GenProduction/python/SMP-RunIISummer20UL16wmLHEGEN-00004-fragment.py
sed -i "s|/cvmfs/cms.cern.ch/.*tar.xz|/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc7_amd64_gcc700/13TeV/madgraph/V5_2.6.5/ZZATo4L/ZZGTO4L_4f_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz|"  Configuration/GenProduction/python/SMP-RunIISummer20UL16wmLHEGEN-00004-fragment.py
scram b
cd ../..

EVENTS=100
cmsDriver.py Configuration/GenProduction/python/SMP-RunIISummer20UL16wmLHEGEN-00004-fragment.py \
    --python_filename SMP-RunIISummer20UL16wmLHEGEN-00004_1_cfg.py --eventcontent RAWSIM,LHE \
    --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE \
    --fileout file:SMP-RunIISummer20UL16wmLHEGEN-00004.root --conditions 106X_mcRun2_asymptotic_v13 \
    --beamspot Realistic25ns13TeV2016Collision \
    --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" \
    --step LHE,GEN --geometry DB:Extended --era Run2_2016 --no_exec --mc -n $EVENTS
cmsRun  SMP-RunIISummer20UL16wmLHEGEN-00004_1_cfg.py 


# Sim
echo "____ start Sim ____"
export SCRAM_ARCH=slc7_amd64_gcc700
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL16SIM-00021_1_cfg.py \
    --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier GEN-SIM --fileout file:SMP-RunIISummer20UL16SIM-00021.root \
    --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision \
    --step SIM --geometry DB:Extended --filein file:SMP-RunIISummer20UL16wmLHEGEN-00004.root \
    --era Run2_2016 --runUnscheduled --no_exec --mc -n $EVENTS
cmsRun SMP-RunIISummer20UL16SIM-00021_1_cfg.py 


# digipremix
echo "____ start premix ____"
export SCRAM_ARCH=slc7_amd64_gcc700
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL16DIGIPremix-00018_1_cfg.py \
    --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier GEN-SIM-DIGI --fileout file:SMP-RunIISummer20UL16DIGIPremix-00018.root \
    --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX" \
    --conditions 106X_mcRun2_asymptotic_v13 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 \
    --geometry DB:Extended --filein file:SMP-RunIISummer20UL16SIM-00021.root \
    --datamix PreMix --era Run2_2016 --runUnscheduled --no_exec --mc -n $EVENTS
cmsRun SMP-RunIISummer20UL16DIGIPremix-00018_1_cfg.py 

# HLT
echo "____ start HLT ____"
export SCRAM_ARCH=slc7_amd64_gcc530
if [ -r CMSSW_8_0_33_UL/src ] ; then
  echo release CMSSW_8_0_33_UL already exists
else
  scram p CMSSW CMSSW_8_0_33_UL
fi
cd CMSSW_8_0_33_UL/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL16HLT-00021_1_cfg.py \
    --eventcontent RAWSIM --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*" \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier GEN-SIM-RAW --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" \
    --fileout file:SMP-RunIISummer20UL16HLT-00021.root --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 \
    --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' \
    --step HLT:25ns15e33_v4 --geometry DB:Extended \
    --filein file:SMP-RunIISummer20UL16DIGIPremix-00018.root \
    --era Run2_2016 --no_exec --mc -n $EVENTS 
cmsRun SMP-RunIISummer20UL16HLT-00021_1_cfg.py 


# reco
echo "____ start reco ____"
export SCRAM_ARCH=slc7_amd64_gcc700
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL16RECO-00021_1_cfg.py \
    --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier AODSIM --fileout file:SMP-RunIISummer20UL16RECO-00021.root \
    --conditions 106X_mcRun2_asymptotic_v13 --step RAW2DIGI,L1Reco,RECO,RECOSIM \
    --geometry DB:Extended --filein file:SMP-RunIISummer20UL16HLT-00021.root \
    --era Run2_2016 --runUnscheduled --no_exec --mc -n $EVENTS 
cmsRun SMP-RunIISummer20UL16RECO-00021_1_cfg.py 

# miniAod
echo "____ start miniAod ____"
export SCRAM_ARCH=slc7_amd64_gcc700
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
# --filein "dbs:/WZJJ_EWK_TLPolarization_TuneCP5_13TeV_madgraph-madspin-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/AODSIM" \
cmsDriver.py  --python_filename SMP-RunIISummer20UL16MiniAOD-00021_1_cfg.py \
    --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier MINIAODSIM --fileout file:SMP-RunIISummer20UL16MiniAOD-00021.root \
    --conditions 106X_mcRun2_asymptotic_v13 --step PAT --geometry DB:Extended \
    --filein file:SMP-RunIISummer20UL16RECO-00021.root \
    --era Run2_2016 --runUnscheduled --no_exec --mc -n $EVENTS 
cmsRun SMP-RunIISummer20UL16MiniAOD-00021_1_cfg.py 

# NanoAod
echo "____ start NanoAod ____"
export SCRAM_ARCH=slc7_amd64_gcc700
if [ -r CMSSW_10_6_19_patch2/src ] ; then
  echo release CMSSW_10_6_19_patch2 already exists
else
  scram p CMSSW CMSSW_10_6_19_patch2
fi
cd CMSSW_10_6_19_patch2/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL16NanoAODv2-00047_1_cfg.py \
    --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier NANOAODSIM --fileout file:SMP-RunIISummer20UL16NanoAODv2-00047.root \
    --conditions 106X_mcRun2_asymptotic_v15 --step NANO \
    --filein file:SMP-RunIISummer20UL16MiniAOD-00021.root \
    --era Run2_2016,run2_nanoAOD_106Xv1 --no_exec --mc -n $EVENTS 
cmsRun SMP-RunIISummer20UL16NanoAODv2-00047_1_cfg.py 

