
if [[ "x${1}" == "x2018" ]]
then 
    ecoh "2018 data"
    crab submit -c cfg2018_data/DoubleMuon_Run2018A_cfg.py  &
    crab submit -c cfg2018_data/DoubleMuon_Run2018B_cfg.py  &
    crab submit -c cfg2018_data/DoubleMuon_Run2018C_cfg.py  &
    crab submit -c cfg2018_data/DoubleMuon_Run2018D_cfg.py  &
    crab submit -c cfg2018_data/EGamma_Run2018A_cfg.py  &
    crab submit -c cfg2018_data/EGamma_Run2018B_cfg.py  &
    crab submit -c cfg2018_data/EGamma_Run2018C_cfg.py  &
    crab submit -c cfg2018_data/EGamma_Run2018D_cfg.py  &
    crab submit -c cfg2018_data/MuonEG_Run2018A_cfg.py  &
    crab submit -c cfg2018_data/MuonEG_Run2018B_cfg.py  &
    crab submit -c cfg2018_data/MuonEG_Run2018C_cfg.py  &
    crab submit -c cfg2018_data/MuonEG_Run2018D_cfg.py  &
    crab submit -c cfg2018_data/SingleMuon_Run2018A_cfg.py  &
    crab submit -c cfg2018_data/SingleMuon_Run2018B_cfg.py  &
    crab submit -c cfg2018_data/SingleMuon_Run2018C_cfg.py  &
    crab submit -c cfg2018_data/SingleMuon_Run2018D_cfg.py  &
elif [[ "x${1}" == "x2017" ]]
then 
    echo " 2017 data"
    crab submit -c cfg2017_data/DoubleEG_Run2017B_cfg.py &
    crab submit -c cfg2017_data/DoubleEG_Run2017C_cfg.py &
    crab submit -c cfg2017_data/DoubleEG_Run2017D_cfg.py &
    crab submit -c cfg2017_data/DoubleEG_Run2017E_cfg.py &
    crab submit -c cfg2017_data/DoubleEG_Run2017F_cfg.py &
    crab submit -c cfg2017_data/DoubleMuon_Run2017B_cfg.py &
    crab submit -c cfg2017_data/DoubleMuon_Run2017B_cfg.pyc &
    crab submit -c cfg2017_data/DoubleMuon_Run2017C_cfg.py &
    crab submit -c cfg2017_data/DoubleMuon_Run2017D_cfg.py &
    crab submit -c cfg2017_data/DoubleMuon_Run2017E_cfg.py &
    crab submit -c cfg2017_data/DoubleMuon_Run2017F_cfg.py &
    crab submit -c cfg2017_data/DoubleMuon_Run2017G_cfg.py &
    crab submit -c cfg2017_data/DoubleMuon_Run2017H_cfg.py &
    crab submit -c cfg2017_data/MuonEG_Run2017B_cfg.py &
    crab submit -c cfg2017_data/MuonEG_Run2017C_cfg.py &
    crab submit -c cfg2017_data/MuonEG_Run2017D_cfg.py &
    crab submit -c cfg2017_data/MuonEG_Run2017E_cfg.py &
    crab submit -c cfg2017_data/MuonEG_Run2017F_cfg.py &
    crab submit -c cfg2017_data/SingleElectron_Run2017B_cfg.py &
    crab submit -c cfg2017_data/SingleElectron_Run2017C_cfg.py &
    crab submit -c cfg2017_data/SingleElectron_Run2017D_cfg.py &
    crab submit -c cfg2017_data/SingleElectron_Run2017E_cfg.py &
    crab submit -c cfg2017_data/SingleElectron_Run2017F_cfg.py &
    crab submit -c cfg2017_data/SingleMuon_Run2017B_cfg.py &
    crab submit -c cfg2017_data/SingleMuon_Run2017C_cfg.py &
    crab submit -c cfg2017_data/SingleMuon_Run2017D_cfg.py &
    crab submit -c cfg2017_data/SingleMuon_Run2017E_cfg.py &
    crab submit -c cfg2017_data/SingleMuon_Run2017F_cfg.py &
    crab submit -c cfg2017_data/SingleMuon_Run2017G_cfg.py &
    crab submit -c cfg2017_data/SingleMuon_Run2017H_cfg.py &

elif [[ "x${1}" == "x2016" ]]
then 
    echo "2016 data"

    crab submit -c cfg2016_data/DoubleEG_Run2016B_v1_cfg.py &
    crab submit -c cfg2016_data/DoubleEG_Run2016B_v2_cfg.py &
    crab submit -c cfg2016_data/DoubleEG_Run2016C_cfg.py &
    crab submit -c cfg2016_data/DoubleEG_Run2016D_cfg.py &
    crab submit -c cfg2016_data/DoubleEG_Run2016E_cfg.py &
    crab submit -c cfg2016_data/DoubleEG_Run2016F_cfg.py &
    crab submit -c cfg2016_data/DoubleEG_Run2016F_noHIPM_cfg.py &
    crab submit -c cfg2016_data/DoubleEG_Run2016G_cfg.py &
    crab submit -c cfg2016_data/DoubleEG_Run2016H_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016B_v1_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016B_v2_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016C_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016D_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016E_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016F_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016F_noHIPM_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016G_cfg.py &
    crab submit -c cfg2016_data/DoubleMuon_Run2016H_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016B_v1_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016B_v2_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016C_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016D_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016E_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016F_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016F_noHIPM_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016G_cfg.py &
    crab submit -c cfg2016_data/MuonEG_Run2016H_cfg.py &
    crab submit -c cfg2016_data/SingleElectron_Run2016B_v1_cfg.py &
    crab submit -c cfg2016_data/SingleElectron_Run2016B_v2_cfg.py &
    crab submit -c cfg2016_data/SingleElectron_Run2016C_cfg.py &
    crab submit -c cfg2016_data/SingleElectron_Run2016D_cfg.py &
    crab submit -c cfg2016_data/SingleElectron_Run2016F_cfg.py &
    crab submit -c cfg2016_data/SingleElectron_Run2016F_noHIPM_cfg.py &
    crab submit -c cfg2016_data/SingleElectron_Run2016G_cfg.py &
    crab submit -c cfg2016_data/SingleElectron_Run2016H_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016B_v1_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016B_v2_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016C_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016D_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016E_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016F_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016F_noHIPM_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016G_cfg.py &
    crab submit -c cfg2016_data/SingleMuon_Run2016H_cfg.py &

fi
