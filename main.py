from datetime import datetime, timedelta
from math import exp


parse_time = lambda k: int(k.split(":")[0]) + int(k.split(":")[1]) / 60

from datetime import datetime, timedelta

energy_hist = [
    # --- MONDAY (Day 1: Heavy Routine) ---
    {"timestamp": "2026-04-20T08:00:00", "day_idx": 1, "time_float": 8.0, 
     "energy_types": {"cognitive": 0.8, "creative": 0.5, "mental": 0.7, "physical": 0.9}, "overall": 0.72},
    {"timestamp": "2026-04-20T14:00:00", "day_idx": 1, "time_float": 14.0, 
     "energy_types": {"cognitive": 0.4, "creative": 0.3, "mental": 0.4, "physical": 0.6}, "overall": 0.42},
    {"timestamp": "2026-04-20T20:00:00", "day_idx": 1, "time_float": 20.0, 
     "energy_types": {"cognitive": 0.7, "creative": 0.9, "mental": 0.6, "physical": 0.3}, "overall": 0.62},

    # --- TUESDAY (Day 2: The "Tuition" Burnout) ---
    {"timestamp": "2026-04-21T09:00:00", "day_idx": 2, "time_float": 9.0, 
     "energy_types": {"cognitive": 0.9, "creative": 0.4, "mental": 0.8, "physical": 0.7}, "overall": 0.7},
    {"timestamp": "2026-04-21T13:00:00", "day_idx": 2, "time_float": 13.0, # Post-Tuition Crash
     "energy_types": {"cognitive": 0.2, "creative": 0.1, "mental": 0.2, "physical": 0.4}, "overall": 0.22},
    {"timestamp": "2026-04-21T18:00:00", "day_idx": 2, "time_float": 18.0, 
     "energy_types": {"cognitive": 0.5, "creative": 0.6, "mental": 0.5, "physical": 0.6}, "overall": 0.55},

    # --- WEDNESDAY (Day 3: Mid-week Recovery) ---
    {"timestamp": "2026-04-22T10:00:00", "day_idx": 3, "time_float": 10.0, 
     "energy_types": {"cognitive": 0.75, "creative": 0.75, "mental": 0.8, "physical": 0.6}, "overall": 0.72},
    {"timestamp": "2026-04-22T22:00:00", "day_idx": 3, "time_float": 22.0, 
     "energy_types": {"cognitive": 0.8, "creative": 0.4, "mental": 0.5, "physical": 0.2}, "overall": 0.47},

    # --- THURSDAY (Day 4: Peak Productivity) ---
    {"timestamp": "2026-04-23T08:30:00", "day_idx": 4, "time_float": 8.5, 
     "energy_types": {"cognitive": 0.95, "creative": 0.6, "mental": 0.9, "physical": 0.8}, "overall": 0.81},
    {"timestamp": "2026-04-23T15:00:00", "day_idx": 4, "time_float": 15.0, 
     "energy_types": {"cognitive": 0.6, "creative": 0.7, "mental": 0.6, "physical": 0.5}, "overall": 0.6},

    # --- FRIDAY (Day 5: The Friday we are predicting for) ---
    {"timestamp": "2026-04-17T09:00:00", "day_idx": 5, "time_float": 9.0, 
     "energy_types": {"cognitive": 0.8, "creative": 0.5, "mental": 0.8, "physical": 0.7}, "overall": 0.7},
    {"timestamp": "2026-04-17T21:00:00", "day_idx": 5, "time_float": 21.0, 
     "energy_types": {"cognitive": 0.9, "creative": 0.8, "mental": 0.7, "physical": 0.4}, "overall": 0.7},

    # --- WEEKEND (Days 0 & 6: Higher Creative, Late Cognitive) ---
    {"timestamp": "2026-04-19T11:00:00", "day_idx": 0, "time_float": 11.0, 
     "energy_types": {"cognitive": 0.5, "creative": 0.9, "mental": 0.8, "physical": 0.6}, "overall": 0.7},
    {"timestamp": "2026-04-18T23:59:00", "day_idx": 6, "time_float": 23.9, 
     "energy_types": {"cognitive": 0.7, "creative": 0.9, "mental": 0.6, "physical": 0.2}, "overall": 0.6}
]


def predict_energy_at(date, day_idx, time, logs):

    if not logs:
        return {"cognitive": 0.5, "creative": 0.5, "mental": 0.5, "physical": 0.5}

    target_date = datetime.fromisoformat(date)
    results = {}

    for e_type in ["cognitive", "creative", "mental", "physical"]:

        exact_found = False

        for log in logs:
            if abs(log["time_float"] - time) < 0.01:
                results[e_type] = log["energy_types"][e_type]
                exact_found = True
                break

        if exact_found:
            continue

        total_weighted_energy = 0
        total_weight = 0

        for log in logs:
            time_distance = abs(log["time_float"] - time)

            weekday_distance = min(
                abs(log["day_idx"] - day_idx), 7 - abs(log["day_idx"] - day_idx)
            )

            age = abs((target_date - datetime.fromisoformat(log["timestamp"])).days) / 7

            recency = exp(-0.4 * age)

            weight = (
                ((time_distance + 0.05) ** -2)
                * ((weekday_distance + 1) ** -2)
                * recency
            )

            total_weighted_energy += log["energy_types"][e_type] * weight
            total_weight += weight

        results[e_type] = total_weighted_energy / total_weight

    return results


print(predict_energy_at("2026-04-24", 5, 10.3, energy_hist))

task = {
    'name': 'programming',
    'duration': 2, # in hours
    'flow_required': True,
    'energy_needed': {'cognitive': 0.7, 'creative': 0.4, 'mental': 0.2, 'physical': 0},
    'deadline': '2026-04-25T11:00:00'
}

time_slots = {
    '2026-04-24': [
        # FIXED: Biological & Survival
        {'range': (0.0, 7.5),   'name': 'Sleep',             'type': 'fixed', 'resilience': 'none'},
        {'range': (8.0, 8.5),   'name': 'Breakfast/Routine', 'type': 'fixed', 'resilience': 'low'},
        {'range': (13.0, 14.0), 'name': 'Lunch & Nap',       'type': 'fixed', 'resilience': 'low'},
        {'range': (19.0, 20.0), 'name': 'Dinner',            'type': 'fixed', 'resilience': 'low'},
        {'range': (23.0, 24.0), 'name': 'Wind-down/Sleep',   'type': 'fixed', 'resilience': 'none'},

        # FIXED: External Commitments
        {'range': (10.0, 12.5), 'name': 'Tuition/Classes',   'type': 'fixed', 'resilience': 'high'},
        {'range': (16.0, 17.5), 'name': 'Gym/Physical',      'type': 'fixed', 'resilience': 'high'},

        # FLEXIBLE: Already Scheduled Tasks
        {'range': (14.5, 15.5), 'name': 'Study Biology',     'type': 'flex',  'resilience': 'medium'}
    ]
}

