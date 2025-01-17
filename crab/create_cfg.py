import argparse
import os
import importlib
import shutil

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-v','--version', help='which version should be', default='1')
parser.add_argument('-u','--units_per_job', help='how many units in one job', default='1')
parser.add_argument('-k','--kind', help='Is it for data? Default: False', default= 'MC')
parser.add_argument('-p','--modulePath', help='where to find the module',default= '../python/fakePhoton')
parser.add_argument('-m','--mode', help='crab? local? condor?',default= 'local')
group = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
group.add_argument('-y','--year', help='run on which year', choices=('2016','2017','2018'))
group.add_argument('-a','--all', help='chose all jobs',action='store_true', default= False)
args = parser.parse_args()

version = f'_v{args.version}/'

datasets={
    'data':{
        '2018':'dataset_2018_data_nano_v9',
        '2017':'dataset_2017_data_nano_v9',
        '2016':'dataset_2016_data_nano_v9',
    },
    'mc':{
        '2018':'dataset_2018_mc_nano_v7',
        '2017':'dataset_2017_mc_nano_v7',
        '2016':'dataset_2016_mc_nano_v7',
    }
}

def new_py(year,kind,mode,unitsPerJob,modulePath):
    signals=[]
    _Samples={}
    if year == '2018':
        outdir = '/store/user/zhyuan/ZZG_2018' + version
        golden_json = "\'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt\'"
        if 'data' in kind:
            mymodule=importlib.import_module(datasets['data'][year])
            _Samples=mymodule.Samples
            cfg_dir = os.getcwd() + '/cfg2018_data/'
            # cfg_dir = os.getcwd() + '/'
        else:
            mymodule=importlib.import_module(datasets['mc'][year])
            _Samples=mymodule.Samples
            cfg_dir = os.getcwd() + '/cfg2018_mc/'
    elif year == '2017':
        outdir = '/store/user/zhyuan/ZZG_2017' + version
        golden_json = "\'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt\'"
        if 'data' in kind:
            mymodule=importlib.import_module(datasets['data'][year])
            _Samples=mymodule.Samples
            cfg_dir = os.getcwd() + '/cfg2017_data/'
        else:
            mymodule=importlib.import_module(datasets['mc'][year])
            _Samples=mymodule.Samples
            cfg_dir = os.getcwd() + '/cfg2017_mc/'
    elif year == '2016':
        cfg_dir = os.getcwd() + '/cfg2016/'
        outdir = '/store/user/zhyuan/ZZG_2016' + version
        golden_json = "\'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt\'"
        if 'data' in kind:
            mymodule=importlib.import_module(datasets['data'][year])
            _Samples=mymodule.Samples
            cfg_dir = os.getcwd() + '/cfg2016_data/'
        else:
            mymodule=importlib.import_module(datasets['data'][year])
            _Samples=mymodule.Samples
            cfg_dir = os.getcwd() + '/cfg2016_mc/'
    else:
        return
    
    #site = "T2_CN_Beijing"
    site = "T3_CH_CERNBOX"

    print(f">>>>>>>>>>>>>>>>>>>> created directory for {year} : {cfg_dir}")
    print(">>>>>>>>>>>>>>>>>>>> the created configuration files:")
    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)

    #if is_data:
        # shutil.copy2(f'PSet_data_{year}.py',f'{cfg_dir}/PSet.py')
        #shutil.copy2(f'crab_script_data_{year}.py',f'{cfg_dir}/crab_script.py')
        # shutil.copy2(f'crab_script_data_{year}.sh',f'{cfg_dir}/crab_script.sh')
    #else:
        # shutil.copy2('PSet.py',f'{cfg_dir}/PSet.py')
        #shutil.copy2(f'crab_script_mc_{year}.py',f'{cfg_dir}/crab_script.py')
        # shutil.copy2(f'crab_script_mc_{year}.sh',f'{cfg_dir}/crab_script.sh')

    for iSample in _Samples:
        file = iSample + '_cfg.py'
        print(file)
        if 'data' in kind:
            dataset=_Samples[iSample]['nanoAOD']
            #script = f'crab_script_data_{year}.py'
            if 'DoubleMuon' in dataset:
                which_data = 'DoubleMuon'
            elif 'MuonEG' in dataset:
                which_data = 'MuonEG'
            elif 'SingleMuon' in dataset:
                which_data = 'SingleMuon'
            elif 'EGamma' in dataset:
                which_data = 'EGamma'
            elif 'SingleElectron' in dataset:
                which_data = 'SingleElectron'
            elif 'DoubleEG' in dataset:
                which_data = 'DoubleEG'
            else:
                print('unkown dataset name in kind')
            # split = 'Automatic'
            #split = 'FileBased'
            split = 'LumiBased'
            lumiMask = f"config.Data.lumiMask = {golden_json}" 
            inbranch_file='input_branch.txt'
            outbranch_file='output_branch.txt'
            scriptargs=f"['kind={kind}','mode={mode}','year={year}','which_data={which_data}']"
        else:
            dataset=_Samples[iSample]['nanoAODSIM']
            which_data='MC'
            #script = f'crab_script_{year}.py'
            split = 'FileBased'
            # split = 'LumiBased'
            #split = 'Automatic'
            lumiMask = "config.Data.totalUnits = -1"
            if iSample in signals:
                inbranch_file=f'ZZG_keep_and_drop_{year}.txt'
                outbranch_file=f'ZZG_outbranch_sig_{year}.txt'
                scriptargs=f"['kind={kind}','mode={mode}','year={year}','which_data={which_data}']"
            else:
                inbranch_file=f'ZZG_keep_and_drop_{year}.txt'
                outbranch_file=f'ZZG_outbranch_mc_{year}.txt'
                scriptargs=f"['kind={kind}','mode={mode}','year={year}','which_data={which_data}']"

        file_content = ""
        file_content += "from WMCore.Configuration import Configuration\n"
        #file_content += "from CRABClient.UserUtilities import config\n"
        file_content += "\n"
        file_content += "config = Configuration()\n"
        file_content += "\n"
        file_content += "config.section_(\"General\")\n"
        file_content += f"config.General.requestName = \'{iSample + '_' + year}\'\n"
        file_content += "config.General.transferLogs= True\n"
        file_content += f"config.General.workArea = \'crab{year}\'\n"
