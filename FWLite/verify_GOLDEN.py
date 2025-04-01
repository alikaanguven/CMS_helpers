#!/usr/bin/env python3
import os
import json
import subprocess
from FWCore.PythonUtilities.LumiList import LumiList

CMSSW_BASE = os.environ['CMSSW_BASE']
SDV = os.path.join(CMSSW_BASE, 'src/SoftDisplacedVertices')
GOLDEN_JSON = "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json"

to_process = LumiList(url=GOLDEN_JSON)
processed = LumiList(filename=os.path.join(SDV, "CustomMiniAOD/testK/checks/aggregatedLumis.json"))
residue = to_process - processed
print(residue)







# for tag, proj_dirs in processedLumis.items():
#     for i in proj_dirs:
#         subprocess.call(['crab', 'report', f"crab_projects/{i}"])
#     to_process = LumiList(filename="crab_projects/{}/results/lumisToProcess.json".format(lumistoProcess[tag]))
#     residue = to_process
#     for proj_dir in proj_dirs:
#         residue = residue - processed

