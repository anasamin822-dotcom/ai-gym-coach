"""
Gym Trainer Nutrition & Workout Planner Service
Calculates BMI, BMR, TDEE, Macros, and generates tailored gym-grade meal plans and workout splits.
"""
from typing import Dict, Any, List


def calculate_bmi(height_cm: float, weight_kg: float) -> Dict[str, Any]:
    """Calculate BMI, category, healthy weight range and health risk status."""
    if height_cm <= 0 or weight_kg <= 0:
        return {
            "bmi": 0.0,
            "category": "Unknown",
            "badge_color": "#888888",
            "message": "Please enter valid height and weight.",
            "min_healthy_weight": 0.0,
            "max_healthy_weight": 0.0
        }

    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 1)

    min_weight = round(18.5 * (height_m ** 2), 1)
    max_weight = round(24.9 * (height_m ** 2), 1)

    if bmi < 18.5:
        category = "Underweight (Kam Wazan)"
        badge_color = "#3498db" # Blue
        message = "Aapka wazan normal se kam hai. Muscle mass aur healthy weight gain par focus karein."
    elif 18.5 <= bmi <= 24.9:
        category = "Normal / Healthy Weight (Fit)"
        badge_color = "#2ecc71" # Green
        message = "Badhai ho! Aapka BMI bilkul healthy range me hai. Lean muscle gain aur fitness maintain karein."
    elif 25.0 <= bmi <= 29.9:
        category = "Overweight (Vajan Zyada)"
        badge_color = "#f39c12" # Orange
        message = "Aapka BMI thoda high hai. Fat loss aur strength training se aap healthy range me aa sakte hain."
    else:
        category = "Obese (Motapa)"
        badge_color = "#e74c3c" # Red
        message = "High health risk category. Consistent calorie deficit, cardio aur guided strength routine follow karein."

    return {
        "bmi": bmi,
        "category": category,
        "badge_color": badge_color,
        "message": message,
        "min_healthy_weight": min_weight,
        "max_healthy_weight": max_weight
    }


def calculate_bmr_tdee(gender: str, age: int, height_cm: float, weight_kg: float, activity_level: str) -> Dict[str, float]:
    """
    Calculate Basal Metabolic Rate (Mifflin-St Jeor) and Total Daily Energy Expenditure.
    """
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    activity_multipliers = {
        "Sedentary (No exercise / Desk job)": 1.2,
        "Lightly Active (1-3 days/week exercise)": 1.375,
        "Moderately Active (3-5 days/week gym)": 1.55,
        "Very Active (6-7 days/week intense gym)": 1.725,
        "Extremely Active (Athletic training / physical job)": 1.9
    }
    multiplier = activity_multipliers.get(activity_level, 1.55)
    tdee = bmr * multiplier

    return {
        "bmr": round(bmr),
        "tdee": round(tdee)
    }


def calculate_nutrition_targets(tdee: float, weight_kg: float, goal: str) -> Dict[str, Any]:
    """
    Calculate target calories and macronutrients (Protein, Carbs, Fats, Water) based on fitness goal.
    """
    if goal == "Fat Loss / Cutting":
        target_calories = round(tdee - 500)
        protein_factor = 2.0  # 2.0g per kg bodyweight
        fat_pct = 0.25
    elif goal == "Muscle Building / Lean Bulk":
        target_calories = round(tdee + 300)
        protein_factor = 2.0
        fat_pct = 0.25
    elif goal == "Weight Gain / Hard Bulking":
        target_calories = round(tdee + 500)
        protein_factor = 1.8
        fat_pct = 0.25
    else:  # Maintenance & General Fitness
        target_calories = round(tdee)
        protein_factor = 1.6
        fat_pct = 0.25

    # Don't let calories drop too low
    target_calories = max(1200, target_calories)

    protein_g = round(weight_kg * protein_factor)
    protein_kcal = protein_g * 4

    fat_kcal = target_calories * fat_pct
    fat_g = round(fat_kcal / 9)

    remaining_kcal = max(0, target_calories - protein_kcal - fat_kcal)
    carbs_g = round(remaining_kcal / 4)

    # Water intake target in liters (~35ml per kg + 500ml for workout)
    water_liters = round((weight_kg * 0.035) + 0.5, 1)

    return {
        "target_calories": target_calories,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fats_g": fat_g,
        "water_liters": water_liters
    }


