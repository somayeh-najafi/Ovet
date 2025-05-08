import streamlit as st
import pandas as pd
from rule_based_v3_streamlit import disease_product_mapping, filter_products, filter_by_condition, filter_for_tags, filter_not_for_tags, filter_type_tags, filter_category_tags, filter_has_tags, filter_life_stage

# Load product data
df_products = pd.read_csv("encoded_all_products.csv")
#df_productdata = pd.read_csv("Products_final_cleaned.csv")


# ------------------ Hardcoded Lists ------------------

dog_breeds = sorted([
    "Beagle", "Boxer", "Bulldog", "Dachshund", "German Shepherd",
    "Golden Retriever", "Labrador Retriever", "Poodle", "Shih Tzu", "Yorkshire Terrier",
	"Bullmastiff", "English spaniel", "Husky", "Doberman", "English bulldog",
	"Shiba Inu", "Australian shepherd", "Pinscher"
])

cat_breeds = sorted([
    "Domestic Shorthair", "American Shorthair", "Domestic Longhair", "Ragdoll",
    "Siamese", "Bengal", "Maine Coon", "British Shorthair", "Persian", "Russian Blue",
    "Sphynx", "Scottish Fold", "Exotic Shorthair", "Oriental Shorthair", "Burmese",
    "Devon Rex", "Himalayan", "Abyssinian", "Birman", "Norwegian Forest Cat"
])

health_conditions = sorted([
	"addisons_disease", "adrenal_disorders", "aging", "anxiety", "arthritis", "atopic_dermatitis",
	"autoimmune diseases", "brachycephalic_syndrome", "bladder_stones", "cancer", "canine_parvovirus",
	"catabolic states", "cachexia", "chronic infections", "cognitive_dysfunction", "congestive_heart_failure",
	"constipation", "cruciate_ligament_tear", "cushings_syndrome", "debilitation", "dehydration", "degenerative_myelopathy",
	"dental_issue", "diabetes", "diarrhea", "dilated cardiomyopathy", "epilepsy", "ear_infections",
	"feline_asthma", "feline_luts", "flea_allergy_dermatitis", "food_sensitivity", "gallbladder_disease", "gastroenteritis",
	"hairballs", "heart_murmur", "hepatic_lipidosis", "hepatitis", "hepatopathy", "high_metabolic_needs",
	"hip_dysplasia", "hot_spots", "hyperglycemia", "hyperlipidemia", "hyperthyroidism", "hypertension",
	"hypocalcemia", "hypothyroidism", "inflammatory_bowel_disease", "inflammatory_mediators", "intervertebral_disc_disease",
	"interstitial_cystitis", "kidney_disease", "lymphangiectasia", "lymphoma", "mast_cell_tumor", "megaesophagus", "mental_health_disorder",
	"metabolic/endocrine", "mitral_valve_disease", "obesity", "osteoarthritis", "osteosarcoma", "otitis", "oxalate_stones", "pancreatitis",
	"periodontal_disease", "portosystemic_shunt", "protein_losing_enteropathy", "proteinuria", "ringworm", "seizure",
	"short_bowel_syndrome", "skin_rash", "struvite", "surgery", "urinary_problems", "urinary_tract_infection", "vestibular_disease",
	"vision_problem", "weak immunity", "underweight", "hypertrophic_cardiomyopathy", "hypertrophic_osteodystrophy"
])

allergy_list = sorted([
    "unknown", "Barley", "Beef", "Carrot", "Chicken", "Corn", "Dairy", "Duck", "Egg", "Fish", "Flaxseed",
    "Lamb", "Oat", "Pea", "Pork", "Potato", "Pumpkin", "Rice", "Salmon", "Soy", "Sweet Potato",
    "Tomato", "Turkey", "Wheat", "Brown Rice", "Coconut", "Chickpea", "Fava Beans", "Quinoa", "Sorghum", "Tapioca",
    "Black Beans", "Broccoli", "Algae", "Millet", "Venison", "Kangaroo", "Duck Liver", "Liver",
    "Rabbit", "Spinach", "Milk"
])

activity_levels = ["Active", "Not Active"]
life_stages = ["Growth", "Adult", "Senior"]


# Set up page config
st.set_page_config(page_title="Pet Nutrition Recommender", layout="centered")
st.title("🐾🐶Pet Food Recommendation Tool - Rule-Based Recommendations🐱🐾")



# Initialize session state for form persistence
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Gender selector
has_gender = st.radio("Gender", options=["Male", "Female"], index=None, key='gender')

# Species dropdown
species = st.selectbox("Species", ["-- Select species --", "Dog", "Cat"], key='species')

# Breed selection
breed_list = []
breed_name = "-- Select a breed --"

if species == "Dog":
    breed_list = dog_breeds
