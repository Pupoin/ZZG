from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = 'ggZZ_ZZTo4mu_MC_2018'
config.General.transferLogs= True
config.General.workArea = 'crabggZZ2018'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['../scripts/haddnano.py', '../python/fakePhoton/ZZG_postproc.py', '../python/fakePhoton/output_branch.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptArgs = ['kind=MC','mode=crab','year=2018','which_data=ggZZ_ZZTo4mu_MC_2018']
config.JobType.sendPythonFolder  = True

config.section_("Data")
#config.Data.outputPrimaryDataset = 'ZZG_fakePhoton'
config.Data.inputDataset='/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
# config.Data.userInputFiles = ['root://eos/user/z/zhyuan/zzg_signal/ZZG2018.root']
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'FileBased'#"LumiBased",'EventAwareLumiBased'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 80000 
# config.Data.totalUnits = 10
# config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'

config.Data.outLFNDirBase ='/store/user/zhyuan/ggZZ_MC_2018_v1/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = 'ggZZ_ZZTo4mu_MC_2018'

config.section_("Site")
config.Site.storageSite = "T3_CH_CERNBOX"
config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']

