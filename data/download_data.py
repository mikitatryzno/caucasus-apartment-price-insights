import os
import zipfile
import kaggle
import shutil
from pathlib import Path
import pandas as pd

def setup_kaggle_credentials():
    """Set up Kaggle API credentials if not already configured."""
    # Check if kaggle.json exists in the default location
    kaggle_dir = os.path.join(os.path.expanduser('~'), '.kaggle')
    kaggle_json = os.path.join(kaggle_dir, 'kaggle.json')
    
    if not os.path.exists(kaggle_json):
        print("Kaggle API credentials not found.")
        print("Please place your kaggle.json file in the ~/.kaggle/ directory")
        print("or enter your credentials below:")
        
        username = input("Kaggle username: ")
        key = input("Kaggle API key: ")
        
        # Create the .kaggle directory if it doesn't exist
        os.makedirs(kaggle_dir, exist_ok=True)
        
        # Create the kaggle.json file
        with open(kaggle_json, 'w') as f:
            f.write(f'{{"username":"{username}","key":"{key}"}}')
        
        # Set permissions on the file (required on Unix systems)
        try:
            os.chmod(kaggle_json, 0o600)
        except Exception as e:
            print(f"Warning: Could not set permissions on kaggle.json: {e}")
    
    print("Kaggle API credentials configured.")

def download_and_process_dataset(dataset_info, output_dir):
    """Download a dataset from Kaggle and process according to requirements."""
    dataset_name = dataset_info["name"]
    output_filename = dataset_info["output_filename"]
    source_file = dataset_info.get("source_file")
    
    print(f"Processing {dataset_name}...")
    
    try:
        # Create a temporary directory for downloads
        temp_dir = os.path.join(output_dir, "temp_" + dataset_name.split('/')[-1])
        os.makedirs(temp_dir, exist_ok=True)
        
        # Download the dataset
        print(f"Downloading {dataset_name}...")
        kaggle.api.dataset_download_files(
            dataset_name,
            path=temp_dir,
            unzip=True
        )
        
        # Find the CSV files in the temp directory
        csv_files = list(Path(temp_dir).glob('**/*.csv'))
        
        if not csv_files:
            print(f"Error: No CSV files found for {dataset_name}")
            return False
        
        # If a specific source file is specified, find it
        if source_file:
            matching_files = [f for f in csv_files if f.name == source_file]
            if matching_files:
                source_path = matching_files[0]
            else:
                print(f"Warning: Specified file '{source_file}' not found.")
                print(f"Available CSV files: {[f.name for f in csv_files]}")
                # Use the first CSV as fallback
                source_path = csv_files[0]
        else:
            # Use the first CSV file found
            source_path = csv_files[0]
        
        # Read the data
        print(f"Reading data from {source_path}...")
        df = pd.read_csv(source_path)
        
        # Save with the new filename
        output_path = os.path.join(output_dir, output_filename)
        df.to_csv(output_path, index=False)
        print(f"Saved data to {output_path}")
        
        # Clean up the temp directory
        shutil.rmtree(temp_dir)
        return True
        
    except Exception as e:
        print(f"Error processing {dataset_name}: {e}")
        return False

def main():
    # Define the datasets to download
    datasets = [
        {
            "name": "mirzoyanvahe/armenian-real-estate-market-data",
            "source_file": "cleaned_apartment_data.csv",
            "output_filename": "yerevan_apartment_data.csv"
        },
        {
            "name": "beridzeg45/apartment-prices",
            "source_file": None,  # Will use the first CSV found
            "output_filename": "tbilisi_apartment_data.csv"
        },
        {
            "name": "azadshahvaladov/apartment-prices-for-azerbaijan-market",
            "source_file": None,  # Will use the first CSV found
            "output_filename": "baku_apartment_data.csv"
        }
    ]
    
    # Create a directory for the downloads
    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = current_dir
    os.makedirs(download_dir, exist_ok=True)
    
    # Set up Kaggle credentials
    setup_kaggle_credentials()
    
    # Download and process each dataset
    successful_downloads = 0
    for dataset_info in datasets:
        if download_and_process_dataset(dataset_info, download_dir):
            successful_downloads += 1
    
    # Print summary
    print(f"\nDownloaded {successful_downloads} out of {len(datasets)} datasets.")
    
    if successful_downloads == len(datasets):
        print("\nAll datasets downloaded successfully!")
    else:
        print("\nSome datasets could not be downloaded. Please check the errors above.")
    
    print(f"Data is located in: {download_dir}")

if __name__ == "__main__":
    main()