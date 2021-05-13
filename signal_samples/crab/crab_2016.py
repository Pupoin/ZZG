from WMCore.Configuration import Configuration
config = Configuration()
#increment_seeds=sourceSeed,g4SimHits

config.section_("General")
config.General.requestName = 'ZZA_signal'
config.General.workArea = 'crab_projects'
config.General.transferLogs = True
config.General.transferOutputs = True

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'SMP-RunIISummer20UL16NanoAODv2-00047_1_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.inputFiles = ['SMP-RunIISummer20UL16NanoAODv2-00047_1_cfg.py, SMP-RunIISummer20UL16MiniAOD-00021.root']
config.JobType.OutputFiles = ['SMP-RunIISummer20UL16MiniAOD-00021.root, SMP-RunIISummer20UL16NanoAODv2-00047.root']
config.JobType.scriptExe = 'wrapper_2016run.sh'


config.section_("Data")
config.Data.splitting = 'Automatic'
config.Data.outputPrimaryDataset = 'ZZA_signal'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 10000
NJOBS = 25  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'ZZA_signal_1'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX' # Should change to the site that you have write permission