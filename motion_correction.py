import os
import argparse
import subprocess
# conda activate motion_correct
# python /home/haolin/Research/Preprocess/motion_correction.py --folder folder

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--folder', required=True, help='文件夹路径')
args = parser.parse_args()

# 获取文件夹的路径
folder = args.folder

# 获取文件夹中的所有子文件夹
subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]

# 定义处理函数
def process_subfolder(subfolder_path):
    subfolder_name = os.path.basename(subfolder_path)  # 获取子文件夹名称
    print(f"----- motion correction for {subfolder_name} -----") 
    ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith('ses-') and os.path.isdir(os.path.join(subfolder_path, f))]
    
    for ses_folder in ses_folders:
        dwi_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/')
        dwi_files = [f for f in os.listdir(dwi_folder) if f.startswith(f'{subfolder_name}_{ses_folder}_run-') and f.endswith('_dwi.nrrd')]
        
        for dwi_file in dwi_files:
            dwi_path = os.path.join(dwi_folder, dwi_file)
            protocol_path = '/home/haolin/Research/Preprocess/dtiprepprotocalonlyeddy.xml'
            output_dir = os.path.join(subfolder_path, f'{ses_folder}/dwi/corrected_masked/')
            
            print(f"Processing {dwi_path} ...")
            
            command = ["/home/haolin/Research/Preprocess/DTIPrep-1.2.11/bin/DTIPrep", 
                       "--DWINrrdFile", dwi_path, 
                       "--default", 
                       "--check", 
                       "--xmlProtocol", protocol_path,
                       "--numberOfThreads", "16", 
                       "--outputFolder", output_dir
                       ]

            subprocess.run(command)

# 处理每个子文件夹
for subfolder in subfolders:
    process_subfolder(subfolder)
