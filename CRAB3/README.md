## CRAB Configuration Script

&nbsp;

```python
import CRABClient
from CRABClient.UserUtilities import config 

config = config()
## If left unset CRAB will create one with the timestamp
## e.g. crab_20240229_214555
## config.General.requestName = 'my_unique_request_name'
## workArea will be the folder name
## e.g. the information about your submission will be 
##      written to this directory:
##      crab_projects/crab_20240229_214555
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/configuration/MC_UL18_CustomMiniAOD.py'
config.JobType.maxMemoryMB = 8000
config.JobType.numCores = 4

config.Data.inputDataset = '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic' # FileBased/LumiBased/...
config.Data.publication = True
## It is better to name your output dataset uniquely
## for instance naming them with version numbers
## This way when the dataset is published on DAS,
## it will only list the files from correct submission.
config.Data.outputDatasetTag = 'CustomMiniAOD_pv1'
## partialDataset will not issue TAPERECALL
## it will simply get the available block of data on any DISK
## only complete blocks are considered.
# config.Data.partialDataset = True
## If ignoreLocality = True
## it will run the data at any available site regardless of
## the location. whitelist,blacklist will be respected.
# config.Data.ignoreLocality = True

config.Site.blacklist=["T2_BR_SPRACE"]

config.Site.storageSite = "T2_AT_Vienna"
```

&nbsp;

Check the status of your submission via:

`crab status -d path_to_workArea/request_name`

`crab status -d crab_projects/crab_20240229_214555 --long`

Status might look like this:

```
Jobs status:   failed       		  2.5% (  27/1076)
               finished     		 97.5% (1049/1076)
```

&nbsp;

In the case of failed jobs your options are:

- `crab resubmit`
- `crab recover`
- `crab submit` with lumiMask
- `crab submit` with lumiMask and userInputFiles
- `crab submit` with blackList and rucio

&nbsp;

### resubmit

Most of the time it will not help, but sometimes resubmitting your job can help process the remaining files.

If the failed jobs are due to FileReadError or sorts, hard luck. This means site might have some problems reading the files.

Sometimes CRAB might complain even the resubmission is not possible.

Then, you might like to consider other options.

### recover

`recover` command will look for the unprocessed lumi sections, and submit a new job with a lumi mask specified.

Again, if there are FileReadErrors `recover` might not be able to solve it, as it merely submits the rest one more time.

However, if you use Rucio and get the unprocessed files on your site, you might evade these type errors.

But you must do the following:

- Get the list of unprocessed lumi sections
- Find the files corresponding to these lumi sections.
- Add a Rucio rule to replicate these files to a site where you have some quota.
- Use `crab recover` and hope that your submission will be submitted to your site, as you copied the data to your site already.

These will be covered in the notes: **CRAB Helper Scripts**, and **Rucio Guide** notebooks.

### lumiMask

Specifying `config.Data.lumiMask = 'notFinishedLumis.json'` will set the lumiMask.

Use `crab report` to get `'notFinishedLumis.json'`.

If you choose to set an inputDataset, CRAB will try to access the whole dataset.

If you set `config.Data.partialDataset = True` CRAB will not require the whole dataset to be present.

It will work on individual blocks (a set of files), but the blocks are required to be complete, otherwise submission does not run.

### lumiMask and userInputFiles

This does not work at all.

**One can not specify both the lumiMask and the userInputFiles together.**

## Ultimate Solution

Use Rucio to get the files on CLIP.

Specify the lumi mask from notPublishedLumis.json

Specify the whitelist to the T2_AT_VIENNA

CRAB will run the job at site.

&nbsp;

## RAW Processing

Sometimes RAW datasets are too huge that CRAB3 does not let you issue a TAPERECALL on the whole dataset. Instead you would need to run it on a list of blocks.

&nbsp;

&nbsp;

#### REF LINKS

- https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePoolInputSources
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Using_a_lumi_mask

&nbsp;

&nbsp;