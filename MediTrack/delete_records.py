from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Path
from fastapi.responses import JSONResponse
from create_records import load_data, save_data
app = FastAPI()

@app.delete("/delete/{patient_id}")
def delete_records(patient_id : Annotated[str, Path(..., description="ID of the patient", examples=["p001"])]
):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    del data[patient_id]

    save_data(data)

    return JSONResponse(
        status_code=200,
        content="Patient deleted successfully"
    )

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8003)