def get_real_trainer_food_plan(goal: str, diet_pref: str) -> List[Dict[str, Any]]:
    """
    Returns a comprehensive, timed gym-trainer food plan with real Indian & global fitness options.
    """
    is_veg = "veg" in diet_pref.lower() and "non" not in diet_pref.lower()

    if goal in ["Fat Loss / Cutting", "Overweight Reduction"]:
        if is_veg:
            meals = [
                {
                    "time": "07:00 AM",
                    "meal": "Morning Detox & Metabolism Booster",
                    "items": "1 glass lukewarm water + 1/2 lemon + 1 tsp chia seeds OR 1 cup warm green tea.",
                    "notes": "Digestion activate karta hai aur bloating kam karta hai."
                },
                {
                    "time": "08:30 AM",
                    "meal": "High-Protein Breakfast (Nashta)",
                    "items": "50g Oats cooked in water/toned milk with 1 scoop whey/soya protein + 5 almonds OR 2 Moong Dal Besan Chilla with mint chutney + 50g low-fat paneer.",
                    "notes": "High fiber + high protein se lambe samay tak bhookh nahi lagti."
                },
                {
                    "time": "11:30 AM",
                    "meal": "Mid-Morning Refreshment",
                    "items": "1 Apple / 1 Orange / Papaya bowl + 1 glass thin chhaas (buttermilk) with roasted jeera.",
                    "notes": "Hydration aur electrolytes provide karta hai."
                },
                {
                    "time": "01:30 PM",
                    "meal": "Clean Balanced Lunch",
                    "items": "1-2 Multigrain / Bran Roti (no butter) + 1 large bowl Dal / Rajma + 100g sauteed Low-Fat Paneer / Soya Chunks + Big green cucumber-tomato salad.",
                    "notes": "Pehle salad khao, taaki overeating na ho."
                },
                {
                    "time": "05:00 PM",
                    "meal": "Pre-Workout Power Snack (Gym se 45m pehle)",
                    "items": "1 black coffee (no sugar) + 1 small banana OR 1 slice brown bread with 1 tsp natural peanut butter.",
                    "notes": "Instant workout energy without heavy stomach."
                },
                {
                    "time": "07:00 PM",
                    "meal": "Post-Workout Recovery (Workout ke 30m andar)",
                    "items": "1 scoop Whey Protein in water OR 200ml sattu drink / buttermilk + 30g boiled chana.",
                    "notes": "Muscle recovery aur soreness kam karne ke liye essential."
                },
                {
                    "time": "08:30 PM",
                    "meal": "Light & Lean Dinner",
                    "items": "1 big bowl Mix Vegetable / Palak / Tomato soup + 150g grilled Tofu or Paneer salad with lemon dressing (Avoid heavy carbs at night).",
                    "notes": "Night me low-carb meal fat loss ko double accelerate karta hai."
                },
                {
                    "time": "10:00 PM",
                    "meal": "Bedtime Recovery",
                    "items": "1 cup warm water with pinch of cinnamon OR warm chamomile/green tea.",
                    "notes": "Sound sleep and overnight fat burn."
                }
            ]
        else:
            meals = [
                {
                    "time": "07:00 AM",
                    "meal": "Morning Detox & Metabolism Booster",
                    "items": "1 glass lukewarm water + 1/2 lemon + 1 tsp chia seeds OR 1 cup warm black coffee.",
                    "notes": "Awakens metabolism and clears morning water retention."
                },
                {
                    "time": "08:30 AM",
                    "meal": "High-Protein Breakfast",
                    "items": "4 Boiled Egg Whites + 1 Whole Egg (omlette/boiled) + 1 slice toasted brown bread + 5 almonds OR 50g Oats with 1 scoop protein.",
                    "notes": "Pure high biological value protein to preserve lean muscle."
                },
                {
                    "time": "11:30 AM",
                    "meal": "Mid-Morning Refreshment",
                    "items": "1 Apple / Grapefruit + 1 glass green tea or chilled salted buttermilk.",
                    "notes": "Keeps metabolic rate elevated throughout the morning."
                },
                {
                    "time": "01:30 PM",
                    "meal": "Clean Balanced Lunch",
                    "items": "150g Grilled/Boiled Chicken Breast OR 150g Fish + 1 small cup brown rice or 1 multigrain roti + big bowl green salad with broccoli & cucumber.",
                    "notes": "High protein, clean slow-digesting carbs."
                },
                {
                    "time": "05:00 PM",
                    "meal": "Pre-Workout Power Snack (45m before workout)",
                    "items": "1 shot strong black coffee + 1 apple or 1 small banana.",
                    "notes": "Caffeine for focus and nitric oxide boost, light carbs for stamina."
                },
                {
                    "time": "07:00 PM",
                    "meal": "Post-Workout Recovery (Within 30m)",
                    "items": "1 scoop Whey Isolate in cold water + 3 boiled egg whites.",
                    "notes": "Immediate amino acid delivery to repairing muscle tissue."
                },
                {
                    "time": "08:30 PM",
                    "meal": "Light High-Protein Dinner",
                    "items": "150g Stir-fried Chicken Breast or Fish with bell peppers, beans, and cabbage soup. No heavy carbs.",
                    "notes": "Zero sugar, minimal fats, pure protein for overnight recovery."
                },
                {
                    "time": "10:00 PM",
                    "meal": "Bedtime Recovery",
                    "items": "1 cup warm water or green tea. Stay off screens 30 min before bed.",
                    "notes": "Restorative sleep triggers growth hormone and accelerates fat loss."
                }
            ]
    else:  # Muscle Building / Lean Bulk / Weight Gain
        if is_veg:
            meals = [
                {
                    "time": "07:00 AM",
                    "meal": "Morning Anabolic Kickstart",
                    "items": "1 glass lukewarm water + 6-8 soaked almonds + 2 walnuts + 2 whole dates (Khajoor).",
                    "notes": "Healthy fats aur natural micronutrients boost."
                },
                {
                    "time": "08:30 AM",
                    "meal": "Power Builder Breakfast",
                    "items": "70g Oats cooked in full cream milk + 1 scoop protein/peanut butter + 1 chopped banana OR 3 Paneer Stuffed Roti with fresh curd.",
                    "notes": "Quality calories + high protein muscle synthesize karne ke liye."
                },
                {
                    "time": "11:30 AM",
                    "meal": "Mid-Morning Muscle Snack",
                    "items": "1 bowl Boiled Kala Chana / Sprouted Moong chaat with lemon & onion + 1 banana shake / tender coconut water.",
                    "notes": "Clean complex carbs aur sustained energy."
                },
                {
                    "time": "01:30 PM",
                    "meal": "Heavy Weightlifter Lunch",
                    "items": "2-3 Multigrain Roti + 1 bowl Jeera/White Rice + 150g Paneer Bhurji / Tofu Curry + 1 large bowl Thick Dal + Fresh curd.",
                    "notes": "Complete amino acid profile (grains + legumes + dairy)."
                },
                {
                    "time": "05:00 PM",
                    "meal": "Pre-Workout Anabolic Fuel (1 hr before workout)",
                    "items": "2 slices Brown bread with 2 tbsp Peanut Butter + 1 Banana + 1 cup Black Coffee.",
                    "notes": "Glycogen load for high intensity lifts and heavy squats/presses."
                },
                {
                    "time": "07:00 PM",
                    "meal": "Post-Workout Muscle Growth Shake",
                    "items": "1-2 scoops Whey Protein + 1 scoop Dextrose/banana OR 300ml banana-peanut butter shake with 50g paneer.",
                    "notes": "Spikes protein synthesis right in the hypertrophy window."
                },
                {
                    "time": "08:45 PM",
                    "meal": "Nutrient-Dense Dinner",
                    "items": "2 Roti + 1 bowl Rice + 100g Soya Chunks or Paneer + Mix vegetable sabzi + Green salad.",
                    "notes": "Replenishes glycogen stores for next day's training."
                },
                {
                    "time": "10:15 PM",
                    "meal": "Bedtime Casein Drink",
                    "items": "1 glass warm Milk with haldi (turmeric) & pinch of black pepper OR 50g fresh raw paneer.",
                    "notes": "Slow digesting casein protein provides muscle repair all night."
                }
            ]
        else:
            meals = [
                {
                    "time": "07:00 AM",
                    "meal": "Morning Anabolic Kickstart",
                    "items": "1 glass lukewarm water + 8 soaked almonds + 2 walnuts + 2 dates.",
                    "notes": "Natural testosterone and hormone building fats."
                },
                {
                    "time": "08:30 AM",
                    "meal": "Power Builder Breakfast",
                    "items": "3 Whole Eggs + 3 Egg Whites (scrambled/boiled) + 2 slices toasted brown bread + 1 glass fresh juice or banana.",
                    "notes": "High protein, healthy cholesterol for natural hormone production."
                },
                {
                    "time": "11:30 AM",
                    "meal": "Mid-Morning Shake / Snack",
                    "items": "High-protein smoothie (Oats + Milk + Peanut butter + 1 Banana) OR 1 bowl sprout salad.",
                    "notes": "Easy dense calories to stay in anabolic surplus."
                },
                {
                    "time": "01:30 PM",
                    "meal": "Weightlifter Lunch",
                    "items": "200g Chicken Breast / Mutton / Fish + 1.5 cups Rice + 1 bowl Dal + Big salad with olive oil dressing.",
                    "notes": "Lean mass building foundation meal."
                },
                {
                    "time": "05:00 PM",
                    "meal": "Pre-Workout Fuel (1 hr before)",
                    "items": "1 boiled sweet potato (shakarkand) OR 2 slices brown bread with peanut butter + 1 cup black coffee.",
                    "notes": "Unstoppable gym energy and insane pump."
                },
                {
                    "time": "07:00 PM",
                    "meal": "Post-Workout Anabolic Window",
                    "items": "1 scoop Whey Protein in water + 1 Banana + 4 boiled egg whites.",
                    "notes": "Rapid glycogen replenishment and fast muscle protein synthesis."
                },
                {
                    "time": "08:45 PM",
                    "meal": "Heavy Recovery Dinner",
                    "items": "150-200g Chicken Breast / Fish + 2 Rotis or Rice + Green vegetables (beans, spinach) + Curd.",
                    "notes": "Clean high protein dinner with essential micronutrients."
                },
                {
                    "time": "10:15 PM",
                    "meal": "Bedtime Casein Recovery",
                    "items": "1 glass warm Milk with pinch of turmeric OR 30g raw almonds.",
                    "notes": "Prevents muscle catabolism during 8 hours of sleep."
                }
            ]

    return meals


