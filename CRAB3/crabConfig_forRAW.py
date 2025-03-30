import CRABClient
from CRABClient.UserUtilities import config 

config = config()

# config.General.requestName = 'tutorial_Aug2021_Data_analysis'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/afs/cern.ch/user/a/aguven/crab_submissions/CMSSW_13_0_16/src/SoftDisplacedVertices/RECO/configuration/Data_Run2023_RECO.py'
config.JobType.maxMemoryMB = 4000
config.JobType.numCores = 2

config.Data.inputDataset = '/JetMET1/Run2023D-v1/RAW'
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
config.Data.publication = True
config.Data.outputDatasetTag = 'Run2023D1_aod_v1'
config.Data.lumiMask = '/afs/cern.ch/user/a/aguven/crab_submissions/CMSSW_13_0_16/src/SoftDisplacedVertices/RECO/testK/lumi_mask.txt'
config.Data.inputBlocks = ['/JetMET1/Run2023D-v1/RAW#de506cf2-7ae2-42a3-a997-8a9d928f200b']
# config.Data.partialDataset = True
# config.Data.ignoreLocality = True

# config.Site.ignoreGlobalBlacklist = True
# config.Site.blacklist=["T2_BR_SPRACE"]
# config.Site.whitelist=["T2_AT_Vienna"]

config.Site.storageSite = "T2_AT_Vienna"
