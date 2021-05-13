from WMCore.Configuration import Configuration
config = Configuration()
#increment_seeds=sourceSeed,g4SimHits

config.section_("General")
config.General.requestName = 'ZZA_signal'
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'NLO_SMP-RunIIFall18wmLHEGS-00093-cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.inputFiles = ['ZZATO4L_4f_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz']

config.section_("Data")
config.Data.splitting = 'Automatic'
config.Data.outputPrimaryDataset = 'MinBias'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 10000
NJOBS = 25  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'ZZA_signal'
config.General.transferLogs = True

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX' # Should change to the site that you have write permission