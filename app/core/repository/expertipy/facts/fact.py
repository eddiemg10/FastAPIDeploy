
from ....schemas.HealthMetrics import PALType, BloodSugar, PALOut, Gender
from ....schemas.Profile import BloodSugarEntry

class Fact():
    height: float
    weight: int 
    bmi: float
    age: int 
    gender: str
    coords: list
    pal: PALOut
    eer: float 
    HbA1C: BloodSugar | None
    blood_sugar_history: list[BloodSugarEntry] | None
    # blood_sugar_level: str
    cuisine: list[str] | None
    exclude: list[str] | None

    def __init__(self, patient):
        self.height = patient['height']
        self.weight = patient['weight']
        self.bmi = patient['bmi']
        self.age = patient['age']
        self.gender = patient['gender']
        self.coords = patient['coords'] 
        self.pal = patient['pal']
        self.eer = patient['eer']
        self.HbA1C = patient['HbA1C']
        self.blood_sugar_history = patient['blood_sugar_history']
        # self.blood_sugar_level = patient['blood_sugar_level']
        # self.cuisine = patient['cuisine']
        self.exclude = patient['exclude']

    def update(self, updates):
        for key, value in updates.items():
            setattr(self, key , value)
        
