from pathlib import Path

from PydanticModels_quoFEM_scInputJSON import ScInputJSONFile
from PydanticModels_quoFEM_RVs import randomVariables
from PydanticModels_UQpy_RunModel import ThirdPartyModel, RunModel, ValidateModelFilePaths


def createTemplateFile(randomVariables: randomVariables, templateFileName: str = 'params_template.in') -> None:
    stringList = [f"{len(randomVariables)}"]
    for rv in randomVariables:
        stringList.append(f"{rv.name} <{rv.name}>")

    with open(templateFileName, "w") as f:
        f.write("\n".join(stringList))
    

def createModelScript(driverScript: str,
                      modelScriptName: str = 'model_script.py',
                      templateFileName: str = 'params_template.in') -> None:
    templateFilePath = Path(templateFileName)
    tmpFileBase = templateFilePath.stem
    tmpFileSuffix = templateFilePath.suffix
    stringList = [
        'import subprocess',
        'import fire\n',
        'def model(sample_index: int) -> None:',
        f"\tcommand1 = f'mv ./InputFiles/{tmpFileBase}_"
        + "{sample_index}"
        + f"{tmpFileSuffix} ./params.in'",
        f"\tcommand2 = './{driverScript}'\n",
        '\tsubprocess.run(command1, stderr=subprocess.STDOUT, shell=True)',
        '\tsubprocess.run(command2, stderr=subprocess.STDOUT, shell=True)\n',
        "if __name__ == '__main__':",
        '\tfire.Fire(model)',
    ]

    with open(modelScriptName, "w") as f:
        f.write("\n".join(stringList))


def createPostProcessScriptLimitState(threshold: float = 0.0,
                                      resultsFile: str = 'results.out',
                                      postProcessFileName: str = 'postprocess_script.py') -> None:
    stringList = [
        'def compute_limit_state(index: int) -> float:',
        f"\twith open('{resultsFile}', 'r') as f:",
        '\t\tres = f.read().strip()',
        '\tif res:',
        '\t\ttry:',
        '\t\t\tres = float(res)',
        '\t\texcept ValueError:',
        "\t\t\traise ValueError(f'Result should be a single float value, check results.out file for sample evaluation {index}')",
        '\t\texcept Exception:',
        '\t\t\traise',
        '\t\telse:',
        f"\t\t\treturn {threshold} - res",
        '\telse:',
        "\t\traise ValueError(f'Result not found in results.out file for sample evaluation "
        + "{index}')",
    ]

    with open(postProcessFileName, "w") as f:
        f.write("\n".join(stringList))


def createVarNamesList(randomVariables: randomVariables) -> list[str]:
    return [f'{rv.name}' for rv in randomVariables]


def createRunModelImportLines() -> str:
    stringList = []
    stringList.append("from UQpy.run_model.RunModel import RunModel")
    stringList.append("from UQpy.run_model.model_execution.ThirdPartyModel import ThirdPartyModel")
    return "\n".join(stringList)


def createRunModelBodyLines(varNamesList) -> str:
    tpm = ThirdPartyModel(var_names=varNamesList)
    rm = RunModel(model=tpm)
    return f"rm = {repr(rm)}"

def main():
    import os
    try:
        os.remove("./UQpyAnalysis.py")
    except OSError:
        pass

    pathToscInputJSONFile = "/Users/aakash/Documents/quoFEM/LocalWorkDir/tmp.SimCenter/templatedir/scInput.json"
    inputData = ScInputJSONFile.parse_file(pathToscInputJSONFile)

    createTemplateFile(randomVariables=inputData.randomVariables)
    createModelScript(driverScript="driver")
    createPostProcessScriptLimitState()
    ValidateModelFilePaths(input_template=Path('params_template.in'), model_script=Path('model_script.py'),
                           output_script=Path('post_process_script.py'))
    varNamesList = createVarNamesList(randomVariables=inputData.randomVariables)
    runModelImportLines = createRunModelImportLines()
    runModelBodyLines = createRunModelBodyLines(varNamesList=varNamesList)

    sectionDiv = "\n\n"
    with open("UQpyAnalysis.py", "a+") as f:
        f.write(sectionDiv.join([runModelImportLines,
                                 runModelBodyLines]))
    
    print("Done!")

if __name__ == "__main__":
    main()
