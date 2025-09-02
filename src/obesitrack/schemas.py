from pydantic import BaseModel, Field, conint, confloat
from typing import Literal


YesNo = Literal["yes", "no"]
Freq = Literal["no", "sometimes", "frequently", "always"]
Transport = Literal["Public_Transportation", "Automobile", "Walking", "Bike", "Motorbike"]


ConstrainedIntAge = conint(ge=5, le=100)
ConstrainedFloatHeight = confloat(gt=0, le=2.3)
ConstrainedFloatWeight = confloat(gt=0, le=300)
ConstrainedFloatFCVC = confloat(ge=1, le=3)
ConstrainedIntNCP = conint(ge=1, le=8)
ConstrainedFloatCH2O = confloat(gt=0, le=10)
ConstrainedFloatFAF = confloat(ge=0, le=7)
ConstrainedFloatTUE = confloat(ge=0, le=24)

class PredictRequest(BaseModel):
	age: int = Field(..., ge=5, le=100)
	height: float = Field(..., gt=0, le=2.3)
	weight: float = Field(..., gt=0, le=300)
	family_history_with_overweight: YesNo
	FAVC: YesNo
	FCVC: float = Field(..., ge=1, le=3)
	NCP: int = Field(..., ge=1, le=8)
	CAEC: Freq
	SMOKE: YesNo
	CH2O: float = Field(..., gt=0, le=10)
	SCC: YesNo
	FAF: float = Field(..., ge=0, le=7)
	TUE: float = Field(..., ge=0, le=24)
	CALC: Freq
	MTRANS: Transport


class PredictResponse(BaseModel):
	label: str
	probabilities: dict[str, float]


class Token(BaseModel):
	access_token: str
	token_type: str = "bearer"


class TokenData(BaseModel):
	username: str | None = None