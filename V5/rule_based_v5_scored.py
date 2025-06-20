import pandas as pd
import numpy as np
import logging

disease_product_mapping = {
    # ===== METABOLIC/ENDOCRINE =====
    "diabetes": {
        "for": ["for_diabetes"],
        "not_for": ["not_for_diabetes"],
        "category": ["category_low carb","category_high fiber"]
    },
    "hyperthyroidism": {
        "for": ["for_hyperthyroidism"],
        "not_for": ["not_for_hyperthyroidism"],
        "category": []

    },
    "hypothyroidism": {
        "for": ["for_metabolic support"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_moderate calorie","category_moderate fat"]
    },
    "cushings_syndrome": {
        "for": ["for_metabolic support","for_weight management"],
        "not_for": ["not_for_hyperlipidemia"],
        "category": ["category_low fat","category_low calorie"]
    },
    "addisons_disease": {
        "for": ["for_metabolic support"],
        "not_for": ["not_for_sodium depletion states","not_for_adrenal disorders"],
        "category": ["category_moderate sodium","category_moderate fat"]
    },
    "hyperlipidemia": {
        "for": ["for_hyperlipidemia"],
        "not_for": ["not_for_hyperlipidemia","not_for_fat intolerant"],
        "category": ["category_low fat"]
    },
    "obesity": {
        "for": ["for_weight management"],
        "not_for": ["not_for_overweight"],
        "category": ["category_low calorie","category_low fat","category_high fiber"]
    },
    "underweight": {
        "for": ["for_appetite stimulation"],
        "not_for": ["not_for_underweight","not_for_catabolic states"],
        "category": ["category_high calorie","category_energy-dense","category_high protein"]
    },

    # ===== GASTROINTESTINAL =====
    "pancreatitis": {
        "for": ["for_pancreatitis"],
        "not_for": ["not_for_pancreatitis", "not_for_fat intolerant"],
        "category": ["category_low fat"]
    },
    "inflammatory_bowel_disease": {
        "for": ["for_gastrointestinal health","for_food sensitivity"],
        "not_for": [],
        "category": ["category_prebiotics"]
    },
    "gastroenteritis": {
        "for": ["for_gastroenteritis"],
        "not_for": ["not_for_dehydration"],
        "category": ["category_digestive care"],
        "custom_dog": ["H_D_P01","H_D_P02","H_D_P03","H_D_P04","H_D_P05","H_D_P06","H_D_P07","H_D_P08","H_D_P09","H_D_P10","H_D_P11",
                       "H_D_P12","H_D_P13","H_D_P14","H_D_P15","H_D_P16","H_D_P17","H_D_P18","H_D_P19","H_D_P20","H_D_P21","H_D_P22",
                       "H_D_P23","H_D_P24","H_D_P25","H_D_P26","H_D_P27","H_D_P28","H_D_P29","H_D_P30","H_D_P31","H_D_P32","H_D_P33",
                       "H_D_P34","H_D_P35","H_D_P36","H_D_P37","H_D_P38","H_D_P39","H_D_P40","H_D_P41","H_D_P42","H_D_P43","H_D_P44",
                       "H_D_P45","H_D_P46","H_D_P47","H_D_P48","H_D_P49","H_D_P50","H_D_P51","H_D_P52","H_D_P53","H_D_P54","H_D_P55",
                       "H_D_P56","H_D_P57","H_D_P58","H_D_P59","H_D_P60","H_D_P61","H_D_P62","H_D_P67","H_D_P68","H_D_P69","H_D_P70",
                       "H_D_P71","H_D_P72","H_D_P73","R_D_P03","R_D_P04","R_D_P05","R_D_P06","R_D_P07","R_D_P08","R_D_P09","R_D_P10",
                       "R_D_P11","R_D_P12","R_D_P13","R_D_P14","R_D_P15","R_D_P16","R_D_P17","R_D_P18","R_D_P19","R_D_P20","R_D_P21",
                       "RC_D_P01","RC_D_P02","RC_D_P03","RC_D_P04","RC_D_P05","RC_D_P06","RC_D_P07","RC_D_P08","RC_D_P09","RC_D_P10",
                       "RC_D_P11","RC_D_P12","RC_D_P13","RC_D_P14","RC_D_P15","RC_D_P16","RC_D_P17","RC_D_P18","RC_D_P19","RC_D_P20",
                       "RC_D_P21","RC_D_P22","RC_D_P23","RC_D_P24","RC_D_P25","RC_D_P26","RC_D_P27","RC_D_P28","RC_D_P29","RC_D_P30",
                       "RC_D_P31","RC_D_P32","RC_D_P33","RC_D_P34","RC_D_P35","RC_D_P36","RC_D_P37","RC_D_P38","P_D_P04","P_D_P05",
                       "P_D_P06","P_D_P07","P_D_P08","P_D_P09","P_D_P10","P_D_P23","P_D_P24","P_D_P25","P_D_P26"],
        "custim_cat": []
    },
    "food_sensitivity": {
        "for": ["for_food sensitivity"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "diarrhea": {
        "for": ["for_diarrhea"],
        "not_for": [],
        "category": ["category_high fiber","category_digestive care"]
    },
    "constipation": {
        "for": ["for_gastrointestinal health"],
        "not_for": [],
        "category": ["category_high fiber"]
    },
    "hairballs": {
        "for": ["for_hairballs"],
        "not_for": [],
        "category": ["category_high fiber","category_digestive care"]
    },
    "protein_losing_enteropathy": {
        "for": ["for_gastrointestinal health"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_high protein"]
    },
    "megaesophagus": {
        "for": ["for_general health"],
        "not_for": [],
        "type": ["Type_Wet"],
        "category": ["category_energy-dense","category_energy-dense"]
    },
    "hepatic_lipidosis": {
        "for": ["for_liver health"],
        "not_for": ["not_for_liver failure"],
        "category": ["category_high protein","category_moderate fat","category_high calorie"]
    },
    "lymphangiectasia": {
        "for": ["for_lymphangiectasia"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_low fat"]
    },
    "hepatitis": {
        "for": ["for_hepatitis","for_liver health"],
        "not_for": ["not_for_liver failure"],
        "category": ["category_moderate fat"]
    },
    "hepatopathy": {
        "for": ["for_hepatitis","for_liver health"],
        "not_for": ["not_for_liver failure","not_for_catabolic states"],
        "category": ["category_low fat","category_digestive care"]
    },
    # ===== RENAL/URINARY =====
    "kidney_disease": {
        "for": ["for_kidney health"],
        "not_for": ["not_for_kidney disease"],
        "category": ["category_low phosphorus","category_low sodium"]
    },
    "feline_luts": {
        "for": ["for_urinary health","for_feline luts"],
        "not_for": ["not_for_struvite","not_for_urinary problems"],
        "category": [],
        "custom_dog": [],
        "custom_cat": []
    },
    "urinary_tract_infection": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_urinary problems"],
        "type": ["Type_Wet"],
        "category": []
    },
    "bladder_stones": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_struvite","not_for_urinary problems"],
        "category": []
    },
    "proteinuria": {
        "for": ["for_proteinuria"],
        "not_for": ["not_for_proteinuria"],
        "category": ["category_low protein","category_low phosphorus"]
    },
    "urinary_problems": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_urinary problems"],
        "type": ["Type_Wet"],
        "category": []
    },
    "struvite": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_struvite"],
        "type": ["Type_Wet"],
        "category": []
    },
    "oxalate_stones": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_struvite","not_for_oxalate stones","Ingredients_spinach","Ingredients_quinoa","Ingredients_soy","Ingredients_beet"],
        "type": ["Type_Wet"],
        "category": ["category_low sodium"]
    },
    # ===== DERMATOLOGICAL =====
    "atopic_dermatitis": {
        "for": ["for_atopic dermatitis","for_skin health"],
        "not_for": [],
        "category": ["category_non-allergenic"],
        "custom_dog" : ["H_D_P13","H_D_P14","H_D_P15","H_D_P16","H_D_P17","H_D_P18","H_D_P19","H_D_P20","H_D_P21","H_D_P22","H_D_P23","H_D_P24","H_D_P25","H_D_P26",
                    "RC_D_P12","RC_D_P13","RC_D_P14","RC_D_P15","RC_D_P25","P_D_P08","P_D_P10","R_D_P16"],
        "custom_cat" : []
    },
    "flea_allergy_dermatitis": {
        "for": ["for_skin health","for_healthy immune system"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "skin_rash": {
        "for": ["for_skin health","for_healthy immune system"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "hot_spots": {
        "for": ["for_skin health"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "ear_infections": {
        "for": ["for_skin health","for_healthy immune system"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "ringworm": {
        "for": ["for_skin health","for_healthy immune system"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    # ===== CARDIAC =====
    "heart_murmur": {
        "for": ["for_heart health"],
        "not_for": ["not_for_cardiac issues","not_for_heart failure"],
        "category": ["category_low sodium","category_high fiber"],
        "has": ["has_Total Omega-3Fatty Acids"]
    },
    "dilated cardiomyopathy": {
        "for": ["for_heart health","for_maintain muscle mass"],
        "not_for": ["not_for_cardiac issues","not_for_heart failure"],
        "category": ["category_low sodium","category_high energy"]
    },
    "hypertrophic_cardiomyopathy": {
        "for": ["for_heart health","for_weight management","for_hydration support"],
        "not_for": ["not_for_cardiac issues","not_for_heart failure"],
        "category": ["category_low sodium","category_high energy"]
    },
    "mitral_valve_disease": {
        "for": ["for_heart health"],
        "not_for": ["not_for_heart failure"],
        "category": ["category_low sodium"]
    },
    "congestive_heart_failure": {
        "for": ["for_heart health"],
        "not_for": ["not_for_heart failure"],
        "category": ["category_low sodium"]
    },
    "hypertension": {#(High Blood Pressure)
        "for": ["for_heart health"],
        "not_for": ["not_for_cardiac issues","not_for_heart failure"],
        "category": ["category_low sodium"]
    },
    # ===== CANCER =====
    "lymphoma": {
        "for": ["for_cancer","for_healthy immune system"],
        "not_for": ["not_for_cancer"],
        "category": ["category_high energy"]
    },
    "mast_cell_tumor": {
        "for": ["for_cancer"],
        "not_for": ["not_for_cancer"],
        "category": ["category_high protein"]
    },
    "osteosarcoma": {
        "for": ["for_cancer"],
        "not_for": ["not_for_cancer"],
        "category": ["category_high calorie"]
    },
    # ===== ORTHOPEDIC =====
    "osteoarthritis": {
        "for": ["for_bone and joint health"],
        "not_for": ["not_for_overweight"],
        "category": ["category_weight management"]
    },
    "hip_dysplasia": {
        "for": ["for_bone and joint health"],
        "not_for": ["not_for_overweight"],
        "category": ["category_weight management"]
    },
    "intervertebral_disc_disease": {
        "for": ["for_bone and joint health"],
        "not_for": ["not_for_overweight"],
        "category": ["category_weight management"]
    },
    "cruciate_ligament_tear": {
        "for": ["for_bone and joint health","for_weight management"],
        "not_for": ["not_for_overweight"],
        "category": ["category_high protein"]
    },
    "arthritis": {
        "for": ["for_bone and joint health","for_weight management"],
        "not_for": ["not_for_overweight"],
        "category": ["category_weight management"],
        "custom_dog": [],
        "custom_cat": ["H_C_P28","H_C_P29","H_C_P30","H_C_P31"]
    },
    # ===== NEUROLOGICAL =====
    "epilepsy": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": []
    },
    "cognitive_dysfunction": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": []
    },
    "vestibular_disease": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": []
    },
    "degenerative_myelopathy": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": []
    },
    "mental_health_disorder": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": ["category_omega3_support"]
    },
    # ===== SPECIES-SPECIFIC =====
    "feline_asthma": {
        "for": ["for_respiratory_support"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "canine_parvovirus": {
        "for": ["for_urgent care"],
        "not_for": ["not_for_debilitation"],
        "category": ["category_recovery"]
    },
    "brachycephalic_syndrome": {
        "for": ["for_general health"],
        "not_for": [],
        "category": ["category_energy-dense"]
    },
    # ===== METABOLIC/ENDOCRINE (ADDITIONS) =====
    "adrenal_disorders": {
        "for": ["for_metabolic support"],
        "not_for": ["not_for_adrenal disorders","not_for_hypertension"],
        "category": []
    },
    "hyperglycemia": {
        "for": ["for_diabetes"],
        "not_for": ["not_for_diabetes"],
        "category": ["category_low carb"]
    },
    # ===== GASTROINTESTINAL (ADDITIONS) =====
    "dehydration": {
        "for": ["for_hydration support"],
        "not_for": ["not_for_dehydration"],
        "type": ["Type_Wet"],
        "category": ["category_low sodium"]
    },
    "gallbladder_disease": {
        "for": ["for_liver health","for_gall bladder diseases"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_low fat"]
    },
    # ===== NEUROLOGICAL (ADDITIONS) =====
    "seizure": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": ["category_controlled_mineral_levels"]
    },
    "anxiety": {
        "for": ["for_calming support","for_anxiety support"],
        "not_for": [],
        "category": ["category_omega3_support"]
    },
    "aging": {
        "for": ["for_aging care"],
        "not_for": [],
        "category": ["category_plant_based","category_natural nutrition","category_weight management"]
    },
    "surgery": {
        "for": ["for_recovery"],
        "not_for": [],
        "category": ["category_high protein"]
    },
    "vision_problem": {
        "for": ["for_vision health"],
        "not_for": [],
        "category": [],
        "custom_dog": [],
        "custim_cat": ["P_C_P25","P_C_P26","P_C_P27","P_C_P28","P_C_P29","P_C_P30","P_C_P31","P_C_P32"]
    },
    "dental_issue": {
        "for": ["for_dental health"],
        "not_for": [],
        "category": []
    },
    "periodontal_disease": {
        "for": ["for_dental health"],
        "not_for": [],
        "category": []
    },
    "inflammatory_mediators": {
        "for": ["for_bone and joint health", "for_skin health"],
        "not_for": [],
        "category": []
    },
    "catabolic states": {
        "for": ["for_maintain muscle mass"],
        "not_for": [],
        "category": ["category_high protein","category_high calorie"]
    },
    "debilitation": {  # (e.g., post-illness weakness)
        "for": ["for_recovery"],
        "not_for": ["not_for_debilitation"],
        "category": ["category_high calorie"]
    },
    "autoimmune diseases": {
        "for":["for_healthy immune system","for_gastrointestinal health"],
         "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "chronic infections": {
        "for":["for_healthy immune system","for_gastrointestinal health"],
         "not_for": [],
        "category": []
    },
    "weak immunity": {
       "for":["for_healthy immune system"],
        "not_for": [],
        "category": ["category_high protein"]
    },
    "cachexia": {
        "for": ["for_maintain muscle mass"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_high protein","category_high calorie"]
    },
    "otitis": {
        "for": ["for_skin health","for_food sensitivity","for_healthy immune system","for_inflammatory mediators"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "portosystemic_shunt": {
        "for": ["for_liver_health","for_metabolic support","for_general health"],
        "not_for": ["not_for_liver failure"],
        "category": ["category_digestive care","category_natural nutrition","category_plant_based"]
    },
    "hypocalcemia": {
        "for": ["for_bone and joint health","for_general health","for_healthy immune system","for_recovery support"],
        "not_for": ["not_for_kidney disease"],
        "category": ["category_multifunction","category_high energy"]
    },
    "hypertrophic_osteodystrophy": {
        "for": ["for_bone and joint health","for_general health"],
        "not_for": [],
        "category": ["category_multifunction","category_moderate calorie","category_moderate fat","category_digestive care"]
    },
    "short_bowel_syndrome": {
        "for": ["for_gastrointestinal health","for_hydration support","for_diarrhea"],
        "not_for": ["not_for_fat intolerant","not_for_liver failure","not_for_dehydration","category_high fiber"],
        "type": ["Type_Wet"],
        "category": [ "category_digestive care","category_energy-dense","category_high calorie"],
        "has": ["has_Magnesium"]
    },
    "interstitial_cystitis": {
        "for": ["for_urinary_health","for_feline luts","for_calming support"],
        "not_for": ["not_for_oxalate stones","not_for_struvite","not_for_truvite urolithiasis"],
        "category": []
    },
    "high_metabolic_needs": {
        "for": ["for_maintain muscle mass"],
        "not_for": ["not_for_overweight"],
        "category": ["category_energy-dense","category_high energy", "category_high protein"]
    }
}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def filter_by_condition(df, column, value):
    """Filter DataFrame where `column` == `value` if column exists and has valid values."""
    if column in df.columns and df[column].any():
        filtered = df[df[column] == value]
        if not filtered.empty:
            logger.debug(f"Filtered by '{column}={value}': {len(filtered)} rows remaining")
            return filtered
    return df

def filter_for_tags(df, disease_info,issue):
    """Combine (union) DataFrames filtered by each 'for' tag individually."""
    if 'for' not in disease_info or not disease_info['for']:
        return df
    for tag in disease_info['for']:
        if tag in df.columns:
            match_mask = df[tag] == 1
            if issue == 'main_issue':
                df.loc[match_mask, 'Score'] += 15
            else: 
                df.loc[match_mask, 'Score'] += 5
    return df
def filter_not_for_tags(df, disease_info,issue):
    """Apply 'not_for' tag filters from disease_info."""
    if 'not_for' in disease_info:
        for tag in disease_info['not_for']:
            match_mask = df[tag] == 0
            if issue == 'main_issue':
                df.loc[match_mask, 'Score'] += 15
            else: 
                df.loc[match_mask, 'Score'] += 5
    return df
def filter_type_tags(df, disease_info,issue):
    """Apply 'type' tag filters from disease_info."""
    if 'type' in disease_info:
        for tag in disease_info['type']:
            match_mask = df[tag] == 1
            if issue == 'main_issue':
                df.loc[match_mask, 'Score'] += 10
            else:
                df.loc[match_mask, 'Score'] += 5
    return df

def filter_category_tags(df, disease_info,issue):
    """Optional: Apply 'category' tag filters from disease_info."""
    if 'category' in disease_info:
        for tag in disease_info['category']:
            if tag in df.columns:
              match_mask = df[tag] == 1
              if issue == 'main_issue':
                df.loc[match_mask, 'Score'] += 15
              else:
                df.loc[match_mask, 'Score'] += 5
    return df
def filter_has_tags(df, disease_info,issue):
    """Optional: Apply 'has' tag filters from disease_info."""
    if 'has' in disease_info:
        for tag in disease_info['has']:
            match_mask = df[tag] == 1
            if issue == 'main_issue':
                df.loc[match_mask, 'Score'] += 15
            else:
                df.loc[match_mask, 'Score'] += 5
    return df

def filter_life_stage(df, life_stage):
    """Filter by life stage (growth/adult/senior)."""
    if life_stage in ['growth', 'adult', 'senior']:
        life_stage_filter = (
            (df[f'life_stage_{life_stage}'] == 1) |
            (df['life_stage_all'] == 1) |
            ((life_stage == 'senior') & (df['life_stage_adult'] == 1))
        )
        if life_stage_filter.any():
            df = df[life_stage_filter]
    return df

def filter_products(df_pet_info, df_products):
    """Main filtering logic for pet products."""
    species_col = f"Species_{df_pet_info.iloc[0]['species']}"
    df_filtered = filter_by_condition(df_products, species_col, 1)


    # Filter by main issue (if any)
    main_issue = df_pet_info.iloc[0]['main_issue'] 
    if main_issue in disease_product_mapping:
        disease_info = disease_product_mapping[main_issue]
        logger.info(f"Filtering for main issue: {main_issue}")
        df_filtered = filter_for_tags(df_filtered, disease_info,'main_issue')
        df_filtered = filter_not_for_tags(df_filtered, disease_info,'main_issue')
        df_filtered = filter_type_tags(df_filtered, disease_info,'main_issue')
        df_filtered = filter_category_tags(df_filtered, disease_info,'main_issue')
        df_filtered = filter_has_tags(df_filtered, disease_info,'main_issue')

        # Check for custom products after main filtering
        species = df_pet_info.iloc[0]['species'].lower()
        custom_key = f"custom_{species}"
        
        if custom_key in disease_info and disease_info[custom_key]:
            custom_products = disease_info[custom_key]
            custom_mask = df_filtered['Product_id'].isin(custom_products)
            df_filtered.loc[custom_mask, 'Score'] += 20

    # Filter by allergies
    if df_pet_info.iloc[0]['allergy'] == 1:
        for ingredient in df_pet_info.iloc[0]['allergic_to']:
            if ingredient == 'unknown':
                filter_by_condition(df_filtered, 'category_non-allergenic', 1)
            else:
                df_filtered = filter_by_condition(df_filtered, f'Ingredients_{ingredient}', 0)

     # Filter by body score
    bds = df_pet_info.iloc[0]['body score (bds)']
    if bds >= 7: # >8 Means Obesity  and >7 Overweight
        df_filtered = filter_by_condition(df_filtered, 'for_weight management', 1)
        df_filtered = filter_by_condition(df_filtered, 'not_for_overweight', 0)
        mask = df_filtered['category_low calorie'] == 1
        df_filtered.loc[mask, 'Score'] += 5

    elif bds <= 3: # Means Underweight
        df_filtered = filter_by_condition(df_filtered, 'for_weight management', 0)
        mask = df_filtered['for_appetite stimulation'] == 1
        df_filtered.loc[mask, 'Score'] += 10
        mask = df_filtered['not_for_overweight'] == 0
        df_filtered.loc[mask, 'Score'] += 10
        mask = df_filtered['not_for_catabolic states'] == 0
        df_filtered.loc[mask, 'Score'] += 5
        mask = df_filtered['category_high calorie'] == 1
        df_filtered.loc[mask, 'Score'] += 10
        mask = df_filtered['category_high protein'] == 1
        df_filtered.loc[mask, 'Score'] += 5


    # Filter by pregnancy/lactation
    if df_pet_info.iloc[0]['pregnant']:
        life_stage = 'growth'
        df_filtered = filter_by_condition(df_filtered, 'not_for_pregnancy', 0)

    if df_pet_info.iloc[0]['lactating']:
        life_stage = 'growth'
        df_filtered = filter_by_condition(df_filtered, 'not_for_lactation', 0)

    # Filter by life stage
    if not (df_pet_info.iloc[0]['pregnant'] or df_pet_info.iloc[0]['lactating']):
       life_stage = df_pet_info.iloc[0]['life_stage']
    df_filtered = filter_life_stage(df_filtered, life_stage)

    # Filter by other issues
    if df_pet_info.iloc[0]['other_issues'] == 1:
        for issue in df_pet_info.iloc[0]['other_issues_list']:
            if issue in disease_product_mapping:
                disease_info = disease_product_mapping[issue]
                df_filtered = filter_for_tags(df_filtered, disease_info,'other_issues')
                df_filtered = filter_not_for_tags(df_filtered, disease_info,'other_issues')
                df_filtered = filter_type_tags(df_filtered, disease_info,'other_issues')
                df_filtered = filter_category_tags(df_filtered, disease_info,'other_issues')
                df_filtered = filter_has_tags(df_filtered, disease_info,'other_issues')

    # Filter by breed size and activity level
    mask = df_filtered[f'breed_size_{df_pet_info.iloc[0]["breed_size"]}'] == 1
    df_filtered.loc[mask, 'Score'] += 5

    # if df_pet_info['activity level'] == 'Active':
    activity_level = df_pet_info.iloc[0]['activity level']
    if activity_level == 'active':
        mask = df_filtered['not_for_active pets'] == 0
        df_filtered.loc[mask, 'Score'] += 10

        mask = df_filtered['category_high calorie'] == 1
        df_filtered.loc[mask, 'Score'] += 5

        mask = df_filtered['category_energy-dense'] == 1
        df_filtered.loc[mask, 'Score'] += 5

    # Get sorted products with scores
    sorted_df = df_filtered.sort_values('Score', ascending=False)

    # Return both IDs and scores (as list of tuples)
    scored_products = list(zip(sorted_df['Product_id'], sorted_df['Score']))

    return scored_products, len(scored_products)
