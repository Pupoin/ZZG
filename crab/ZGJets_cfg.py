from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = 'ZGJets'
config.General.transferLogs= True
config.General.workArea = 'crab2018'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['../scripts/haddnano.py', '../python/fakePhoton/ZZG_postproc.py', '../python/fakePhoton/output_branch.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptArgs = ['kind=MC','mode=crab','year=2018','which_data=ZGJets']
config.JobType.sendPythonFolder  = True

config.section_("Data")
#config.Data.outputPrimaryDataset = 'ZZG_fakePhoton'
config.Data.inputDataset = '/ZGJetsToLLG_012nlo3lo_13TeV-sherpa/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased' #'LumiBased', 'EventAwareLumiBased'  
config.Data.unitsPerJob = 1
# config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

config.Data.outLFNDirBase ='/store/user/zhyuan/ZGJets_mc/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = 'ZGJets'

config.section_("Site")
config.Site.storageSite = "T3_CH_CERNBOX"
config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']