elif species == "Cat":
    breed_list = cat_breeds

if breed_list:
    breed_name = st.selectbox("Breed Name", ["-- Select a breed --"] + breed_list, key='breed')

# Allergy selector
has_allergy = st.radio("Allergies", options=["Yes", "No"], index=None, key='allergy')

selected_allergies = []
if has_allergy == "Yes":
    selected_allergies = st.multiselect(
        "Allergies", 
        allergy_list, 
        placeholder="Choose an option",
        key='allergies'
    )

# Female-specific options
has_lactation = False
has_pregnant = False

if has_gender == "Female":
    has_lactation = st.radio(
        "Lactating", 
        options=[True, False], 
        index=None, 
        format_func=lambda x: "Yes" if x else "No",
        key='lactating'
    )
    has_pregnant = st.radio(
        "Pregnant", 
        options=[True, False], 
        index=None, 
        format_func=lambda x: "Yes" if x else "No",
        key='pregnant'
    )

# Main form
with st.form("pet_form"):
    breed_size = st.selectbox(
        "Breed Size", 
        ["-- Select breed size --", "Small", "Medium", "Large"],
        key='breed_size'
    )
    life_stage = st.selectbox(
        "Life Stage", 
        ["-- Select life stage --"] + life_stages,
        key='life_stage'
    )
    activity_level = st.selectbox(
        "Activity Level", 
        ["-- Select activity level --"] + activity_levels,
        key='activity_level'
    )

    weight = st.number_input(
        "Weight (kg)", 
        min_value=0.0, 
        step=0.1, 
        value=0.0,
        key='weight'
    )
    age = st.number_input(
        "Age (months)", 
        min_value=0, 
        step=1, 
        value=0,
        key='age'
    )
    body_score = st.slider(
        "Body Score (1-9)", 
        min_value=1, 
        max_value=9, 
        step=1,
        key='body_score'
    )

    # Health issues
    main_issue = st.selectbox(
        "Main Health Issue", 
        ["-- Select main issue --"] + health_conditions,
        key='main_issue'
    )


    other_issues = st.multiselect(
        "Other Health Issues (up to 2)", 
        health_conditions,
        placeholder="Choose up to two issues",
        max_selections=2
       
    )
   
    submitted = st.form_submit_button("Get Recommendations")

# Process form submission
if submitted:
    errors = []
    
    # Validate required fields
    validation_checks = {
        "species": species == "-- Select species --",
       # "breed": breed_name == "-- Select a breed --",
        "breed_size": breed_size == "-- Select breed size --",
        "life_stage": life_stage == "-- Select life stage --",
        "activity_level": activity_level == "-- Select activity level --",
        "allergy": has_allergy is None,
        #"main_issue": main_issue == "-- Select main issue --",
        "gender": has_gender is None
    }

    for field, is_invalid in validation_checks.items():
        if is_invalid:
            errors.append(f"Please select {field.replace('_', ' ')}.")

    if weight <= 0:
        errors.append("Weight must be greater than 0")
    if age <= 0:
        errors.append("Age must be greater than 0")

    if errors:
        for error in errors:
            st.error(error)
    else:
        # Process other_issues to match your manual script format
        has_other_issues = 1 if other_issues else 0
        other_issues_list = [issue.strip().lower() for issue in other_issues] if other_issues else []


        # Create pet info DataFrame
        pet_info = {
            "species": species,
            "life_stage": life_stage.lower(),
            "weight": float(weight),
            "age (months)": int(age),
            "activity level": activity_level.lower(),
            "main_issue": main_issue.lower(),
            "other_issues": has_other_issues,
            "other_issues_list": other_issues_list, 
            "gender": has_gender.lower(),
            "breed": breed_name,
            "breed_size": breed_size.lower(),
            "body score (bds)": float(body_score),
            "pregnant": bool(has_pregnant) if has_gender == "Female" else False,
            "lactating": bool(has_lactation) if has_gender == "Female" else False,
            "allergy": int(has_allergy == "Yes"),
            "allergic_to": [a.lower() for a in selected_allergies] if selected_allergies else []
        }

        df_pet_info = pd.DataFrame([pet_info])
        
        # Save to session state
        st.session_state.form_data = pet_info
        
        # Display processed data (for debugging)
        st.write("### Pet Information Summary")
        st.json(pet_info)
        # Here we would call recommendation function
        product_ids, count = filter_products(df_pet_info, df_products)
        recommended_products = df_products[df_products['Product_id'].isin(product_ids)]
                
        # Display would look like:
        st.write("## Recommended Products:")
        st.write("#### No. of Recommended Products:",count)
        for _, row in recommended_products.iterrows():
           st.write(f"- {row['Product_Name']} (ID: {row['Product_id']})")