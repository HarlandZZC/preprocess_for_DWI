import os
import argparse
# python /home/haolin/Research/Preprocess/check_subfolders_after_BrainMask.py --folder folder

def check_subfolders(folder_path):
    # 获取文件夹下的所有子文件夹列表
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith("ses-") and os.path.isdir(os.path.join(subfolder_path, f))]
        
        for ses_folder in ses_folders:
            ses_folder_path = os.path.join(subfolder_path, ses_folder)
            dwi_folder = os.path.join(ses_folder_path, "dwi", "corrected_masked")

            # 检查必需文件是否存在
            required_files_groups = [
                [
                    "{}_{}_run-{}_dwi_QCed.bval".format(subfolder, ses_folder, run),
                    "{}_{}_run-{}_dwi_QCed.bvec".format(subfolder, ses_folder, run),
                    "{}_{}_run-{}_dwi_QCed_bse.nii.gz".format(subfolder, ses_folder, run),
                    "{}_{}_run-{}_dwi_QCed_bse-multi_BrainMask.nii.gz".format(subfolder, ses_folder, run)
                ]
                for run in range(1, 201)  # 由于范围是不包含结束值的，这将检查从运行1到运行200的文件。
            ]

            for required_files in required_files_groups:
                if all(os.path.exists(os.path.join(dwi_folder, f)) for f in required_files):
                    print("子文件夹 {} 的 {} 包含必需的文件.".format(subfolder, ses_folder))
                    break
                else:
                    print("子文件夹 {} 的 {} 缺少以下必需的文件:".format(subfolder, ses_folder))
                    for required_files in required_files_groups:
                        missing_files = [f for f in required_files if not os.path.exists(os.path.join(dwi_folder, f))]
                        if missing_files:
                            for file in missing_files:
                                print(file)
                            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="文件夹的路径")
    args = parser.parse_args()

    folder_path = args.folder
    check_subfolders(folder_path)
