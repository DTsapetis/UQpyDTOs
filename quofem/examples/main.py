from src.runmodel.RunModelDTOs import RunModelDTO
from src.quofemDTOs import *
import os

code = []

with open(os.path.join(os.getcwd(), "inputsSubsetSimtcl.json")) as my_file:
    json = my_file.read()
    model = Model.parse_raw(json)

code.append('from UQpy.distributions import JointIndependent\n')
marginals_code = 'dist = JointIndependent(['
for distribution in model.randomVariables:
    (distribution_code, input) = distribution.init_to_text()
    marginals_code += input + ','
    code.append(distribution_code)
marginals_code += '])\n'
code.append(marginals_code)

runmodel_code = RunModelDTO.create_runmodel_with_variables_driver(variables=model.randomVariables,
                                                                  driver_filename="driver")
(uqmethod_code, _) = model.UQ.methodData.generate_code()

code.append(runmodel_code)
code.append(uqmethod_code)

with open("UQpyAnalysis.py", 'w') as outfile:
    outfile.write("\n".join(code))
