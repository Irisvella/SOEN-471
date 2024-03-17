from faker import Faker
import pandas as pd
import numpy as np
import random

# Can upadte to include more locales if needed
locales = ['en_US']
fake = Faker(locales)

restricted_zip_codes = [
    "036", "692", "878", "059", "790", "879",
    "063", "821", "884", "102", "823", "890",
    "203", "830", "893", "556", "831"
]

# Helper function
def generate_personal_info(info_type):
    if info_type == 'name':
        return fake.name()
    elif info_type == 'email':
        return fake.email()
    elif info_type == 'phone_number':
        return fake.phone_number()
    # Extend with more types if needed

# Function to insert a mistake into a field
def insert_mistake(field):
    mistake_types = ['name', 'email', 'phone_number']  # Extendable list
    mistake_type = random.choice(mistake_types)
    mistake_content = generate_personal_info(mistake_type)

    if random.choice([True, False]):  # 50% chance to append or prepend the mistake
        return f"{mistake_content} {field}"
    else:
        return f"{field} {mistake_content}"

# Function to check and update records for restricted ZIP codes
def check_for_restricted_zip(record):
    for zip_code in restricted_zip_codes:
        if zip_code in record["Location"]:
            record["Contains Personal Information"] = "Yes"
            break

# Generate the data
def generate_corrected_dataset(num_records):
    data = []

    for _ in range(num_records):
        record = {
            "Barcode": fake.bothify(text="???###"),
            "PatientID": fake.unique.uuid4(),
            "Ethnicity": fake.random_element(elements=("Asian", "Caucasian", "African American", "Hispanic", "Arabic", "Other")),
            "Age": str(fake.random_int(min=0, max=100)),
            "SerumTumorMarkers": f"Total PSA (ng/mL): {np.random.normal(loc=1.84, scale=2.01, size=1).round(2)}",
            "MRIDate": fake.date(),
            "TumorMarkersResults": fake.random_element(elements=("Low", "Moderate", "High")),
            "Conclusion": fake.sentence(),
            "ClinicallySignificant": fake.random_element(elements=("Yes", "No")),
            "PiRAD": fake.random_element(elements=("1", "2", "3", "4", "5")),
            "Location": fake.city(),
            "Contains Personal Information": "No"
        }
        
        # Simulate the chance of identifiable information slipping into any attribute
        if fake.boolean(chance_of_getting_true=20):
            chosen_field = random.choice(["TumorMarkersResults", "Conclusion"])
            record[chosen_field] = insert_mistake(record[chosen_field])
            record["Contains Personal Information"] = "Yes"

        # Check for restricted ZIP codes
        check_for_restricted_zip(record)

        data.append(record)
    return pd.DataFrame(data)

corrected_df = generate_corrected_dataset(100)
print(corrected_df.head())
