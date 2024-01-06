from app.core.repository.expertipy.facts.fact import Fact

class Explanation():
    """
    Explanation Module
    """
    def __init__(self, text: str, link: str = None):
        self.text = text,
        self.link = link


class ExplanationModule():
    def __init__(self, fact: Fact):
        self.x_15_15_rule = Explanation(
            text=f"Your Blood sugar is {fact.blood_sugar_history[0]}. Since this is between the 55-69 mg/dL range, it is recommended to raise it by following the 15-15 rule: have 15 grams of carbs and check your blood sugar after 15 minutes. If it’s still below your target range, have another serving. Once it’s in range, eat a nutritious meal or snack to ensure it doesn’t get too low again.",
            link="https://www.cdc.gov/diabetes/basics/low-blood-sugar-treatment.html"),
        
        self.x_sport_induced_hypoglycemia = Explanation(
            text=f"Your activity level is  {fact.pal.pal}. This indicates that you are in danger of 'Sport induced Hpoglycemia. This may be because you did not eat low GI food before physically demanding activity and either ate nothing after the activity or ate low GI foods afterwards. Medium GI foods have been recommended as a result since you're diabetic. NOTE: Check the iron content of the foods you take as you have a 30-70% higher iron requirement than normally active individuals'",
        link="https://www.gifoundation.com/nutrition/low-blood-sugar/#:~:text=Sport%20induced%20Hypoglycemia,a%20lot%20better."),

        self.x_active_person = Explanation(
            text=f"Your activity level ({fact.pal.pal}) indicates you engage in physically demanding tasks"
        ),

        self.x_pal = Explanation(
            text=f"Based on the activities you engage in, Your estimated Basal Metabolic Rate (BMR) over 24 hours is {fact.pal.value}, which indicates a Phsical Activity Level (PAL) of {fact.pal.pal}",
        link="Link to docs"), #TODO: Link to docs

        self.x_estimaed_energy_requirements = Explanation(
            text=f"Based on your age ({fact.age}), gender ({fact.gender}) and PAL ({fact.pal.pal}) your daily Estimated Energy Requirements is {fact.eer} kcal. The recommended foods have been curated to meet this requirement",
        link="Link to docs"), #TODO: Link to docs

        self.x_infant= Explanation(
            text=f"The age of the patient is too young to recommend any foods."
        )
        # self.x_cuisine = Explanation(
        #     text=f"You have a cuisine preference: {fact.cuisine}, which has also been used to filter food recommendations"
        # )

        self.x_exclusions = Explanation(
            text=f"Some foods have been excluded: {fact.exclude}"
        )

    def x_location(self, location):
        return Explanation(
            text=f"Your location has been mapped to be in {location['county']} county in the {location['region']} region. The recommended foods have therefore factored this in mind",
        link=location['image'])
    
    def x_sugar_levels(self, levels):
        return Explanation(
            text=f"Your blood sugar levels : {levels['blood_sugar_level'][0]["value"]} {levels['blood_sugar_level'][0]['units'].value} indicate a {levels['level']} blood sugar level. The recommended foods have therefore factored this in mind",
        link="Link to docs") #TODO: link to docs
    
    def x_fructose(fructose_cals):
        return Explanation(
            text=f"While the fruits recommended are generally healhty, it is important to ensure they don't exceed 12% of your daily energy requirements, which for you is {fructose_cals} calories. This is because when fructose is consumed, it is metabolized primarily in the liver. This can lead to an increase in the production of triglycerides, high levels of which can increase the risk of heart disease and stroke."
            )
    
   
