from fastapi import APIRouter, HTTPException, Header, Body, Form
from pydantic import BaseModel
from app.services.prediction import predict

router = APIRouter()

class housedetails(BaseModel):
    bedrooms: int
    bathrooms: int
    house_size_sqft: float
    land_size_perch: float
    location: str


@router.post("/predict/request")
async def get_data_request(data: housedetails = Body(...)):
    try:
        predict_price = await predict(data.bedrooms, data.bathrooms, data.house_size_sqft, data.land_size_perch, data.location)
        if predict_price is None:
            raise HTTPException(status_code=400, detail="Prediction failed")
        
        return {
            "predicted_price": predict_price
        }
    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/predict/form")
async def get_data(
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    house_size_sqft: float = Form(...),
    land_size_perch: float = Form(...),
    location: str = Form(...)
):
    try:
        # Create the Pydantic model instance manually
        data = housedetails(
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            house_size_sqft=house_size_sqft,
            land_size_perch=land_size_perch,
            location=location
        )
        
        predict_price = await predict(
            data.bedrooms, data.bathrooms, data.house_size_sqft, data.land_size_perch, data.location
        )
        if predict_price is None:
            raise HTTPException(status_code=400, detail="Prediction failed")
        
        return {"predicted_price": predict_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
