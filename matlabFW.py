import os
import argparse
import subprocess
from multiprocessing.pool import ThreadPool
# python /home/haolin/Research/Preprocess/matlabFW.py --folder folder --num_workers 1

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
    print(f"----- matlab FW for {subfolder_name} -----") 
    ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith('ses-') and os.path.isdir(os.path.join(subfolder_path, f))]

    
    for ses_folder in ses_folders:
        dwi_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/corrected_masked/')
        dwi_files = [f for f in os.listdir(dwi_folder) if f.startswith(f'{subfolder_name}_{ses_folder}_run-') and f.endswith('_dwi_QCed.nhdr')]
        

        for dwi_file in dwi_files:
            run_id = dwi_file.split('_run-')[1].split('_dwi_QCed.nhdr')[0]
            case_id = f"{subfolder_name}_{ses_folder}_run-{run_id}"
            dwi_nhdr_path = os.path.join(dwi_folder, dwi_file)
            dwi_nifti_path = os.path.join(dwi_folder, f"{subfolder_name}_{ses_folder}_run-{run_id}_dwi_QCed.nii.gz")
            bval_path = os.path.join(dwi_folder, f"{subfolder_name}_{ses_folder}_run-{run_id}_dwi_QCed.bval")
            bvec_path = os.path.join(dwi_folder, f"{subfolder_name}_{ses_folder}_run-{run_id}_dwi_QCed.bvec")
            mask_nhdr_path = os.path.join(dwi_folder, f"{subfolder_name}_{ses_folder}_run-{run_id}_dwi_QCed_bse-multi_BrainMask.nhdr")
            mask_nifti_path = os.path.join(dwi_folder, f"{subfolder_name}_{ses_folder}_run-{run_id}_dwi_QCed_bse-multi_BrainMask.nii.gz")
            output_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/matlabFW/{subfolder_name}_{ses_folder}_run-{run_id}')
            log_path = os.path.join(subfolder_path, f'{ses_folder}/dwi/matlabFW/{subfolder_name}_{ses_folder}_run-{run_id}/{subfolder_name}_{ses_folder}_run-{run_id}.log')

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # 生成命令行
            command = [
                "/data01/software/MATLAB/R2022b/bin/matlab",
                "-nodisplay", "-nosplash", "-nodesktop",
                "-logfile", log_path,
                "-r", f"addpath('/home/haolin/Research/Preprocess/FreeWater/'); addpath('/home/haolin/Research/Preprocess/FreeWater/lib'); addpath('/home/haolin/Research/Preprocess/FreeWater/lib/IO'); FreeWater_OneCase('{case_id}', '{dwi_nifti_path}', '{bval_path}', '{bvec_path}', '{mask_nifti_path}', '{output_folder}'); exit"  
            ]

            # Execute the command
            print(f"Processing {case_id} ...")
            subprocess.call(command)


with ThreadPool(processes=num_workers) as pool:
    subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    pool.map(process_subfolder, subfolders)
  