from app.core.schemas.HealthMetrics import EEROut, EERIn

# Coefficients

lhs_constant = 0
age_coefficient = 0
height_coefficient = 0
weight_coefficient = 0
rhs_constant = 0

def get_coefficients(age, gender, PAL):
    # Coefficients for ages 0 - 2
    if (age < 3):
        print("Coefficients for ages 0 - 2")
        if gender == "male":
            lhs_constant = -716.45
            age_coefficient = -1
            height_coefficient = 17.82
            weight_coefficient = 15.06
            rhs_constant = 135
        elif gender == "female":
            lhs_constant = -69.15
            age_coefficient = 80
            height_coefficient = 2.65
            weight_coefficient = 54.15
            rhs_constant = 80

    # Coefficients for ages 3 - 13
    elif(age >= 3 and age <= 13):
        print("Coefficients for ages 3 - 13")
        if gender == "male":
            if PAL == "inactive":
                lhs_constant = -447.51
                age_coefficient = 3.68
                height_coefficient = 13.01
                weight_coefficient = 13.15
                rhs_constant = (20/15/25)
            elif PAL == "low active":
                lhs_constant = 19.12
                age_coefficient = 3.68
                height_coefficient = 8.62
                weight_coefficient = 20.28
                rhs_constant = (20/15/25)
            elif PAL == "active":
                lhs_constant = -388.19
                age_coefficient = 3.68
                height_coefficient = 12.66
                weight_coefficient = 20.46
                rhs_constant = (20/15/25)
            elif PAL == "very active":
                lhs_constant = -671.75 
                age_coefficient = 3.68
                height_coefficient = 15.38
                weight_coefficient = 23.25
                rhs_constant = (20/15/25)
        elif gender == "female":
            if PAL == "inactive":
                lhs_constant = 55.59 
                age_coefficient = -22.25
                height_coefficient = 8.43
                weight_coefficient = 17.07
                rhs_constant = (15/30)
            elif PAL == "low active":
                lhs_constant = -297.54
                age_coefficient = -22.25
                height_coefficient = 12.77
                weight_coefficient = 14.73
                rhs_constant = (15/30)
            elif PAL == "active":
                lhs_constant = -189.55
                age_coefficient = -22.25
                height_coefficient = 11.74
                weight_coefficient = 18.34
                rhs_constant = (15/30)
            elif PAL == "very active":
                lhs_constant = -709.59
                age_coefficient = -22.25
                height_coefficient = 18.22
                weight_coefficient = 14.25
                rhs_constant = (15/30)

    # Coefficients for ages 14 - 18
    elif(age >= 14 and age <= 18):
        print("Coefficients for ages 14 - 18")
        if gender == "male":
            if PAL == "inactive":
                lhs_constant = -447.51
                age_coefficient = 3.68
                height_coefficient = 13.01
                weight_coefficient = 13.15
                rhs_constant = 20
            elif PAL == "low active":
                lhs_constant = 19.12
                age_coefficient = 3.68
                height_coefficient = 8.62
                weight_coefficient = 20.28
                rhs_constant = 20
            elif PAL == "active":
                lhs_constant = -388.19
                age_coefficient = 3.68
                height_coefficient = 12.66
                weight_coefficient = 20.46
                rhs_constant = 20
            elif PAL == "very active":
                lhs_constant = -671.75 
                age_coefficient = 3.68
                height_coefficient = 15.38
                weight_coefficient = 23.25
                rhs_constant = 20
        elif gender == "female":
            if PAL == "inactive":
                lhs_constant = 55.59 
                age_coefficient = -22.25
                height_coefficient = 8.43
                weight_coefficient = 17.07
                rhs_constant = 20
            elif PAL == "low active":
                lhs_constant = -297.54
                age_coefficient = -22.25
                height_coefficient = 12.77
                weight_coefficient = 14.73
                rhs_constant = 20
            elif PAL == "active":
                lhs_constant = -189.55
                age_coefficient = -22.25
                height_coefficient = 11.74
                weight_coefficient = 18.34
                rhs_constant = 20
            elif PAL == "very active":
                lhs_constant = -709.59
                age_coefficient = -22.25
                height_coefficient = 18.22
                weight_coefficient = 14.25
                rhs_constant = 20

    elif(age >= 19):
        print("Coefficients for ages 19+")
        if gender == "male":
            print("Gender = male")
            if PAL == "inactive":
                lhs_constant = 753.07
                age_coefficient = -10.83
                height_coefficient = 6.50
                weight_coefficient = 14.10
                rhs_constant = 0
            elif PAL == "low active":
                lhs_constant = 581.47
                age_coefficient = -10.83
                height_coefficient = 8.30
                weight_coefficient = 14.94
                rhs_constant = 0
            elif PAL == "active":
                lhs_constant = 1004.82
                age_coefficient = -10.83
                height_coefficient = 6.52
                weight_coefficient = 15.91
                rhs_constant = 0
            elif PAL == "very active":
                lhs_constant = -517.88
                age_coefficient = -10.83
                height_coefficient = 15.61
                weight_coefficient = 19.11
                rhs_constant = 0
        elif gender == "female":
            if PAL == "inactive":
                print("Hereeee")
                lhs_constant = 584.90
                age_coefficient = -7.01
                height_coefficient = 5.72
                weight_coefficient = 11.71
                rhs_constant = 0
            elif PAL == "low active":
                lhs_constant = 575.77
                age_coefficient = -7.01
                height_coefficient = 6.60
                weight_coefficient = 12.14
                rhs_constant = 0
            elif PAL == "active":
                lhs_constant = 710.25
                age_coefficient = -7.01
                height_coefficient = 6.54
                weight_coefficient = 12.34
                rhs_constant = 0
            elif PAL == "very active":
                lhs_constant = 511.83
                age_coefficient = -7.01
                height_coefficient = 9.07
                weight_coefficient = 12.56
                rhs_constant = 0

    return (lhs_constant, age_coefficient, height_coefficient, weight_coefficient, rhs_constant)


def calculate_eer(request: EERIn):
    age, height, weight, gender, PAL = request.age, request.height, request.weight, request.gender, request.pal
    coefficients = get_coefficients(age, gender, PAL)
    lhs_constant, age_coefficient, height_coefficient, weight_coefficient, rhs_constant = coefficients
    
    # EER Forumla
    # print(f"{lhs_constant} + ({age_coefficient} * {age}) + ({height_coefficient} * {height}) + ({weight_coefficient} * {weight}) + {rhs_constant}")
    EER = lhs_constant + (age_coefficient * age) + (height_coefficient * height) + (weight_coefficient * weight) + rhs_constant
    return {"value": EER}

def calculate_eer_from_dict(request):
    age, height, weight, gender, PAL = request["age"], request["height"], request["weight"], request["gender"], request["pal"]
    coefficients = get_coefficients(age, gender, PAL)
    lhs_constant, age_coefficient, height_coefficient, weight_coefficient, rhs_constant = coefficients
    
    # EER Forumla
    # print(f"{lhs_constant} + ({age_coefficient} * {age}) + ({height_coefficient} * {height}) + ({weight_coefficient} * {weight}) + {rhs_constant}")
    EER = lhs_constant + (age_coefficient * age) + (height_coefficient * height) + (weight_coefficient * weight) + rhs_constant
    return {"value": EER}