#        file_content += f"config.JobType.allowUndistributedCMSSW = True\n"
        file_content += "\n"
        file_content += "config.section_(\"JobType\")\n"
        file_content += "config.JobType.pluginName = \'Analysis\'\n"
        file_content += "config.JobType.psetName = \'PSet.py\'\n"
        file_content += f"config.JobType.scriptExe = \'crab_script.sh\'\n" 
        file_content += f"config.JobType.inputFiles = [\'../scripts/haddnano.py', \'{modulePath}/ZZG_postproc.py\', \'{modulePath}/{outbranch_file}\'] #hadd nano will not be needed once nano tools are in cmssw\n"
        file_content += f"config.JobType.scriptArgs = {scriptargs}\n"
        file_content += "config.JobType.sendPythonFolder  = True\n"
        file_content += "\n"
        file_content += "config.section_(\"Data\")\n"
        file_content += "#config.Data.outputPrimaryDataset = \'ZZG_fakePhoton\'\n"
        file_content += f"config.Data.inputDataset = \'{dataset}\'\n"
        file_content += "#config.Data.inputDBS = \'phys03\'\n"
        file_content += "config.Data.inputDBS = \'global\'\n"
        file_content += f"config.Data.splitting = \'{split}\' #\'LumiBased\', \'EventAwareLumiBased\'  \n" 
        # file_content += "#config.Data.splitting = \'EventAwareLumiBased\'\n"
        file_content += f"config.Data.unitsPerJob = {unitsPerJob}\n" 
        file_content += f"{lumiMask}\n"
        file_content += "\n"
        file_content += f"config.Data.outLFNDirBase =\'{outdir}\'\n"
        file_content += "config.Data.publication = False\n"
        file_content += "config.Data.ignoreLocality = True\n"
        file_content += "config.Data.allowNonValidInputDataset = True\n"
        file_content += f"config.Data.outputDatasetTag = \'{iSample + '_' + year}\'\n"
        file_content += "\n"
        file_content += "config.section_(\"Site\")\n"
        file_content += f"config.Site.storageSite = \"{site}\"\n"
        file_content += "config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']\n"
        file_content += "\n"

        tmp = open(cfg_dir + str(file), "w")
        tmp.write(file_content)

if __name__ == '__main__':
    if args.all:
        new_py('2016',args.kind,args.mode,args.units_per_job,args.modulePath)
        new_py('2017',args.kind,args.mode,args.units_per_job,args.modulePath)
        new_py('2018',args.kind,args.mode,args.units_per_job,args.modulePath)
    else:
        new_py(args.year,args.kind,args.mode,args.units_per_job,args.modulePath)
