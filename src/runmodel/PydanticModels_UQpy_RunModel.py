from pydantic import BaseModel, FilePath, PositiveInt
from typing import Optional
from pathlib import Path


class ValidateModelFilePaths(BaseModel):
    input_template: FilePath = Path('params_template.in')
    model_script: FilePath = Path('model_script.py')
    output_script: FilePath = Path('post_process_script.py')


class ThirdPartyModel(BaseModel):
    var_names: list[str]
    input_template: str = 'params_template.in'
    model_script: str = 'model_script.py'
    output_script: str = 'post_process_script.py'
    model_object_name: Optional[str] = None
    output_object_name: Optional[str] = None
    fmt: Optional[str] = None
    separator: str = ", "
    delete_files: bool = False
    model_dir: str = 'Model_Runs'


class RunModel(BaseModel):
    model: ThirdPartyModel
    # samples: Optional[list] = None
    ntasks: PositiveInt = 1
    cores_per_task: PositiveInt = 1
    nodes: PositiveInt = 1
    resume: bool = False
