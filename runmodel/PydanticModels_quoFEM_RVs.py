import pydantic
import typing
# import scipy.stats as st
# import numpy as np

allowableInputTypes = typing.Literal["Parameters", "Moments", "Dataset"]
# allowableVariableClasses = typing.Literal["Design", "Uniform", "NA", "Uncertain"]

############################################
# def readFile(path):
#     with open(path, "r") as f:
#         return np.genfromtxt(f)

############################################
class RVCommonData(pydantic.BaseModel):
    name: str
    value: str
    refCount: int

# ############################################
class UncertainVariableClass(RVCommonData):
    variableClass: typing.Literal["Uncertain"]

class DesignVariableClass(RVCommonData):
    variableClass: typing.Literal["Design"]

class UniformVariableClass(RVCommonData):
    variableClass: typing.Literal["Uniform"]
        
class NAVariableClass(RVCommonData):
    variableClass: typing.Literal["NA"]


# class randomVariableClass(pydantic.BaseModel):
#     __root__: list[typing.Annotated[
#         typing.Union[UncertainVariableClass, DesignVariableClass, UniformVariableClass,
#         NAVariableClass
#         ], pydantic.Field(discriminator="variableClass")]]
    
#     class Config:
#         extra = pydantic.Extra.forbid

# with open("rvClassSchema.json", "w") as f:
#     json.dump(randomVariableClass.schema(), f, indent=4)

# ############################################     
class BetaUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["Beta"]

class ChiSquaredUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["ChiSquared"]

class ExponentialUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["Exponential"]

class GammaUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["Gamma"]

class GumbelUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["Gumbel"]

class LognormalUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["Lognormal"]

class NormalUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["Normal"]

class TruncatedExponentialUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["TruncatedExponential"]

class UniformUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["Uniform"]

class WeibullUncertainVariable(UncertainVariableClass):
    distribution: typing.Literal["Weibull"]

# class randomVariableDistributionsUncertain(randomVariableClass):
#     __root__: list[typing.Annotated[typing.Union[BetaUncertainVariable, UniformUncertainVariable], 
#     pydantic.Field(discriminator="distribution")]]
    
#     class Config:
#         extra = pydantic.Extra.forbid

# with open("rvDistUncertainSchema.json", "w") as f:
#     json.dump(randomVariableDistributionsUncertain.schema(), f, indent=4)

# ############################################      
class UniformUniformVariable(UniformVariableClass):
    distribution: typing.Literal["Uniform"]

# class randomVariableDistributionsUniform(randomVariableClass):
#     __root__: list[UniformUniformVariable]
    
#     class Config:
#         extra = pydantic.Extra.forbid

# with open("rvDistUniformSchema.json", "w") as f:
#     json.dump(randomVariableDistributionsUniform.schema(), f, indent=4)

############################################     
class BetaUncertainData(BetaUncertainVariable):
    lowerbound: float = 0.0
    upperbound: float = 1.0
    @pydantic.validator('upperbound')
    def upper_bound_not_bigger_than_lower_bound(v, values):
        if 'lowerbound' in values and v <= values['lowerbound']:
            raise ValueError(f"The upper bound must be bigger than the lower bound {values['lowerbound']}. Got a value of {v}.")
        return v

class BetaParameters(BetaUncertainData):
    inputType: typing.Literal["Parameters"]
    alphas: pydantic.PositiveFloat
    betas: pydantic.PositiveFloat

    def _to_scipy(self):
        a = self.alphas
        b = self.betas
        loc = self.lowerbound
        scale = self.upperbound - self.lowerbound
        return {"a": a, "b": b, "loc": loc, "scale": scale}

class BetaMoments(BetaUncertainData):
    inputType: typing.Literal["Moments"]
    mean: float
    standardDev: pydantic.PositiveFloat

    def _to_scipy(self):
        a = (self.upperbound - self.mean)*(self.mean - self.lowerbound)/(self.standardDev**2-1)*(self.mean-self.lowerbound)/(self.upperbound - self.lowerbound)
        b = a*(self.upperbound-self.mean)/(self.mean-self.lowerbound)
        if a <= 0 or b <= 0:
            raise ValueError(f"The specified moments are not appropriate.")
        loc = self.lowerbound
        scale = self.upperbound - self.lowerbound
        return {"a": a, "b": b, "loc": loc, "scale": scale}

