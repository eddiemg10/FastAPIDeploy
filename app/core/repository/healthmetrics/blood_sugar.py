from app.core.schemas.HealthMetrics import BloodSugarIn, BloodSugarUnits, GlucoseTest


def interpret_blood_sugar(request: BloodSugarIn):
    """
    mg/dL in mmol/L, conversion factor: 1 mg/dL = 0.0555 mmol/L
    a1c = (mg/dL + 46.7)/28.7 (American Diabetes Association) 
    """
    value, units, test = request.value, request.units, request.test
    mg_value = None
    mmol_value = None
    percentage_value = None
    level = None

    if units == BloodSugarUnits.mg_dL:
        mg_value = value
        mmol_value = 0.0555 * mg_value
        percentage_value =  (mg_value + 46.7) / 28.7
    elif units == BloodSugarUnits.mmol_L:
        mmol_value = value
        mg_value = (1/0.0555) * mmol_value
        percentage_value =  (mg_value + 46.7) / 28.7
    elif units == BloodSugarUnits.percentage:
        percentage_value = value
        mg_value = (percentage_value * 28.7) - 46.7
        mmol_value = 0.0555 * mg_value

    # Depending on the type of test, categorization of blood sugar levels varies
    if test == GlucoseTest.A1C:
        if percentage_value < 5.7:
            level = "normal"
        elif percentage_value >= 5.7 and percentage_value <= 6.4:
            level = "prediabetic"
        else:
            level = "diabetic"

    elif test == GlucoseTest.random:
        if mg_value < 70:
            level = "hypoglycemic"
        elif mg_value < 200:
            level = "normal"
        else:
            level = "diabetic"

    elif test == GlucoseTest.fasting:
        if mg_value < 70:
            level = "hypoglycemic"
        elif mg_value < 100:
            level = "normal"
        elif mg_value >= 100 and mg_value <= 125:
            level = "prediabetic"
        else:
            level = "diabetic"
            
    elif test == GlucoseTest.tolerance:
        if mg_value < 70:
            level = "hypoglycemic"
        elif mg_value < 140:
            level = "normal"
        elif mg_value >= 140 and mg_value <= 199:
            level = "prediabetic"
        else:
            level = "diabetic"


    sugar_level = [
        {"value": mg_value, "units": BloodSugarUnits.mg_dL},
        {"value": mmol_value, "units": BloodSugarUnits.mmol_L},
        {"value": percentage_value, "units": BloodSugarUnits.percentage}
    ]
    results = {
        "blood_sugar_level": sugar_level,
        "test": test,
        "level": level
    }
    return results