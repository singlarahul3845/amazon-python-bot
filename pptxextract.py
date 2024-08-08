import zipfile
import os
import shutil

def extract_first_pptx(zip_paths, destination_folder):
    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    def extract_from_zip(zip_path):
        # Path for the temporary directory used to store nested zips
        temp_dir = os.path.join(destination_folder, 'temp_zip')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        def recurse_zip(file_path):
            # Open the zip file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for entry in zip_ref.namelist():
                    # Ignore directories
                    if entry.endswith('/'):
                        continue

                    # Check if the entry is a zip file itself
                    if entry.lower().endswith('.zip'):
                        # Extract to the temporary folder
                        nested_zip_path = os.path.join(temp_dir, entry)
                        zip_ref.extract(entry, temp_dir)

                        # Recursively check the nested zip
                        if recurse_zip(nested_zip_path):
                            return True

                    # Check if the entry is a .pptx file
                    elif entry.lower().endswith('.pptx'):
                        # Extract the .pptx file
                        zip_ref.extract(entry, destination_folder)
                        print(f"Extracted {entry} to {destination_folder}")
                        return True

            return False

        # Start the recursion from the initial zip path
        result = recurse_zip(zip_path)

        # Cleanup: Remove the temporary directory after processing is complete
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)  # Remove the directory and all its contents

        if not result:
            print(f"No .pptx file found in zip file: {zip_path}")
            return False

        return True

    # Iterate over each zip path and extract the first .pptx found
    for zip_path in zip_paths:
        print(f"Processing {zip_path}...")
        extract_from_zip(zip_path)

# Usage
zip_file_paths = [
  r"C:\Users\Rahul Singla\Downloads\devops_practices_for_hybrid_environment_it_powerpoint_presentation_slides.zip",
  r"C:\Users\Rahul Singla\Downloads\devops_best_practices_powerpoint_ppt_template_bundles.zip",
  r"C:\Users\Rahul Singla\Downloads\industrial_waste_management_powerpoint_ppt_template_bundles.zip",
  r"C:\Users\Rahul Singla\Downloads\industrial_waste_powerpoint_ppt_template_bundles.zip",
  r"C:\Users\Rahul Singla\Downloads\industrial_waste_management_powerpoint_presentation_slides (1).zip",
  r"C:\Users\Rahul Singla\Downloads\context_awareness_powerpoint_ppt_template_bundles_crp.zip",
  r"C:\Users\Rahul Singla\Downloads\project_context_for_consulting_proposal_to_improve_brand_awareness_ppt_icon_display.zip",
  r"C:\Users\Rahul Singla\Downloads\project_context_of_business_reputation_building_and_awareness_one_pager_sample_example_document.zip",
  r"C:\Users\Rahul Singla\Downloads\project_context_for_awareness_campaign_proposal_one_pager_sample_example_document.zip",
  r"C:\Users\Rahul Singla\Downloads\new_hair_and_beauty_salon_marketing_plan_to_enhance_customer_experience_and_sales_strategy_cd.zip",
]
destination_folder = r'C:\Users\Rahul Singla\OneDrive\Desktop\alpha brain\destination_folder'
extract_first_pptx(zip_file_paths, destination_folder)
