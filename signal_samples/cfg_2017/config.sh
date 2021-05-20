#! /bin/bash
# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
# export Proxy_path=/afs/cern.ch/user/s/sdeng/.krb5/x509up_u109738
# voms-proxy-info -all
# voms-proxy-info -all -file $Proxy_path
EVENTS=2000

# LHEGen
echo "____ start lhegen ____"
export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SMP-RunIISummer20UL17wmLHEGEN-00001 --retry 3 --create-dirs -o Configuration/GenProduction/python/SMP-RunIISummer20UL17wmLHEGEN-00001-fragment.py
sed -i "s|/cvmfs/cms.cern.ch/.*tar.xz|/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc7_amd64_gcc700/13TeV/madgraph/V5_2.6.5/ZZATo4L/ZZGTO4L_4f_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz|"  Configuration/GenProduction/python/SMP-RunIISummer20UL*wmLHEGEN-*-fragment.py
SEED=$(($(date +%s) % 100 + 1)) && echo $SEED
scram b
cd ../..
cmsDriver.py Configuration/GenProduction/python/SMP-RunIISummer20UL17wmLHEGEN-00001-fragment.py \
  --python_filename SMP-RunIISummer20UL17wmLHEGEN-00001_1_cfg.py --eventcontent RAWSIM,LHE \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier GEN,LHE --fileout file:SMP-RunIISummer20UL17wmLHEGEN-00001.root \
  --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision \
  --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" \
  --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" \
  --step LHE,GEN --geometry DB:Extended --era Run2_2017 --no_exec --mc -n $EVENTS || exit $? ;
#cmsRun SMP-RunIISummer20UL17wmLHEGEN-00001_1_cfg.py



# Sim
echo "____ start Sim ____"
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17SIM-00014_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:SMP-RunIISummer20UL17SIM-00014.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step SIM --geometry DB:Extended --filein file:SMP-RunIISummer20UL17wmLHEGEN-00001.root --era Run2_2017 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;
#cmsRun SMP-RunIISummer20UL17SIM-00014_1_cfg.py

# digipremix
echo "____ start premix ____"
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17DIGIPremix-00014_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:SMP-RunIISummer20UL17DIGIPremix-00014.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX" --conditions 106X_mc2017_realistic_v6 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:SMP-RunIISummer20UL17SIM-00014.root --datamix PreMix --era Run2_2017 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;
#cmsRun SMP-RunIISummer20UL17DIGIPremix-00014_1_cfg.py

# HLT
echo "____ start HLT ____"
if [ -r CMSSW_9_4_14_UL_patch1/src ] ; then
  echo release CMSSW_9_4_14_UL_patch1 already exists
else
  scram p CMSSW CMSSW_9_4_14_UL_patch1
fi
cd CMSSW_9_4_14_UL_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17HLT-00013_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:SMP-RunIISummer20UL17HLT-00013.root --conditions 94X_mc2017_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2e34v40 --geometry DB:Extended --filein file:SMP-RunIISummer20UL17DIGIPremix-00014.root --era Run2_2017 --no_exec --mc -n $EVENTS || exit $? ;
#cmsRun SMP-RunIISummer20UL17HLT-00013_1_cfg.py

# reco
echo "____ start reco ____"
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17RECO-00013_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:SMP-RunIISummer20UL17RECO-00013.root --conditions 106X_mc2017_realistic_v6 --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --filein file:SMP-RunIISummer20UL17HLT-00013.root --era Run2_2017 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;
#cmsRun SMP-RunIISummer20UL17RECO-00013_1_cfg.py

# miniAod
echo "____ start miniAod ____"
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17MiniAOD-00013_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:SMP-RunIISummer20UL17MiniAOD-00013.root --conditions 106X_mc2017_realistic_v6 --step PAT --geometry DB:Extended --filein "dbs:/WZJJ_EWK_InclusivePolarization_TuneCP5_13TeV_madgraph-madspin-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM" --era Run2_2017 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;
#cmsRun SMP-RunIISummer20UL17MiniAOD-00013_1_cfg.py

# NanoAod
echo "____ start NanoAod ____"
if [ -r CMSSW_10_6_19_patch2/src ] ; then
  echo release CMSSW_10_6_19_patch2 already exists
else
  scram p CMSSW CMSSW_10_6_19_patch2
fi
cd CMSSW_10_6_19_patch2/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17NanoAODv2-00036_1_cfg.py \
  --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier NANOAODSIM --fileout file:SMP-RunIISummer20UL17NanoAODv2-00036.root \
  --conditions 106X_mc2017_realistic_v8 --step NANO \
  --filein "dbs:/WZJJ_EWK_InclusivePolarization_TuneCP5_13TeV_madgraph-madspin-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM" \
  --era Run2_2017,run2_nanoAOD_106Xv1 --no_exec --mc -n $EVENTS || exit $? ;
#cmsRun SMP-RunIISummer20UL17NanoAODv2-00036_1_cfg.py