def get_gym_workout_routine(goal: str) -> List[Dict[str, Any]]:
    """
    Returns a complete, real trainer weekly gym split matching the app's core exercises
    (Squats, Push-ups, Biceps Curls, Shoulder Press, Lunges).
    """
    if "loss" in goal.lower() or "cutting" in goal.lower():
        routine = [
            {
                "day": "Monday",
                "focus": "Chest, Shoulders & High-Rep Core",
                "exercises": [
                    {"name": "Standard Push-ups (Form Verified)", "sets": "4 sets", "reps": "15-20 reps", "rest": "45 sec"},
                    {"name": "Dumbbell Shoulder Press", "sets": "4 sets", "reps": "12-15 reps", "rest": "60 sec"},
                    {"name": "Incline Dumbbell Press", "sets": "3 sets", "reps": "12 reps", "rest": "60 sec"},
                    {"name": "Lateral Raises (Side Delts)", "sets": "4 sets", "reps": "15 reps", "rest": "45 sec"},
                    {"name": "HIIT Treadmill / Jump Rope", "sets": "15 mins", "reps": "Interval sprints", "rest": "30 sec"}
                ]
            },
            {
                "day": "Tuesday",
                "focus": "Legs Hyper-Burn & Glutes",
                "exercises": [
                    {"name": "Bodyweight / Goblet Squats (Form Tracked)", "sets": "4 sets", "reps": "15-20 reps", "rest": "60 sec"},
                    {"name": "Walking Lunges (Each Leg)", "sets": "4 sets", "reps": "12-15 reps", "rest": "60 sec"},
                    {"name": "Leg Press", "sets": "3 sets", "reps": "15 reps", "rest": "60 sec"},
                    {"name": "Calf Raises", "sets": "4 sets", "reps": "20 reps", "rest": "45 sec"},
                    {"name": "Plank Hold", "sets": "3 sets", "reps": "45-60 sec", "rest": "45 sec"}
                ]
            },
            {
                "day": "Wednesday",
                "focus": "Back, Biceps & Cardio Recovery",
                "exercises": [
                    {"name": "Lat Pulldown / Pull-ups", "sets": "4 sets", "reps": "12-15 reps", "rest": "60 sec"},
                    {"name": "Seated Cable Rows", "sets": "4 sets", "reps": "12-15 reps", "rest": "60 sec"},
                    {"name": "Dumbbell Biceps Curls (Form Tracked)", "sets": "4 sets", "reps": "15 reps", "rest": "45 sec"},
                    {"name": "Hammer Curls", "sets": "3 sets", "reps": "15 reps", "rest": "45 sec"},
                    {"name": "Incline Treadmill Walk", "sets": "20 mins", "reps": "Brisk walk (12% inc)", "rest": "--"}
                ]
            },
            {
                "day": "Thursday",
                "focus": "Active Recovery & Mobility",
                "exercises": [
                    {"name": "Full Body Dynamic Stretching", "sets": "15 mins", "reps": "Mobility work", "rest": "--"},
                    {"name": "Light Jogging / Outdoor Walk", "sets": "30 mins", "reps": "Low intensity", "rest": "--"},
                    {"name": "Foam Rolling / Core Crunches", "sets": "3 sets", "reps": "25 reps", "rest": "45 sec"}
                ]
            },
            {
                "day": "Friday",
                "focus": "Full Body Compound Shred",
                "exercises": [
                    {"name": "Barbell / Dumbbell Squats", "sets": "4 sets", "reps": "12-15 reps", "rest": "60 sec"},
                    {"name": "Push-ups to Failure", "sets": "3 sets", "reps": "Max reps", "rest": "60 sec"},
                    {"name": "Overhead Shoulder Press", "sets": "4 sets", "reps": "12 reps", "rest": "60 sec"},
                    {"name": "Walking Lunges with Dumbbells", "sets": "3 sets", "reps": "12 reps/leg", "rest": "60 sec"},
                    {"name": "Mountain Climbers + Burpees", "sets": "4 sets", "reps": "30 sec on / 30 sec off", "rest": "30 sec"}
                ]
            },
            {
                "day": "Saturday",
                "focus": "Arms, Core & Metabolic Circuit",
                "exercises": [
                    {"name": "Biceps Barbell Curl", "sets": "4 sets", "reps": "12-15 reps", "rest": "45 sec"},
                    {"name": "Triceps Rope Pushdowns", "sets": "4 sets", "reps": "15 reps", "rest": "45 sec"},
                    {"name": "Hanging Leg Raises", "sets": "4 sets", "reps": "15 reps", "rest": "45 sec"},
                    {"name": "Russian Twists", "sets": "3 sets", "reps": "20 reps/side", "rest": "30 sec"}
                ]
            },
            {
                "day": "Sunday",
                "focus": "Complete Rest & Muscle Repair",
                "exercises": [
                    {"name": "Hydration, Healthy Eating & 8-Hour Deep Sleep", "sets": "All day", "reps": "Rest", "rest": "--"}
                ]
            }
        ]
    else:  # Muscle Building / Hypertrophy / Bulk
        routine = [
            {
                "day": "Monday",
                "focus": "Chest & Triceps (Push Day 1)",
                "exercises": [
                    {"name": "Barbell Flat Bench Press", "sets": "4 sets", "reps": "8-10 reps (Heavy)", "rest": "90 sec"},
                    {"name": "Incline Dumbbell Press", "sets": "4 sets", "reps": "10-12 reps", "rest": "75 sec"},
                    {"name": "Push-ups (Chest Finisher)", "sets": "3 sets", "reps": "15-20 reps", "rest": "60 sec"},
                    {"name": "Dips (Bodyweight or Weighted)", "sets": "3 sets", "reps": "10-12 reps", "rest": "75 sec"},
                    {"name": "Triceps Skull Crushers", "sets": "4 sets", "reps": "10-12 reps", "rest": "60 sec"}
                ]
            },
            {
                "day": "Tuesday",
                "focus": "Back & Biceps (Pull Day 1)",
                "exercises": [
                    {"name": "Deadlifts or Barbell Rows", "sets": "4 sets", "reps": "6-8 reps (Heavy)", "rest": "120 sec"},
                    {"name": "Wide Grip Lat Pulldown", "sets": "4 sets", "reps": "10-12 reps", "rest": "75 sec"},
                    {"name": "Single Arm Dumbbell Row", "sets": "3 sets", "reps": "10 reps/side", "rest": "60 sec"},
                    {"name": "Dumbbell Biceps Curls (Form Tracked)", "sets": "4 sets", "reps": "10-12 reps", "rest": "60 sec"},
                    {"name": "Hammer Curls (Brachialis)", "sets": "3 sets", "reps": "10-12 reps", "rest": "60 sec"}
                ]
            },
            {
                "day": "Wednesday",
                "focus": "Legs & Calves (Heavy Lower Day)",
                "exercises": [
                    {"name": "Barbell Back Squats (Deep Form Tracked)", "sets": "4 sets", "reps": "8-10 reps", "rest": "120 sec"},
                    {"name": "Bulgarian Split Squats / Lunges", "sets": "3 sets", "reps": "10-12 reps/leg", "rest": "75 sec"},
                    {"name": "Leg Press (Heavy)", "sets": "4 sets", "reps": "10-12 reps", "rest": "90 sec"},
                    {"name": "Romanian Deadlift (Hamstrings)", "sets": "4 sets", "reps": "10-12 reps", "rest": "90 sec"},
                    {"name": "Standing Calf Raises", "sets": "4 sets", "reps": "15-20 reps", "rest": "45 sec"}
                ]
            },
            {
                "day": "Thursday",
                "focus": "Shoulders, Traps & Core",
                "exercises": [
                    {"name": "Overhead Shoulder Press (Form Tracked)", "sets": "4 sets", "reps": "8-10 reps", "rest": "90 sec"},
                    {"name": "Dumbbell Lateral Raises", "sets": "4 sets", "reps": "12-15 reps", "rest": "60 sec"},
                    {"name": "Reverse Pec Deck / Facepulls (Rear Delts)", "sets": "4 sets", "reps": "15 reps", "rest": "60 sec"},
                    {"name": "Dumbbell Shrugs (Traps)", "sets": "4 sets", "reps": "12 reps", "rest": "60 sec"},
                    {"name": "Hanging Leg Raises / Cable Crunch", "sets": "4 sets", "reps": "15 reps", "rest": "45 sec"}
                ]
            },
            {
                "day": "Friday",
                "focus": "Arms Hypertrophy (Biceps & Triceps Super-sets)",
                "exercises": [
                    {"name": "Barbell Preacher Curls", "sets": "4 sets", "reps": "10-12 reps", "rest": "60 sec"},
                    {"name": "Triceps Rope Overhead Extension", "sets": "4 sets", "reps": "12 reps", "rest": "60 sec"},
                    {"name": "Incline Dumbbell Curl", "sets": "3 sets", "reps": "10-12 reps", "rest": "60 sec"},
                    {"name": "Close Grip Bench Press", "sets": "3 sets", "reps": "8-10 reps", "rest": "75 sec"},
                    {"name": "Push-ups Burnout Set", "sets": "2 sets", "reps": "To failure", "rest": "60 sec"}
                ]
            },
            {
                "day": "Saturday",
                "focus": "Legs & Upper Body Pump (Conditioning)",
                "exercises": [
                    {"name": "Walking Lunges (Dumbbell)", "sets": "4 sets", "reps": "12 reps/leg", "rest": "60 sec"},
                    {"name": "Pull-ups / Chin-ups", "sets": "4 sets", "reps": "8-12 reps", "rest": "75 sec"},
                    {"name": "Dumbbell Shoulder Press", "sets": "3 sets", "reps": "10-12 reps", "rest": "60 sec"},
                    {"name": "Plank & Core Circuit", "sets": "3 sets", "reps": "1 min hold", "rest": "45 sec"}
                ]
            },
            {
                "day": "Sunday",
                "focus": "Rest & High-Protein Recovery",
                "exercises": [
                    {"name": "Active recovery walk, hydration, stretch and 8h sleep", "sets": "Full Day", "reps": "Rest", "rest": "--"}
                ]
            }
        ]

    return routine


TRAINER_GOLDEN_RULES = [
    "💧 **Hydration Rule**: Rozana 3 se 4 litre paani zaroor piyein. Muscle dehydration se cramps aate hain aur strength 15% kam ho jaati hai.",
    "🍳 **Protein Timing**: Har meal me 20-30g protein hona chahiye. Workout ke 45 minutes ke andar post-workout meal lena compulsory hai.",
    "🚫 **Avoid Hidden Sugars**: Cold drinks, packaged fruit juices, sweets aur refined flour (maida) se dur rahein.",
    "🏋️‍♂️ **Form Over Weight**: Zyada wazan uthane se pehle form perfect karein. Wrong form se injury hoti hai aur muscle grow nahi hota.",
    "😴 **Sleep & Growth**: Muscle gym me nahi banta, muscle recovery aur neend me banta hai. Roz 7-8 ghante ki proper sleep lein."
]
