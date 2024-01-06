from app.core.schemas.HealthMetrics import BmiIn

def calculate_bmi(request: BmiIn):
    bmi = request.weight/(request.height/100)**2
    return {"bmi": bmi}