from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *
from app.core.repository.expertipy.kb.kb import KB
from app.core.repository.food import FoodController, FoodGroupController
from app.core.repository.expertipy.explanation.explanation_module import Explanation, ExplanationModule
from app.core.repository.healthmetrics import bmi, blood_sugar, eer
from app.core.schemas.Profile import RecommendationProfile
from app.core.schemas.HealthMetrics import EERIn
# from ..serialize import serializeDict, create_mock_request

from app.core.database import get_database
from fastapi import Depends


def recommend(req: RecommendationProfile):
    # Build a fact
    eer_input = {
      "age" : req.age,
      "height": req.height,
      "weight": req.weight,
      "gender": req.gender,
      "pal": req.pal.pal
    }
    eer_value = eer.calculate_eer_from_dict(eer_input)

    patient = {
    "height": req.height,
    "weight": req.weight,
    "bmi": req.weight/(req.height/100)**2,
    "age": req.age,
    "gender": req.gender,
    "coords": req.coords, #(39,-3),
    "pal": req.pal, #{"pal":"active", "value": 2.43},
    "eer": eer_value['value'],
    # "HbA1C": {
    #   "value": 70,
    #   "units": "mg/dL"
    # },
    "HbA1C": req.HbA1C.__dict__,
    "blood_sugar_history": req.blood_sugar_history,
    "exclude": req.exclude,
  }
    # return req.blood_sugar_history
    fact = Fact(patient)

    # test -> If bmi is between 20 and 30 and eer is less greater than 2650 then recommend foods high in energy
    # ant1 = Antecedent(value=fact.bmi, operation=Operation.between , reference=[20, 30])
    # ant2 = Antecedent(value=fact.eer, operation=Operation.greater , reference=2650)

    # cons1 = Consequent({"energy": "high"})

    # rule = ProductionRule(antecedents=[ant1, ant2], consequents=[cons1], logic="OR")
    query = []
    knowledge_base = KB(fact)
    rules = knowledge_base.build(fact)
    visited_rules = set()
    query_builder=[]
    ctr = 0
    while ctr < 4:
      rule_triggered = False
      knowledge_base = KB(fact)
      # print(vars(fact), "\n\n")
      rules = knowledge_base.build(fact)
      # print(vars(knowledge_base.fact), "\n\n")
      for rule in rules:
        if rule.evaluate() and rule.id not in visited_rules:
          query, fact = rule.execute()  # Pass the fact to execute method
          if not len(query) < len(query_builder):
            query_builder = query
          else:
            query_builder.append(query)
          visited_rules.add(rule.id)
          print(query_builder)
          print(visited_rules)
          rule_triggered = True
      ctr += 1

      if not rule_triggered:
        print("No match found")
        break
    
    query_builder.append(ExplanationModule.x_fructose(0.12 * fact.eer))
    if fact.age < 1:
      query_builder = [Explanation(text=f"The age of the patient is too young to recommend any foods.")]
    # return query_builder
    sugar_level = getattr(fact, "blood_sugar_level", None)['level']
    carb_percentage, protein_percentage, fat_percentage = getAMDR(query_builder, sugar_level)
    
    cals_from_carbs = carb_percentage/100*fact.eer
    cals_from_protein = protein_percentage/100*fact.eer
    cals_from_fat = fat_percentage/100*fact.eer
    
    # return (carb_percentage, protein_percentage, fat_percentage)

    foods = FoodController.index(page=1, size=600 , db=get_database(), groups=None)
    
    FG = FoodGroups()
    food_plan = {
      "summary": {
        "recommended_calories": fact.eer,
        "from_carbs": cals_from_carbs,
        "from_protein":cals_from_protein,
        "other": cals_from_fat
      } 
        }
    number_of_meals = 5
    if number_of_meals == 5:
      kcal_distribution = meal_calory_distribution(number_of_meals, fact.eer)
      breakfast_kcal, morning_snack_kcal, lunch_kcal, afternoon_snack_kcal, dinner_kcal = kcal_distribution
      breakfast_filter =  {
      "GI": (0, 55), 
      "group": [FG.beverages, FG.cereals, FG.startchy_roots, FG.fruits], 
      "tags": "breakfast",
      # "location": "coast" 
      # "exclude": "1234"
      }
      if fact.age < 1:
        breakfast_filter = {}
        breakfast_filter['tags'] = "infant"
      print(breakfast_filter)
      breakfast_results = FoodController.filter(get_database(), breakfast_filter)
      breakfast_label = {
        "recommended_calories": breakfast_kcal,
        "from_carbs": carb_percentage/100*breakfast_kcal,
        "from_protein": protein_percentage/100*breakfast_kcal,
        "other": fat_percentage/100*breakfast_kcal
      }
      food_plan.update({"breakfast": [breakfast_label, breakfast_results]})

      ################################
      groups = [FG.mixed, FG.meats_and_poultry, FG.fish, FG.vegetables, FG.legumes, FG.fruits]

      if "meat" in fact.exclude:
        groups.remove(FG.meats_and_poultry)
      if "fish" in fact.exclude:
        groups.remove(FG.fish)

      
    
      main_meal_filter = {
      # "GI": (0, 100), 
      "group": groups, 
      "tags": "", 
      "location": "coast",
      # "exclude": ["meat"]
      }
      if fact.age < 1:
        main_meal_filter = {}
        main_meal_filter['tags'] = "infant"
      main_meal_results = FoodController.filter(get_database(), main_meal_filter)
      lunch_results = {}
      dinner_results = {}
        # return main_meal_results

        # for group,food_items in main_meal_results.items():
        #   if len(food_items) < 4:
        #     lunch_results[group] = food_items
        #     dinner_results[group] = food_items
        #   else:
        #     items = len(food_items)
        #     for i in range(items):
        #       if i % 2 == 0:
        #         if(lunch_results.get(group, None)):
        #           lunch_results[group].append(food_items[i])
        #         else:
        #           lunch_results[group]= [food_items[i]]

        #         # lunch_results.update({group: lunch_results.get(group, []).append(food_items[i])})
        #       else:
        #         if(lunch_results.get(group, None)):
        #           lunch_results[group].append(food_items[i])
        #         else:
        #           lunch_results[group]= food_items[i]
        #         # dinner_results.update({group: dinner_results.get(group, []).append(food_items[i])})

      lunch_results, dinner_results = splitFods(main_meal_results, lunch_results, dinner_results)

      # food_plan.update({"lunch": lunch_results, "dinner": dinner_results})

      lunch_label = {
        "recommended_calories": lunch_kcal,
        "from_carbs": carb_percentage/100*lunch_kcal,
        "from_protein": protein_percentage/100*lunch_kcal,
        "other": fat_percentage/100*lunch_kcal
      }
      # food_plan.update({"lunch": [lunch_label, lunch_results]})

      dinner_label = {
        "recommended_calories": dinner_kcal,
        "from_carbs": carb_percentage/100*dinner_kcal,
        "from_protein": protein_percentage/100*dinner_kcal,
        "other": fat_percentage/100*dinner_kcal
      }
      # food_plan.update({"dinner": [dinner_label, dinner_results]})
      # return main_meal_results

      snack_filter = {
      "GI": (0, 85), 
      "group": [FG.dairy, FG.nuts_seeds, FG.vegetables, FG.fruits], 
      "tags": "snack", 
      # "location": "coast"
      # "exclude": ["meat"]
      }
      if fact.age < 1:
        snack_filter = {}
        snack_filter['tags'] = "infant"
      snack_results = FoodController.filter(get_database(), snack_filter)

      early_snack_results = {}
      late_snack_results = {}
      early_snack_results, late_snack_results = splitFods(main_meal_results, early_snack_results, late_snack_results)
      early_snack_label = {
        "recommended_calories": morning_snack_kcal,
        "from_carbs": carb_percentage/100*morning_snack_kcal,
        "from_protein": protein_percentage/100*morning_snack_kcal,
        "other": fat_percentage/100*morning_snack_kcal
      }
      food_plan.update({"morning_snack": [early_snack_label, early_snack_results]})
      food_plan.update({"lunch": [lunch_label, lunch_results]})

      late_snack_label = {
        "recommended_calories": afternoon_snack_kcal,
        "from_carbs": carb_percentage/100*afternoon_snack_kcal,
        "from_protein": protein_percentage/100*afternoon_snack_kcal,
        "other": fat_percentage/100*afternoon_snack_kcal
      }
      food_plan.update({"afternoon_snack": [late_snack_label, late_snack_results]})
      food_plan.update({"dinner": [dinner_label, dinner_results]})

      # food_plan.update({"snacks": snack_results})
    else:
      kcal_distribution = meal_calory_distribution(number_of_meals, fact.eer)
      breakfast_kcal, lunch_kcal, dinner_kcal = kcal_distribution


    # filter =  {
    #   "GI": (0, 55), 
    #   # "location": "coast",
    #   "group": "653e83acfe351cbe41209807", 
    #   "tags": "breakfast", 
    #   # "exclude": "1234"
    # }
    # results = FoodController.filter(get_database(), filter)
    return {"recommendations": food_plan, "explanations": query_builder}
    return food_plan
    return fact
      

