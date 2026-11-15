from pydantic import BaseModel
from typing import Optional
class Patient(BaseModel):
    name : str
    age : int
    height : float
    weight : float
    is_married : Optional[bool] = False

patient_dict = {
    "name" : "Aladdin",
    "age" : 25,
    "height" : 1.43,
    "weight" : 67.28
}

patient1 = Patient(**patient_dict)

# temp = patient1.model_dump()
# temp = patient1.model_dump(include=['name', 'age'])
# temp = patient1.model_dump(exclude=['height'])
temp = patient1.model_dump(exclude_unset=True)
print(temp)
print(type(temp))
