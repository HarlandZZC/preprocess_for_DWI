import os
import argparse
import subprocess
# python /home/haolin/Research/Preprocess/tractography.py --folder folder --numThread 64 --freewater N

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--folder', required=True, help='文件夹路径')
parser.add_argument('--numThread', required=True, help='线程数量')
parser.add_argument('--freewater', default='N', choices=['Y', 'N'], help='是否启用 freeWater 参数 (Y/N)')
args = parser.parse_args()

# 获取文件夹的路径
folder = args.folder

# 获取是否启用 freeWater 参数
freewater_enabled = args.freewater == 'Y'

num_Thread = args.numThread

# 获取文件夹中的所有子文件夹
subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]

# 定义处理函数
def process_subfolder(subfolder_path, folder_path):
    subfolder_name = os.path.basename(subfolder_path)  # 获取子文件夹名称
    folder_name = os.path.basename(folder_path)
    print(f"----- Tractography for {subfolder_name} -----") 
    ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith('ses-') and os.path.isdir(os.path.join(subfolder_path, f))]
    
    for ses_folder in ses_folders:
        dwi_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/corrected_masked/')
        dwi_files = [f for f in os.listdir(dwi_folder) if f.startswith(f'{subfolder_name}_{ses_folder}_run-') and f.endswith('_dwi_QCed.nhdr')]
        
        for dwi_file in dwi_files:
            dwi_path = os.path.join(dwi_folder, dwi_file)
            run_id = dwi_file.split('_run-')[1].split('_dwi_QCed.nhdr')[0]

            tractography_output_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/tractography')
            print("Target folder path:", tractography_output_folder)

            if not os.path.exists(tractography_output_folder):
                os.makedirs(tractography_output_folder)

            tractography_output_path = os.path.join(subfolder_path, f'{ses_folder}/dwi/tractography',f"{subfolder_name}_{ses_folder}_run-{run_id}_tractography.vtk")
            
            # 生成命令行
            command = [
                "/data01/software/Slicer-5.2.2-linux-amd64/Slicer",
                "--launch",
                "/data01/software/Slicer-5.2.2-linux-amd64/NA-MIC/Extensions-31382/UKFTractography/lib/Slicer-5.2/cli-modules/UKFTractography",
                "--numThreads",
                f"{num_Thread}",
                "--numTensor",
                "2",
                "--dwiFile",
                dwi_path,
                "--maskFile",
                os.path.join(dwi_folder, f"{subfolder_name}_{ses_folder}_run-{run_id}_dwi_QCed_bse-multi_BrainMask.nhdr"),
                "--tracts",
                tractography_output_path,
                "--seedingThreshold",
                "0.1",
                "--stoppingFA",
                "0.08",
                "--stoppingThreshold",
                "0.06",
                "--seedsPerVoxel",
                "3",
                "--recordFA",
                "--recordTrace",
                "--recordTensors"
            ]
            
            if freewater_enabled:
                command.extend(["--freeWater", "--recordFreeWater"])

            # Execute the command
            print(f"Processing {dwi_path} ...")
            subprocess.call(command)

# 处理每个子文件夹
for subfolder in subfolders:
    process_subfolder(subfolder, folder)

