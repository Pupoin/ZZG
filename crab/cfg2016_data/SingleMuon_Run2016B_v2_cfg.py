from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = 'SingleMuon_Run2016B_v2_2016'
config.General.transferLogs= True
config.General.workArea = 'crab2016'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['../scripts/haddnano.py', '../python/fakePhoton/ZZG_postproc.py', '../python/fakePhoton/output_branch.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptArgs = ['kind=data','mode=crab','year=2016','which_data=SingleMuon']
config.JobType.sendPythonFolder  = True

config.section_("Data")
#config.Data.outputPrimaryDataset = 'ZZG_fakePhoton'
config.Data.inputDataset = '/SingleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased' #'LumiBased', 'EventAwareLumiBased'  
config.Data.unitsPerJob = 100
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'

config.Data.outLFNDirBase ='/store/user/zhyuan/ZZG_2016_v1/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = 'SingleMuon_Run2016B_v2_2016'

config.section_("Site")
config.Site.storageSite = "T3_CH_CERNBOX"
config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']
