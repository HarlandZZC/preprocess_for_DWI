import os
import argparse
import subprocess
from multiprocessing.pool import ThreadPool
import concurrent.futures
# source /data01/software/bashrc && conda activate WMA
# python /home/haolin/Research/Preprocess/WMA.py --folder folder --num_workers 6 --remove N

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--folder', required=True, help='文件夹路径')
parser.add_argument('--num_workers', default=4, type=int, help='Number of threads') 
parser.add_argument('--remove', default='N', choices=['Y', 'N'], help='是否删除多余文件')
args = parser.parse_args()

# 获取文件夹的路径和最大线程数
folder = args.folder
remove_enabled = args.remove == 'Y'
num_workers = args.num_workers

# 获取文件夹中的所有子文件夹
subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]

# 定义处理函数
def process_subfolder(subfolder_path):
    subfolder_name = os.path.basename(subfolder_path)  # 获取子文件夹名称
    print(f"----- White Matter Atlas for {subfolder_name} -----") 
    ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith('ses-') and os.path.isdir(os.path.join(subfolder_path, f))]
    
    for ses_folder in ses_folders:
        tract_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/tractography/')
        tract_files = [f for f in os.listdir(tract_folder) if f.startswith(f'{subfolder_name}_{ses_folder}_run-') and f.endswith('_tractography_OneTsr.vtk')]
        
        for tract_file in tract_files:
            tract_path = os.path.join(tract_folder, tract_file)
            print(tract_path)

            whitematteratlas_output_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/WMA')

            if not os.path.exists(whitematteratlas_output_folder):
                os.makedirs(whitematteratlas_output_folder)

            # 生成命令行
            command = [
                "/data01/software/whitematteranalysis/bin/wm_apply_ORG_atlas_to_subject.sh",
                "-i",
                tract_path,
                "-o",
                whitematteratlas_output_folder,
                "-a",
                "/data01/software/ORG-Atlases",
                "-s",
                "/data01/software/Slicer-5.2.2-linux-amd64/Slicer",
                "-d",
                "1",
                "-m",  
                "/data01/software/Slicer-5.2.2-linux-amd64/Slicer --launch /data01/software/Slicer-5.2.2-linux-amd64/NA-MIC/Extensions-31382/SlicerDMRI/lib/Slicer-5.2/cli-modules/FiberTractMeasurements",
                "-n",
                "8"
            ]

            if remove_enabled:
                command.extend(["-c", "2"])
            
            # 执行命令行
            print(f"Processing {tract_path} ...")
            subprocess.call(command)

# def process_folder(folder):
#     subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
#     with concurrent.futures.ThreadPoolExecutor(max_workers=max_works) as executor:  
#         future_to_subfolder = {executor.submit(process_subfolder, subfolder, folder): subfolder for subfolder in subfolders}
#         for future in concurrent.futures.as_completed(future_to_subfolder):
#             subfolder = future_to_subfolder[future]
#             try:
#                 future.result()
#             except Exception as exc:
#                 print(f"处理 {subfolder} 时发生异常: {exc}")

with ThreadPool(processes=num_workers) as pool:
    subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    pool.map(process_subfolder, subfolders)
