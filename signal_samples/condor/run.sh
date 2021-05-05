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
cmsRun SMP-RunIISummer20UL16wmLHEGEN-00004_1_cfg.py

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
cmsRun SMP-RunIISummer20UL16SIM-00021_1_cfg.py

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
cmsRun SMP-RunIISummer20UL16DIGIPremix-00018_1_cfg.py

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
cmsRun SMP-RunIISummer20UL16HLT-00021_1_cfg.py

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
cmsRun SMP-RunIISummer20UL16RECO-00021_1_cfg.py

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
cmsRun SMP-RunIISummer20UL16MiniAOD-00021_1_cfg.py

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
cmsRun SMP-RunIISummer20UL16NanoAODv2-00047_1_cfg.pys