from pydantic import BaseModel, PositiveFloat


class Normal(BaseModel):
    loc: float = 0.0
    scale: PositiveFloat = 1.0


class Uniform(BaseModel):
    loc: float = 0.0
    scale: PositiveFloat = 1.0