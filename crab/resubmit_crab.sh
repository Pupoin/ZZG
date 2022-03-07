
if [[ "x${1}" == "x2018" ]]
then 
    echo "2018 data"
    crab resubmit crab2018/crab_DoubleMuon_Run2018A_2018
    crab resubmit crab2018/crab_DoubleMuon_Run2018B_2018
    crab resubmit crab2018/crab_DoubleMuon_Run2018C_2018
    crab resubmit crab2018/crab_DoubleMuon_Run2018D_2018
    crab resubmit crab2018/crab_EGamma_Run2018A_2018
    crab resubmit crab2018/crab_EGamma_Run2018B_2018
    crab resubmit crab2018/crab_EGamma_Run2018C_2018
    crab resubmit crab2018/crab_EGamma_Run2018D_2018
    crab resubmit crab2018/crab_MuonEG_Run2018A_2018
    crab resubmit crab2018/crab_MuonEG_Run2018B_2018
    crab resubmit crab2018/crab_MuonEG_Run2018C_2018
    crab resubmit crab2018/crab_MuonEG_Run2018D_2018
    crab resubmit crab2018/crab_SingleMuon_Run2018A_2018
    crab resubmit crab2018/crab_SingleMuon_Run2018B_2018
    crab resubmit crab2018/crab_SingleMuon_Run2018C_2018
    crab resubmit crab2018/crab_SingleMuon_Run2018D_2018
elif [[ "x${1}" == "x2017" ]]
then 
    echo " 2017 data"
    crab status -d crab2017/crab_DoubleEG_Run2017B_2017
    crab status -d crab2017/crab_DoubleEG_Run2017C_2017
    crab status -d crab2017/crab_DoubleEG_Run2017D_2017
    crab status -d crab2017/crab_DoubleEG_Run2017E_2017
    crab status -d crab2017/crab_DoubleEG_Run2017F_2017
    crab status -d crab2017/crab_DoubleMuon_Run2017B_2017
    crab status -d crab2017/crab_DoubleMuon_Run2017C_2017
    crab status -d crab2017/crab_DoubleMuon_Run2017D_2017
    crab status -d crab2017/crab_DoubleMuon_Run2017E_2017
    crab status -d crab2017/crab_DoubleMuon_Run2017F_2017
    crab status -d crab2017/crab_DoubleMuon_Run2017G_2017
    crab status -d crab2017/crab_DoubleMuon_Run2017H_2017
    crab status -d crab2017/crab_MuonEG_Run2017B_2017
    crab status -d crab2017/crab_MuonEG_Run2017C_2017
    crab status -d crab2017/crab_MuonEG_Run2017D_2017
    crab status -d crab2017/crab_MuonEG_Run2017E_2017
    crab status -d crab2017/crab_MuonEG_Run2017F_2017
    crab status -d crab2017/crab_SingleElectron_Run2017B_2017
    crab status -d crab2017/crab_SingleElectron_Run2017C_2017
    crab status -d crab2017/crab_SingleElectron_Run2017D_2017
    crab status -d crab2017/crab_SingleElectron_Run2017E_2017
    crab status -d crab2017/crab_SingleElectron_Run2017F_2017
    crab status -d crab2017/crab_SingleMuon_Run2017B_2017
    crab status -d crab2017/crab_SingleMuon_Run2017C_2017
    crab status -d crab2017/crab_SingleMuon_Run2017D_2017
    crab status -d crab2017/crab_SingleMuon_Run2017E_2017
    crab status -d crab2017/crab_SingleMuon_Run2017F_2017
    crab status -d crab2017/crab_SingleMuon_Run2017G_2017
    crab status -d crab2017/crab_SingleMuon_Run2017H_2017
elif [[ "x${1}" == "x2016" ]]
then 
    echo "2016 data"
    crab status -d crab2016/crab_DoubleEG_Run2016B_v1_2016
    crab status -d crab2016/crab_DoubleEG_Run2016B_v2_2016
    crab status -d crab2016/crab_DoubleEG_Run2016C_2016
    crab status -d crab2016/crab_DoubleEG_Run2016D_2016
    crab status -d crab2016/crab_DoubleEG_Run2016E_2016
    crab status -d crab2016/crab_DoubleEG_Run2016F_2016
    crab status -d crab2016/crab_DoubleEG_Run2016F_noHIPM_2016
    crab status -d crab2016/crab_DoubleEG_Run2016G_2016
    crab status -d crab2016/crab_DoubleEG_Run2016H_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016B_v1_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016B_v2_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016C_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016D_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016E_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016F_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016F_noHIPM_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016G_2016
    crab status -d crab2016/crab_DoubleMuon_Run2016H_2016
    crab status -d crab2016/crab_MuonEG_Run2016B_v1_2016
    crab status -d crab2016/crab_MuonEG_Run2016B_v2_2016
    crab status -d crab2016/crab_MuonEG_Run2016C_2016
    crab status -d crab2016/crab_MuonEG_Run2016D_2016
    crab status -d crab2016/crab_MuonEG_Run2016E_2016
    crab status -d crab2016/crab_MuonEG_Run2016F_2016
    crab status -d crab2016/crab_MuonEG_Run2016F_noHIPM_2016
    crab status -d crab2016/crab_MuonEG_Run2016G_2016
    crab status -d crab2016/crab_MuonEG_Run2016H_2016
    crab status -d crab2016/crab_SingleElectron_Run2016B_v1_2016
    crab status -d crab2016/crab_SingleElectron_Run2016B_v2_2016
    crab status -d crab2016/crab_SingleElectron_Run2016C_2016
    crab status -d crab2016/crab_SingleElectron_Run2016D_2016
    crab status -d crab2016/crab_SingleElectron_Run2016F_2016
    crab status -d crab2016/crab_SingleElectron_Run2016F_noHIPM_2016
    crab status -d crab2016/crab_SingleElectron_Run2016G_2016
    crab status -d crab2016/crab_SingleElectron_Run2016H_2016
    crab status -d crab2016/crab_SingleMuon_Run2016B_v1_2016
    crab status -d crab2016/crab_SingleMuon_Run2016B_v2_2016
    crab status -d crab2016/crab_SingleMuon_Run2016C_2016
    crab status -d crab2016/crab_SingleMuon_Run2016D_2016
    crab status -d crab2016/crab_SingleMuon_Run2016E_2016
    crab status -d crab2016/crab_SingleMuon_Run2016F_2016
    crab status -d crab2016/crab_SingleMuon_Run2016F_noHIPM_2016
    crab status -d crab2016/crab_SingleMuon_Run2016G_2016
    crab status -d crab2016/crab_SingleMuon_Run2016H_2016
fi
