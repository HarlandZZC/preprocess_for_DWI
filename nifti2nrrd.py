import os
import argparse
import subprocess
# conda activate motion_correct
# python /home/haolin/Research/Preprocess/nifti2nrrd.py --folder folder

def convert_to_nrrd(nifti_file, bval_file, bvec_file):
    slicer_path = "/data01/software/Slicer-5.2.2-linux-amd64/Slicer"
    slicer_cli_module = "/data01/software/Slicer-5.2.2-linux-amd64/lib/Slicer-5.2/cli-modules/DWIConvert"
    output_volume = nifti_file[:-len(".nii.gz")] + ".nrrd"

    command = [
        slicer_path,
        "--launch", slicer_cli_module,
        "--conversionMode", "FSLToNrrd",
        "--transposeInputBVectors",
        "--outputVolume", output_volume,
        "--smallGradientThreshold", "0.2",
        "--inputBValues", bval_file,
        "--inputBVectors", bvec_file,
        "--fslNIFTIFile", nifti_file,
        "--allowLossyConversion"
    ]

    subprocess.run(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Path to the folder")
    args = parser.parse_args()

    folder_path = args.folder

    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith("ses-") and os.path.isdir(os.path.join(subfolder_path, f))]

        for ses_folder in ses_folders:
            dwi_folder = os.path.join(subfolder_path, ses_folder, "dwi")
            dwi_files = [f for f in os.listdir(dwi_folder) if f.endswith(".nii.gz")]

            for dwi_file in dwi_files:
                input_file = os.path.join(dwi_folder, dwi_file)
                bval_file = os.path.join(dwi_folder, f"{dwi_file[:-len('.nii.gz')]}.bval")
                bvec_file = os.path.join(dwi_folder, f"{dwi_file[:-len('.nii.gz')]}.bvec")

                convert_to_nrrd(input_file, bval_file, bvec_file)
