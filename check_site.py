import os
import csv
import argparse
# python /home/haolin/Research/Preprocess/check_site.py --folder folder

def check_sub_id_and_folders(site_folder):
    csv_files = [f for f in os.listdir(site_folder) if f.endswith('fine.csv')]

    if not csv_files:
        print("Error: fine.csv file not found in SITE folder.")
        return

    csv_path = os.path.join(site_folder, csv_files[0])

    sub_folders = [f for f in os.listdir(site_folder) if os.path.isdir(os.path.join(site_folder, f)) and f.startswith('sub-')]
    sub_ids = set()

    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            sub_id = row.get('SUB_ID')
            if sub_id:
                sub_ids.add(sub_id)

    missing_sub_folders = sub_ids.difference(set([sub_folder.split('-')[1] for sub_folder in sub_folders]))
    missing_sub_ids = set([f'sub-{sub_id}' for sub_id in sub_ids]).difference(sub_folders)

    if missing_sub_folders:
        print("Error: The following SUB_IDs are missing corresponding sub-folders:")
        print(', '.join(missing_sub_folders))

    if missing_sub_ids:
        print("Error: The following sub-folders do not have corresponding SUB_IDs:")
        print(', '.join(missing_sub_ids))

    if not missing_sub_folders and not missing_sub_ids:
        print("All SUB_IDs in fine.csv have corresponding sub-folders, and vice versa.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if SUB_IDs in fine.csv correspond to one-level sub-folders in the SITE folder.")
    parser.add_argument("--folder", required=True, help="Path to the SITE folder.")
    args = parser.parse_args()

    check_sub_id_and_folders(args.folder)