class BetaDataset(BetaUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str
    
    # def _to_scipy(self):
    #     loc = self.lowerbound
    #     scale = self.upperbound - self.lowerbound
    #     data = readFile(self.dataDir)
    #     params = st.beta.fit(data=data, floc=loc, fscale=scale)
    #     a = params[0]
    #     b = params[1]
    #     return {"a": a, "b": b, "loc": loc, "scale": scale}

############################################
class ChiSquaredUncertainData(ChiSquaredUncertainVariable):
    pass

class ChiSquaredParameters(ChiSquaredUncertainData):
    inputType: typing.Literal["Parameters"]
    k: pydantic.conint(ge=1)

class ChiSquaredMoments(ChiSquaredUncertainData):
    inputType: typing.Literal["Moments"]
    mean: pydantic.PositiveFloat

class ChiSquaredDataset(ChiSquaredUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################
class ExponentialUncertainData(ExponentialUncertainVariable):
    pass

class ExponentialParameters(ExponentialUncertainData):
    inputType: typing.Literal["Parameters"]
    lamda: pydantic.PositiveFloat = pydantic.Field(alias="lambda")

class ExponentialMoments(ExponentialUncertainData):
    inputType: typing.Literal["Moments"]
    mean: pydantic.PositiveFloat

class ExponentialDataset(ExponentialUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################
class GammaUncertainData(GammaUncertainVariable):
    pass

class GammaParameters(GammaUncertainData):
    inputType: typing.Literal["Parameters"]
    k: pydantic.PositiveFloat
    lamda: pydantic.PositiveFloat = pydantic.Field(alias="lambda")

class GammaMoments(GammaUncertainData):
    inputType: typing.Literal["Moments"]
    mean: pydantic.PositiveFloat
    standardDev: pydantic.PositiveFloat

class GammaDataset(GammaUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################
class GumbelUncertainData(GumbelUncertainVariable):
    pass

class GumbelParameters(GumbelUncertainData):
    inputType: typing.Literal["Parameters"]
    alphaparam: pydantic.PositiveFloat
    betaparam: float

class GumbelMoments(GumbelUncertainData):
    inputType: typing.Literal["Moments"]
    mean: float
    standardDev: pydantic.PositiveFloat

class GumbelDataset(GumbelUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################
class LognormalUncertainData(LognormalUncertainVariable):
    pass

class LognormalParameters(LognormalUncertainData):
    inputType: typing.Literal["Parameters"]
    lamda: float = pydantic.Field(alias="lambda")
    zeta: pydantic.PositiveFloat

class LognormalMoments(LognormalUncertainData):
    inputType: typing.Literal["Moments"]
    mean: pydantic.PositiveFloat
    stdDev: pydantic.PositiveFloat

class LognormalDataset(LognormalUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################
class NormalUncertainData(NormalUncertainVariable):
    pass

class NormalParameters(NormalUncertainData):
    inputType: typing.Literal["Parameters"]
    mean: float
    stdDev: pydantic.PositiveFloat

class NormalMoments(NormalUncertainData):
    inputType: typing.Literal["Moments"]
    mean: float
    stdDev: pydantic.PositiveFloat

class NormalDataset(NormalUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################     
class TruncatedExponentialUncertainData(TruncatedExponentialUncertainVariable):
    a: float
    b: float
    @pydantic.validator('b')
    def upper_bound_not_bigger_than_lower_bound(v, values):
        if 'a' in values and v <= values['a']:
            raise ValueError(f"The upper bound must be bigger than the lower bound {values['a']}. Got a value of {v}.")
        return v

class TruncatedExponentialParameters(TruncatedExponentialUncertainData):
    inputType: typing.Literal["Parameters"]
    lamda: pydantic.PositiveFloat = pydantic.Field(alias="lambda")

class TruncatedExponentialMoments(TruncatedExponentialUncertainData):
    inputType: typing.Literal["Moments"]
    mean: pydantic.PositiveFloat

class TruncatedExponentialDataset(TruncatedExponentialUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################
class UniformUncertainData(UniformUncertainVariable):
    pass

class UniformParameters(UniformUncertainData):
    inputType: typing.Literal["Parameters"]
    lowerbound: float = 0.0
    upperbound: float = 1.0
    @pydantic.validator('upperbound')
    def upper_bound_not_bigger_than_lower_bound(v, values):
        if 'lowerbound' in values and v <= values['lowerbound']:
            raise ValueError(f"The upper bound must be bigger than the lower bound {values['lowerbound']}. Got a value of {v}.")
        return v

class UniformMoments(UniformUncertainData):
    inputType: typing.Literal["Moments"]
    mean: float
    standardDev: pydantic.PositiveFloat

class UniformDataset(UniformUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################
class WeibullUncertainData(WeibullUncertainVariable):
    pass

class WeibullParameters(WeibullUncertainData):
    inputType: typing.Literal["Parameters"]
    scaleparam: pydantic.PositiveFloat
    shapeparam: pydantic.PositiveFloat

class WeibullMoments(WeibullUncertainData):
    inputType: typing.Literal["Moments"]
    mean: pydantic.PositiveFloat
    standardDev: pydantic.PositiveFloat

class WeibullDataset(WeibullUncertainData):
    inputType: typing.Literal["Dataset"]
    dataDir: str

############################################
randomVariables = list[typing.Union[BetaParameters, BetaMoments, BetaDataset,\
                                ChiSquaredParameters, ChiSquaredMoments, ChiSquaredDataset,\
                                ExponentialParameters, ExponentialMoments, ExponentialDataset,\
                                GammaParameters, GammaMoments, GammaDataset,\
                                GumbelParameters, GumbelMoments, GumbelDataset,\
                                LognormalParameters, LognormalMoments, LognormalDataset,\
                                NormalParameters, NormalMoments, NormalDataset,\
                                TruncatedExponentialParameters, TruncatedExponentialMoments, TruncatedExponentialDataset,\
                                UniformParameters, UniformMoments, UniformDataset,\
                                WeibullParameters, WeibullMoments, WeibullDataset]]

# class randomVariables(pydantic.BaseModel):
#     __root__: list[typing.Union[BetaParameters, BetaMoments, BetaDataset, 
#                                 ChiSquaredParameters, ChiSquaredMoments, ChiSquaredDataset,
#                                 ExponentialParameters, ExponentialMoments, ExponentialDataset,
#                                 GammaParameters, GammaMoments, GammaDataset,
#                                 GumbelParameters, GumbelMoments, GumbelDataset,
#                                 LognormalParameters, LognormalMoments, LognormalDataset,
#                                 NormalParameters, NormalMoments, NormalDataset,
#                                 TruncatedExponentialParameters, TruncatedExponentialMoments, TruncatedExponentialDataset,
#                                 UniformParameters, UniformMoments, UniformDataset,
#                                 WeibullParameters, WeibullMoments, WeibullDataset]]
    # __root__: list[typing.Annotated[[
    #                typing.Annotated[typing.Union[BetaParameters, UniformParameters], pydantic.Field(discriminator="distribution")],
    #                typing.Annotated[typing.Union[BetaMoments, UniformMoments], pydantic.Field(discriminator="distribution")],
    #                typing.Annotated[typing.Union[BetaDataset, UniformDataset], pydantic.Field(discriminator="distribution")]
    #                ], pydantic.Field(discriminator="inputType")]]
        # typing.Annotated[
        # typing.Union[BetaParameters, BetaMoments, BetaDataset,
        # UniformParameters, UniformMoments, UniformDataset,
        # ], pydantic.Field(discriminator="inputType")]]
    
    # class Config:
    #     extra = pydantic.Extra.forbid

# with open('rvSchema.json', 'w') as f:
#     json.dump(randomVariables.schema(), f, indent=4)
# print(randomVariables.schema_json(indent=4))


