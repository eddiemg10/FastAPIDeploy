from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *
from ....schemas.HealthMetrics import PALType, GlucoseTest
from ..explanation.explanation_module import ExplanationModule
from app.core.repository.locations import LocationController
from app.core.repository.healthmetrics.blood_sugar import interpret_blood_sugar

class Req:
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)
class KB():
    def __init__(self, fact: Fact):
        self.Explanations = ExplanationModule(fact)
        self.query = []
        self.rules = []
        self.fact = fact
        
        # Rule 1: (Hypoglycemia) If Hypoglycemia detected
        self.ant_is_hypoglycemic = Antecedent(value=getattr(self.fact, "sugar_level", None), operation=Operation.equals , reference="hypoglycemic")
        # if person if hypoglycemic, check whether it's sports induced
        self.ant_is_very_active = Antecedent(value=fact.pal.pal, operation=Operation.equals, reference=PALType.very_active) # Sports induced Hypoglycemia
        self.ant_is_active = Antecedent(value=fact.pal.pal, operation=Operation.equals, reference=PALType.active) # Sports induced Hypoglycemia

        self.ant_is_active_individual = Antecedent(value=getattr(self.fact, "is_an_active_person", None), operation=Operation.equals, reference=True)
        
        self.ant_has_coordinates = Antecedent(value=getattr(self.fact, "coords", None), operation=Operation.exists, reference=None)
        
        self.ant_has_pal = Antecedent(value=getattr(self.fact, "pal", None), operation=Operation.exists, reference=None)
        
        self.ant_has_eer = Antecedent(value=getattr(self.fact, "eer", None), operation=Operation.exists, reference=None)

        self.ant_has_hbA1C = Antecedent(value=getattr(self.fact, "HbA1C", None), operation=Operation.exists, reference=None)
        
        self.ant_has_history = Antecedent(value=getattr(self.fact, "blood_sugar_history", None), operation=Operation.exists, reference=None)
        
        # self.ant_has_cuisine = Antecedent(value=getattr(self.fact, "cuisine", None), operation=Operation.exists, reference=None)
        
        self.ant_has_exclusions = Antecedent(value=getattr(self.fact, "exclude", None), operation=Operation.exists, reference=None)
        
        ###############################################################
        
        self.cons_sports_hypoglycemia = Consequent({
            "explanation" : self.Explanations.x_sport_induced_hypoglycemia,
            "fact_updates" : {"has_sports_hypoglycemia": True},
            "filter": {
                "GI" : ("Medium", fact.blood_sugar_history[0])
            }
        })

        self.cons_active_individual = Consequent({
            "explanation" : self.Explanations.x_active_person,
            "fact_updates" : {"is_an_active_person": True},
        })

        self.cons_infer_pal = Consequent({
            "explanation" : self.Explanations.x_pal,
        })

        self.cons_infer_eer = Consequent({
            "explanation" : self.Explanations.x_estimaed_energy_requirements,
        })

        # self.cons_infer_cuisine = Consequent({
        #         "explanation" : self.Explanations.x_cuisine,
        #         "filter": {
        #             "cuisine" : self.fact.cuisine
        #         }
        # })

        self.cons_infer_exclusions = Consequent({
                "explanation" : self.Explanations.x_exclusions,
        })
        
        if self.fact.coords:
            location_details = LocationController.find_county_and_highlight((fact.coords))
            self.cons_infer_location = Consequent({
                "fact_updates" : {"location": location_details},
                "explanation" : self.Explanations.x_location(location_details),
                "filter": {
                    "location" : "coast"
                }
            })
        
        if self.fact.HbA1C:
            self.fact.HbA1C.update({"test": GlucoseTest.A1C})
            sugar_levels = interpret_blood_sugar(Req(self.fact.HbA1C))
            self.cons_infer_blood_sugar_level = Consequent({
                "fact_updates" : {"blood_sugar_level": sugar_levels, "sugar_level": sugar_levels["level"]},
                "explanation" : self.Explanations.x_sugar_levels(sugar_levels),
                "filter": {
                    "amdr" : sugar_levels
                }
            })
        else:
            sugar_levels = interpret_blood_sugar(Req(fact.blood_sugar_history[0]))
            self.cons_infer_blood_sugar_level = Consequent({
                "fact_updates" : {"blood_sugar_level": sugar_levels, "sugar_level": sugar_levels["level"]},
                "explanation" : self.Explanations.x_sugar_levels(sugar_levels),
                "filter": {
                    "amdr" : sugar_levels
                }
            })
               
    
    def build(self, fact):
        self.fact = fact

        # Infer the Physical Activity Level
        self.rules.append(ProductionRule(id=1, query=self.query, fact=self.fact, antecedents=[self.ant_has_pal], consequents=[self.cons_infer_pal]))
        # Active or not active?
        self.rules.append(ProductionRule(id=2, query=self.query, fact=self.fact, antecedents=[self.ant_is_very_active, self.ant_is_active], consequents=[self.cons_active_individual], logic=Logic.OR))
        # Infer blood sugar level
        self.rules.append(ProductionRule(id=3, query=self.query, fact=self.fact, antecedents=[self.ant_has_hbA1C, self.ant_has_history], consequents=[self.cons_infer_blood_sugar_level], logic=Logic.OR))
        # If active and hypoglycemic, then patient is exposed to sports induced hypoglycmia
        self.rules.append(ProductionRule(id=4, query=self.query, fact=self.fact, antecedents=[self.ant_is_hypoglycemic, self.ant_is_active_individual], consequents=[self.cons_sports_hypoglycemia], logic=Logic.AND))
        # If coordinates are present, Infer Location
        if fact.coords:
            self.rules.append(ProductionRule(id=5, query=self.query, fact=self.fact, antecedents=[self.ant_has_coordinates], consequents=[self.cons_infer_location]))
        # Infer the patient's estimated energy requirements
        self.rules.append(ProductionRule(id=6, query=self.query, fact=self.fact, antecedents=[self.ant_has_eer], consequents=[self.cons_infer_eer]))
        # Infer user's cuisine preference
        # if len(fact.cuisine) > 0:
        #     self.rules.append(ProductionRule(id=7, query=self.query, fact=self.fact, antecedents=[self.ant_has_cuisine], consequents=[self.cons_infer_cuisine]))
        # Infer user's exclusions
        if len(fact.exclude) > 0:
            self.rules.append(ProductionRule(id=8, query=self.query, fact=self.fact, antecedents=[self.ant_has_exclusions], consequents=[self.cons_infer_exclusions]))
        
        

        return self.rules
    
