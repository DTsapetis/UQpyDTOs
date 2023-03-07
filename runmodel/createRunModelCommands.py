from pathlib import Path

from PydanticModels_quoFEM_scInputJSON import ScInputJSONFile
from PydanticModels_quoFEM_RVs import randomVariables
from PydanticModels_UQpy_RunModel import ThirdPartyModel, RunModel, ValidateModelFilePaths


def createTemplateFile(randomVariables: randomVariables, templateFileName: str = 'params_template.in') -> None:
    stringList = []
    stringList.append(f"{len(randomVariables)}")
    for rv in randomVariables:
        stringList.append(f"{rv.name} <{rv.name}>")

    with open(templateFileName, "w") as f:
        f.write("\n".join(stringList))
    

def createModelScript(driverScript: str, modelScriptName: str = 'model_script.py', templateFileName: str = 'params_template.in') -> None:
    templateFilePath = Path(templateFileName)
    tmpFileBase = templateFilePath.stem
    tmpFileSuffix = templateFilePath.suffix
    stringList = []
    stringList.append("import subprocess")
    stringList.append("import fire\n")
    stringList.append("def model(sample_index: int) -> None:")
    stringList.append(f"\tcommand1 = f'mv ./InputFiles/{tmpFileBase}_" + "{sample_index}" + f"{tmpFileSuffix} ./params.in'")
    stringList.append(f"\tcommand2 = './{driverScript}'\n")
    stringList.append("\tsubprocess.run(command1, stderr=subprocess.STDOUT, shell=True)")
    stringList.append("\tsubprocess.run(command2, stderr=subprocess.STDOUT, shell=True)\n")
    stringList.append("if __name__ == '__main__':")
    stringList.append("\tfire.Fire(model)")

    with open(modelScriptName, "w") as f:
        f.write("\n".join(stringList))


def createPostProcessScriptLimitState(threshold: float = 0.0, resultsFile: str = 'results.out', postProcessFileName: str = 'post_process_script.py') -> None:
    stringList = []
    stringList.append("def compute_limit_state(index: int) -> float:")
    stringList.append(f"\twith open('{resultsFile}', 'r') as f:")
    stringList.append(f"\t\tres = f.read().strip()")
    stringList.append("\tif res:")
    stringList.append("\t\ttry:")
    stringList.append("\t\t\tres = float(res)")
    stringList.append("\t\texcept ValueError:")
    stringList.append("\t\t\traise ValueError(f'Result should be a single float value, check results.out file for sample evaluation {index}')")
    stringList.append("\t\texcept Exception:")
    stringList.append("\t\t\traise")
    stringList.append(("\t\telse:"))
    stringList.append(f"\t\t\treturn {threshold} - res")
    stringList.append("\telse:")
    stringList.append("\t\traise ValueError(f'Result not found in results.out file for sample evaluation " + "{index}')")

    with open(postProcessFileName, "w") as f:
        f.write("\n".join(stringList))


def createVarNamesList(randomVariables: randomVariables) -> list[str]:
    stringList = []
    for rv in randomVariables:
        stringList.append(f'{rv.name}')
    return stringList


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
    ValidateModelFilePaths(input_template=Path('params_template.in'), model_script=Path('model_script.py'), output_script=Path('post_process_script.py'))
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
