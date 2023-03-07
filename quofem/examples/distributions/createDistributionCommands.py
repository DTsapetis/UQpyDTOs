from pathlib import Path

from quofem.examples.runmodel.PydanticModels_UQpy_RunModel import ValidateModelFilePaths
from quofem.examples.runmodel.PydanticModels_quoFEM_scInputJSON import ScInputJSONFile
from quofem.examples.runmodel.createRunModelCommands import createTemplateFile, createModelScript, \
    createPostProcessScriptLimitState, createVarNamesList, createRunModelImportLines, createRunModelBodyLines


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
    ValidateModelFilePaths(input_template=Path('params_template.in'), model_script=Path('model_script.py'),
                           output_script=Path('post_process_script.py'))
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