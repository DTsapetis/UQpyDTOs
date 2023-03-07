from pydantic import BaseModel, Field
from typing import Literal, Union
from typing_extensions import Annotated

from src.sampling.mcmc.StretchDto import StretchDto


class ReliabilityMethodBaseDTO(BaseModel):
    pass


class SubsetSimulationDTO(ReliabilityMethodBaseDTO):
    method: Literal['SubsetSimulation'] = 'SubsetSimulation'
    conditionalProbability: float
    failureThreshold: int
    maxLevels: int
    samplingMethod: StretchDto


class FormDTO(ReliabilityMethodBaseDTO):
    method: Literal['FORM'] = 'FORM'


ReliabilityMethod = Annotated[Union[SubsetSimulationDTO, FormDTO], Field(discriminator='method')]
