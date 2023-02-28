from pathlib import Path

from PydanticModels_quoFEM_scInputJSON import ScInputJSONFile
from PydanticModels_quoFEM_RVs import randomVariables


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
    stringList.append(f"\tcommand1 = f'mv ./InputFiles/{tmpFileBase}_" + "{sample_index + 1}" + f"{tmpFileSuffix} ./params.in'")
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
    stringList.append("\t\tif res.isdigit():")
    stringList.append(f"\t\t\treturn {threshold} - float(res)")
    stringList.append(("\t\telse:"))
    stringList.append("\t\t\traise ValueError(f'Result should be a single float value, check results.out file for sample evaluation " + "{index}')")
    stringList.append("\telse:")
    stringList.append("\t\traise ValueError(f'Result not found in results.out file for sample evaluation " + "{index}')")

    with open(postProcessFileName, "w") as f:
        f.write("\n".join(stringList))


def createVarNamesListString(randomVariables: randomVariables) -> str:
    stringList = []
    for rv in randomVariables:
        stringList.append(f"'{rv.name}'")
    return "varNames = [" + ", ".join(stringList) + "]"


def createRunModelImportLines() -> str:
    stringList = []
    stringList.append("from UQpy.run_model.RunModel import RunModel")
    stringList.append("from UQpy.run_model.model_execution.ThirdPartyModel import ThirdPartyModel")
    return "\n".join(stringList)


def createRunModelBodyLines() -> str:
    stringList = []
    stringList.append("model = ThirdPartyModel(input_template='params_template.in', ")
    stringList.append("\t"*6 + "model_script='model_script.py', ")
    stringList.append("\t"*6 + "output_script='post_process_script.py', ")
    stringList.append("\t"*6 + "var_names=varNames, ")
    stringList.append("\t"*6 + "model_dir='workdir')")
    stringList.append("rm = RunModel(model=model)")

    return "\n".join(stringList)


def main():
    import os
    os.remove("./UQpyAnalysis.py")
    sectionDiv = "\n\n"

    pathToscInputJSONFile = "/Users/aakash/Documents/quoFEM/LocalWorkDir/tmp.SimCenter/templatedir/scInput.json"
    inputData = ScInputJSONFile.parse_file(pathToscInputJSONFile)

    createTemplateFile(inputData.randomVariables)
    createModelScript("driver.bat")
    createPostProcessScriptLimitState()
    runModelImportStatements = createRunModelImportLines()

    varNamesListString = createVarNamesListString(inputData.randomVariables)
    runModelBodyString = createRunModelBodyLines()

    with open("UQpyAnalysis.py", "a+") as f:
        f.write(sectionDiv.join([runModelImportStatements,
                                 varNamesListString,
                                 runModelBodyString]))
    
    print("Done!")

if __name__ == "__main__":
    main()
