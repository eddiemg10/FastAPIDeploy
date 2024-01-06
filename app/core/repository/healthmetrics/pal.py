from fastapi import HTTPException
from dataclasses import dataclass
from ..serialize import serializeList
from app.core.schemas.HealthMetrics import PALType 

@dataclass
class Activity():
    activity: str
    """
    Energy costs of activities, expressed as multiples of basal metabolic rate, or PAR
    """
    par: float

activities = [
Activity("Sleeping", 1),
Activity("Personal care (dressing, showering)", 2.3),
Activity("Eating", 1.5),
Activity("Cooking", 2.1),
Activity("Sitting(office work, selling produce, rending shop)", 1.5),
Activity("General household work", 2.8),
Activity("Driving", 2.0),
Activity("Walking at varying paces without a load", 3.2),
Activity("Light leisure activities (watching TV, chatting)", 1.4),
Activity("Standing, carrying light loads (waiting on tables, arranging merchandise)", 2.2),
Activity("Commuting on the bus", 1.2),
Activity("Low intensity aerobic exercise", 4.2),
Activity("Non-mechanized agricultural work (planting, weeding, gathering)", 4.1),
Activity("Collecting water/wood", 4.4),
Activity("Non-mechanized domestic chores (sweeping, washing clothes and dishes by hand)", 2.3)
]
def retrieve_pal_activites():
    return activities


def calculate_pal(request):
    # Time x Energy Cost
    total = 0
    hours = 0
    for activity in request:
        hours += activity.time
        total += (activity.par * activity.time)
    
    if(hours > 24):
        raise HTTPException(status_code=400, detail=f"Sum total of daily activities cannot exceed 24 hours. Received {hours} hours")
    
    mean_pal = total/24

    if mean_pal < 1.7:
        activity_level = PALType.inactive
    elif mean_pal >= 1.7 and mean_pal < 2:
        activity_level = PALType.low_active
    elif mean_pal >= 2 and mean_pal <= 2.4:
        activity_level = PALType.active
    else:
        activity_level = PALType.very_active

    return {"pal": activity_level, "value": mean_pal}

