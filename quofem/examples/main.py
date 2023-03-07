# from preprocess.models import *
# import os

# with open(os.path.join(os.getcwd(), "tmp.SimCenter", "templatedir", "inputsSubsetSimtcl.json")) as my_file:
#     json = my_file.read()
#     model = Model.parse_raw(json)
#     (prerequisite_str, input_str) = model.UQ.reliabilityMethodData.subsetSimulationData.mcmcMethodData.generate_code()

#     with open("UQpy_runner.py", 'w') as outfile:
#         outfile.write(prerequisite_str)
#         outfile.write(input_str)
from src.runmodel.RunModelDTOs import RunModelDTO
from src.quofemDTOs import *
import os

code = []

with open(os.path.join(os.getcwd(), "tmp.SimCenter", "templatedir", "inputsSubsetSimtcl.json")) as my_file:
    json = my_file.read()
    model = Model.parse_raw(json)

runmodel_code = RunModelDTO.create_runmodel_with_variables_driver(variables=model.randomVariables,
                                                                  driver_filename="driver")

(uqmethod_code, _) = model.UQ.methodData.generate_code()

code.append(runmodel_code)
code.append(uqmethod_code)

with open("UQpyAnalysis.py", 'w') as outfile:
    outfile.write("\n".join(code))
