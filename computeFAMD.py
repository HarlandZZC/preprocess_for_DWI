import os
import argparse
import subprocess
from multiprocessing.pool import ThreadPool
# python /home/haolin/Research/Preprocess/computeFAMD.py --folder folder --num_workers 1

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--folder', required=True, help='要处理的文件夹路径')
parser.add_argument('--num_workers', default=4, type=int, help='Number of threads')  
args = parser.parse_args()

# 获取文件夹的路径
folder = args.folder
num_workers = args.num_workers

# 定义处理函数
def process_subfolder(subfolder_path):
    subfolder_name = os.path.basename(subfolder_path)  # 获取子文件夹名称
    print(f"----- compute FAMD for {subfolder_name} -----") 
    ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith('ses-') and os.path.isdir(os.path.join(subfolder_path, f))]

    
    for ses_folder in ses_folders:
        FW_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/matlabFW/')
        sub_FW_folders = [f for f in os.listdir(FW_folder) if f.startswith(f'{subfolder_name}_{ses_folder}_run-')]

        for sub_FW_folder in sub_FW_folders:
            print(sub_FW_folder)
            case_id = sub_FW_folder
            output_path = os.path.join(FW_folder, sub_FW_folder, sub_FW_folder)
            print(output_path)
            FW_nifti_path = os.path.join(FW_folder, sub_FW_folder, f"{case_id}_TensorDTINoNeg.nii.gz")
            
            # 生成命令行
            command = [
                "fslmaths",
                FW_nifti_path,
                "-tensor_decomp",
                output_path
            ]

            # Execute the command
            print(f"Processing {case_id} ...")
            subprocess.call(command)


with ThreadPool(processes=num_workers) as pool:
    subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    pool.map(process_subfolder, subfolders)
  