def getAMDR(query, sugar_level):
  PROTEIN_AMDR = (10, 35)
  CARBOHYDRATES_AMDR = (45, 65)
  FAT_AMDR = (20, 35)

  if sugar_level == "hypoglycemic":
    CARBOHYDRATES_AMDR = (55, 65)
    PROTEIN_AMDR = (10, 20)

  elif sugar_level == "prediabetic":
    CARBOHYDRATES_AMDR = (50, 55)
    PROTEIN_AMDR = (15, 25)

  elif sugar_level == "diabetic":
    CARBOHYDRATES_AMDR = (45, 50)
    PROTEIN_AMDR = (25, 35)
  else:
    CARBOHYDRATES_AMDR = (50, 65)

  # Adjust individual AMDRs proportionally to ensure they add up to 100%
  carb_percentage = sum(CARBOHYDRATES_AMDR) / 2
  protein_percentage = sum(PROTEIN_AMDR) /2
  fat_percentage = sum(FAT_AMDR) / 2

  return (carb_percentage, protein_percentage, fat_percentage)
 



def meal_calory_distribution(number_of_meals, eer):
  kcal_distribution = ()
  if number_of_meals == 3:
    breakfast_kcal = 0.2 * eer
    lunch_kcal = 0.41 * eer
    dinner_kcal = 0.39 * eer
    kcal_distribution = (breakfast_kcal, lunch_kcal, dinner_kcal)
  else:
    breakfast_kcal = 0.18 * eer
    morning_snack_kcal = 0.05 * eer
    lunch_kcal = 0.36 * eer
    afternoon_snack = 0.1 * eer
    dinner_kcal = 0.31 * eer
    kcal_distribution = (breakfast_kcal, morning_snack_kcal, lunch_kcal, afternoon_snack, dinner_kcal)
  
  return kcal_distribution

