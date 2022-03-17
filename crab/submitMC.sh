
#!/bin/bash
# Declare a dictionary.
declare -A name_path
name_path=( 
# [ZZ]='/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM' 
#[WZG]='/WZG_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM' 
#[ttZJ]='/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM' 
# [WWZ]='/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1_ext1-v1/NANOAODSIM' 
[ggZZ_ZZTo2e2mu]='/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
[ggZZ_ZZTo2e2tau]='/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
[ggZZ_ZZTo2mu2tau]='/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
[ggZZ_ZZTo2e2nu]='/GluGluToContinToZZTo2e2nu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
[ggZZ_ZZTo4mu]='/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
[ggZZ_ZZTo2mu2nu]='/GluGluToContinToZZTo2mu2nu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
[ggZZ_ZZTo4tau]='/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
[ggZZ_ZZTo4e]='/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
)

for name in ${!name_path[@]};
do
    echo "${name}, ${name_path[${name}]}"
    cp base_MC_2018_cfg.py ${name}_MC_2018_cfg.py

    sed "s/ZA_MC_/${name}_MC_/g" -i ${name}_MC_2018_cfg.py
    sed "s|config.Data.inputDataset.*|config.Data.inputDataset=\'${name_path[${name}]}\'|g" -i ${name}_MC_2018_cfg.py
    crab submit ${name}_MC_2018_cfg.py > log.sub_${name}_MC_2018_cfg &
done


