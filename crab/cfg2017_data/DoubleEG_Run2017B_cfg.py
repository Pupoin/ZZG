from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = 'DoubleEG_Run2017B_2017'
config.General.transferLogs= True
config.General.workArea = 'crab2017'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['../scripts/haddnano.py', '../python/fakePhoton/ZZG_postproc.py', '../python/fakePhoton/output_branch.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptArgs = ['kind=data','mode=crab','year=2017','which_data=DoubleEG']
config.JobType.sendPythonFolder  = True

config.section_("Data")
#config.Data.outputPrimaryDataset = 'ZZG_fakePhoton'
config.Data.inputDataset = '/DoubleEG/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased' #'LumiBased', 'EventAwareLumiBased'  
config.Data.unitsPerJob = 100
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'

config.Data.outLFNDirBase ='/store/user/zhyuan/ZZG_2017_v1/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = 'DoubleEG_Run2017B_2017'

config.section_("Site")
config.Site.storageSite = "T3_CH_CERNBOX"
config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']
