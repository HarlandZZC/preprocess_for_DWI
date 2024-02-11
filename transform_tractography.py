import os
import argparse
import subprocess
from multiprocessing.pool import ThreadPool
import concurrent.futures
import whitematteranalysis as wma
# source /data01/software/bashrc && conda activate WMA
# python /home/haolin/Research/Preprocess/transform_tractography.py --folder folder --num_workers 6 

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--folder', required=True, help='文件夹路径')
parser.add_argument('--num_workers', default=4, type=int, help='Number of threads') 
args = parser.parse_args()

# 获取文件夹的路径和最大线程数
folder = args.folder
num_workers = args.num_workers

def command_harden_transform(polydata, transform, inverse, slicer_path, outdir):
    if inverse:
        str_inverse = 1
    else:
        str_inverse = 0

    print("<wm_harden_transform_with_slicer> Transforming:", polydata)
    cmd = slicer_path + " --no-main-window --python-script $(which harden_transform_with_slicer.py) " + \
            polydata + " " + transform + " " + str(str_inverse) + " " + outdir + " --python-code 'slicer.app.quit()' " + \
            ' >> ' + os.path.join(outdir, 'log.txt 2>&1')

    os.system(cmd)

# 获取文件夹中的所有子文件夹
subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]

# 定义处理函数
def process_subfolder(subfolder_path):
    subfolder_name = os.path.basename(subfolder_path)  # 获取子文件夹名称
    print(f"----- Tractography Transform for {subfolder_name} -----") 
    ses_folders = [f for f in os.listdir(subfolder_path) if f.startswith('ses-') and os.path.isdir(os.path.join(subfolder_path, f))]
    
    for ses_folder in ses_folders:
        tract_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/tractography/')
        tract_files = [f for f in os.listdir(tract_folder) if f.startswith(f'{subfolder_name}_{ses_folder}_run-') and f.endswith('_tractography.vtk')]
        
        for tract_file in tract_files:
            base_name = os.path.splitext(tract_file)[0]
            tract_path = os.path.join(tract_folder, tract_file)
            print(f"tract_path: {tract_path}")
            tfm_path = os.path.join(subfolder_path, f'{ses_folder}/dwi/WMA/',base_name,"TractRegistration",base_name,"output_tractography", f"itk_txform_{base_name}.tfm")
            print(f"tfm_path: {tfm_path}")
            output_folder = os.path.join(subfolder_path, f'{ses_folder}/dwi/WMA/',base_name,"TractRegistration",base_name,"output_tractography")
            print(f"output_folder: {output_folder}")

            slicer_path = "/data01/software/Slicer-5.2.2-linux-amd64/Slicer"

            inverse = 0

            # polydata = wma.io.read_polydata(tract_path)

            command_harden_transform(tract_path, tfm_path, inverse, slicer_path, output_folder)
            new_filename = os.path.join(output_folder,f"{base_name}_tfm.vtk")
            if os.path.exists(new_filename):
                os.remove(new_filename)
            os.rename(os.path.join(output_folder,tract_file), new_filename)
            
with ThreadPool(processes=num_workers) as pool:
    subfolders = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    pool.map(process_subfolder, subfolders)