def splitFods(main_results, result1, result2):
  for group,food_items in main_results.items():
        if len(food_items) < 4:
          result1[group] = food_items
          result2[group] = food_items
        else:
          items = len(food_items)
          for i in range(items):
            if i % 2 == 0:
              if(result1.get(group, None)):
                result1[group].append(food_items[i])
              else:
                result1[group]= [food_items[i]]

            else:
              if(result2.get(group, None)):
                result2[group].append(food_items[i])
              else:
                result2[group]= [food_items[i]]
  return result1, result2
   


class FoodGroups():
  def __init__(self):
    self.cereals = "653e83a8fe351cbe412097ed"
    self.startchy_roots = "653e83aafe351cbe412097f0"
    self.legumes = "653e83aafe351cbe412097f3"
    self.vegetables = "653e83aafe351cbe412097f6"
    self.fruits="653e83abfe351cbe412097f9"
    self.dairy="653e83abfe351cbe412097fb"
    self.meats_and_poultry="653e83abfe351cbe412097fd"
    self.fish="653e83abfe351cbe412097ff"
    self.oils_fats="653e83acfe351cbe41209801"
    self.nuts_seeds="653e83acfe351cbe41209803"
    self.sweeteners="653e83acfe351cbe41209805"
    self.beverages="653e83acfe351cbe41209807"
    self.condiments="653e83adfe351cbe41209809"
    self.insects="653e83adfe351cbe4120980b"
    self.mixed = "653e83adfe351cbe4120980d"