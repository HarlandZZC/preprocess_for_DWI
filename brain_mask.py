import os
import argparse
import subprocess
# source /data01/software/bashrc && conda activate dmri_seg
# python /home/haolin/Research/Preprocess/brain_mask.py --folder folder

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--folder', required=True, help='文件夹路径')
args = parser.parse_args()

# 获取文件夹的路径
folder = args.folder

# 获取文件夹中的所有子文件夹
subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]

# 定义处理函数
def process_subfolder(subfolder_path, folder_path):
    subfolder_name = os.path.basename(subfolder_path)  # 获取子文件夹名称
    folder_name = os.path.basename(folder_path)
    print(f"----- brain mask for {subfolder_name} -----") 
    ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith('ses-') and os.path.isdir(os.path.join(subfolder_path, f))]
    
    for ses_folder in ses_folders:
        dwi_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/corrected_masked/')
        dwi_files = [f for f in os.listdir(dwi_folder) if f.startswith(f'{subfolder_name}_{ses_folder}_run-') and f.endswith('_dwi_QCed.nrrd')]
        
        for dwi_file in dwi_files:
            dwi_path = os.path.join(dwi_folder, dwi_file)
            txt_file = os.path.join('/home/haolin/Research/Preprocess/dwi_list', f'{folder_name}_list.txt')

            with open(txt_file, "w") as f:
                f.write(dwi_path)

            model_folder = "/data01/software/CNN-Diffusion-MRIBrain-Segmentation/model_folder"

            print(f"Processing {dwi_path} ...")
            
            command = f"/data01/software/CNN-Diffusion-MRIBrain-Segmentation/pipeline/dwi_masking.py -i {txt_file} -f {model_folder}"

            subprocess.call(command, shell=True, executable="/bin/bash")

# 处理每个子文件夹
for subfolder in subfolders:
    process_subfolder(subfolder, folder)
