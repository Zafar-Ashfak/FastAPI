import uvicorn
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal, Annotated
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from MediTrack.create_records import Patient, load_data ,save_data

app = FastAPI()


class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None, max_length=50)]
    email: Annotated[Optional[EmailStr], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal["MALE", "FEMALE", "OTHER"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    allergies: Annotated[Optional[List[str]], Field(default=None)]


# Creating an endpoint to update existing patient's records
@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, new_records : UpdatePatient):

    data = load_data()

    # Check that patient exists or not
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    existing_patient_info = data[patient_id]
    update_patient_info = new_records.model_dump(exclude_unset=True)

    # Retrieve on the given info
    for key, value in update_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(
        status_code=200,
        content="Patient updated successfully"
    )

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8002)