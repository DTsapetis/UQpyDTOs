from pydantic import BaseModel, Field
from typing import Literal, Union
from typing_extensions import Annotated
from py_linq import Enumerable

from preprocess.ReliabilityDTOs import ReliabilityMethod


class ModuleBaseDTO(BaseModel):
    pass


class SamplingDTO(ModuleBaseDTO):
    uqType: Literal['Sampling'] = 'Sampling'

    def generate_code(self):
        pass


class ReliabilityDTO(ModuleBaseDTO):
    uqType: Literal['Reliability'] = 'Reliability'
    methodData: ReliabilityMethod


ModuleDTO = Annotated[Union[ReliabilityDTO, SamplingDTO], Field(discriminator='uqType')]