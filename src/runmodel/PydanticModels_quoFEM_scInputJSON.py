from __future__ import annotations
from typing import Dict, List, Literal, Union, Optional
from pydantic import BaseModel, DirectoryPath, confloat, PositiveInt
from pathlib import Path

from PydanticModels_quoFEM_RVs import randomVariables
from PydanticModels_UQpyMCMC import Stretch


# ProbabilityType = confloat(ge=0.0, le=1.0)
SubsetSimConditionalProbabilityType = confloat(gt=0.0, lt=1.0)
CorrelationType = confloat(ge=-1.0, le=1.0)


class OpenSeesFEMApplicationData(BaseModel):
    mainScript: str
    MS_Path: DirectoryPath
    postprocessScript: str = '""'
    PS_Path: Optional[DirectoryPath] = None


class OpenSeesPyFEMApplicationData(BaseModel):
    mainScript: str
    MS_Path: DirectoryPath
    postprocessScript: str = '""'
    PS_Path: Optional[DirectoryPath] = None
    parametersScript: str = '""'
    PA_Path: Optional[DirectoryPath] = None


class FEMApplicationOpenSees(BaseModel):
    Application: Literal["OpenSees"]
    ApplicationData: OpenSeesFEMApplicationData


class FEMApplicationOpenSeesPy(BaseModel):
    Application: Literal["OpenSeesPy"]
    ApplicationData: OpenSeesPyFEMApplicationData


class UQApplication(BaseModel):
    Application: str
    ApplicationData: Optional[Dict[str, str]] = None


class Applications(BaseModel):
    FEM: Union[FEMApplicationOpenSees, FEMApplicationOpenSeesPy]
    UQ: UQApplication


class EDPItem(BaseModel):
    length: int
    name: str
    type: str


class UCSD_UQ_TMCMC(BaseModel):
    calDataFile: str
    calDataFilePath: DirectoryPath
    logLikelihoodFile: str = '""'
    logLikelihoodPath: Optional[DirectoryPath] = None
    numExperiments: Optional[int] = None
    numParticles: int
    parallelExecution: bool
    readUserDefinedCovarianceData: Optional[bool] = False
    seed: int
    uqType: str


class SubsetSimulationData(BaseModel):
    conditionalProbability: SubsetSimConditionalProbabilityType
    maxLevels: PositiveInt
    failureThreshold: float
    mcmcMethodData: Stretch


class ReliabilityMethodData(BaseModel):
    method: Literal["Subset Simulation"]
    subsetSimulationData: SubsetSimulationData


class UQpy_Reliability(BaseModel):
    parallelExecution: bool
    reliabilityMethodData: ReliabilityMethodData
    uqType: Literal["Reliability"]


class ScInputJSONFile(BaseModel):
    Applications: Applications
    EDP: List[EDPItem]
    FEM: Optional[Dict[str, str]] = None
    UQ: Union[UCSD_UQ_TMCMC, UQpy_Reliability]
    WorkflowType: Optional[str] = None
    correlationMatrix: List[CorrelationType]
    isSurrogate: Optional[bool] = None
    localAppDir: DirectoryPath
    randomVariables: randomVariables
    remoteAppDir: Optional[DirectoryPath] = None
    resultType: Optional[str]
    runDir: Optional[str]
    runType: Literal["runningLocal", "runningRemote"]
    summary: Optional[List] = None
    workingDir: str


def main():

    # import json
    # with open("scInputSchema.json", "w") as f:
        # json.dump(ScInputJSONFile.schema(), f, indent=4)
    # for item in n:
        # print(f"{item = }")
    
    print("Done!")

if __name__ == "__main__":
    main()
