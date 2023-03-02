from PydanticModels_quoFEM_scInputJSON import ScInputJSONFile
from PydanticModels_quoFEM_RVs import randomVariables
from PydanticModels_UQpy_Distributions import Normal, Uniform
from createRunModelCommands import *


def createDistributionsImportLines(randomVariables) -> str:
    stringSet = set()
    for rv in randomVariables:
        stringSet.add(f"from UQpy.distributions.collection.{rv.distribution} import {rv.distribution}")
    return "\n".join(stringSet)


def createDistributionsBodyLines(randomVariables) -> str:
    stringList = []
    for rv in randomVariables:
        if rv.distribution in ["Uniform", "Normal"]:
            params = rv._to_scipy()
            dist = eval(rv.distribution)(**params)
            stringList.append(f'{rv.name} = {repr(dist)}')
    return "\n".join(stringList)


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

    distributionsImportLines = createDistributionsImportLines(inputData.randomVariables)
    distributionsBodyLines = createDistributionsBodyLines(inputData.randomVariables)

    sectionDiv = "\n\n"
    with open("UQpyAnalysis.py", "a+") as f:
        f.write(sectionDiv.join([distributionsImportLines, 
                                 runModelImportLines,
                                 distributionsBodyLines,
                                 runModelBodyLines]))
    
    print("Done!")


if __name__ == "__main__":
    main()