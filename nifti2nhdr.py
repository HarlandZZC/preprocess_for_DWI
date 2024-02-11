import os
import argparse
import subprocess
# conda activate dmri_seg
# python /home/haolin/Research/Preprocess/nifti2nhdr.py --folder folder

def convert_to_nhdr(nifti_file, nhdr_file, bval_file=None, bvec_file=None):
    command = ["python", "/data01/software/conversion/conversion/nhdr_write.py", "--nifti", nifti_file, "--nhdr", nhdr_file]

    # 添加 bval 和 bvec 参数（如果提供）
    if bval_file is not None and bvec_file is not None:
        command += ["--bval", bval_file, "--bvec", bvec_file]

    subprocess.run(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="文件夹的路径")
    args = parser.parse_args()

    folder_path = args.folder

    # 获取文件夹中的所有子文件夹列表
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith("ses-") and os.path.isdir(os.path.join(subfolder_path, f))]
        
        for ses_folder in ses_folders:
            dwi_folder = os.path.join(subfolder_path, ses_folder, "dwi", "corrected_masked")

            # 获取dwi文件列表
            dwi_files = [f for f in os.listdir(dwi_folder) if f.endswith("_QCed.nii.gz") or f.endswith("_QCed_bse.nii.gz") or f.endswith("_QCed_bse-multi_BrainMask.nii.gz")]

            for dwi_file in dwi_files:
                input_file = os.path.join(dwi_folder, dwi_file)
                output_file = os.path.join(dwi_folder, dwi_file[:-len(".nii.gz")] + ".nhdr")  # 转换后的文件名为 .nhdr 格式

                # 构建对应的bval和bvec文件名
                bval_file = os.path.join(dwi_folder, f"{dwi_file[:-len('.nii.gz')]}.bval")
                bvec_file = os.path.join(dwi_folder, f"{dwi_file[:-len('.nii.gz')]}.bvec")

                if dwi_file.endswith("_QCed_bse.nii.gz") or dwi_file.endswith("_QCed_bse-multi_BrainMask.nii.gz"):
                    convert_to_nhdr(input_file, output_file)
                else:
                    convert_to_nhdr(input_file, output_file, bval_file, bvec_file)
