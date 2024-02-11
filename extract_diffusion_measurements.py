import os
import shutil
import argparse
# python /home/haolin/Research/Preprocess/extract_diffusion_measurements.py --subject_folder --output_folder

def copy_and_rename_files(subject_folder, output_folder):
    # 创建output_folder和子文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_commissural_folder = os.path.join(output_folder, 'tracts_commissural')
    output_left_hemisphere_folder = os.path.join(output_folder, 'tracts_left_hemisphere')
    output_right_hemisphere_folder = os.path.join(output_folder, 'tracts_right_hemisphere')

    os.makedirs(output_commissural_folder, exist_ok=True)
    os.makedirs(output_left_hemisphere_folder, exist_ok=True)
    os.makedirs(output_right_hemisphere_folder, exist_ok=True)

    # 获取subject_folder中所有一级子文件夹
    sub_folders = [folder for folder in os.listdir(subject_folder) if os.path.isdir(os.path.join(subject_folder, folder))]

    for sub_id in sub_folders:
        sub_folder_path = os.path.join(subject_folder, sub_id)
        
        WMA_folder = "ses-1_run-1_tractography_NFW"
        # 构建源文件路径和目标文件路径
        commissural_src = os.path.join(sub_folder_path, f'ses-1/dwi/WMA/{sub_id}_{WMA_folder}/FiberClustering/SeparatedClusters/diffusion_measurements_commissural.csv')
        commissural_dst = os.path.join(output_commissural_folder, f'{sub_id}_ses-1_run-1.csv')

        left_hemisphere_src = os.path.join(sub_folder_path, f'ses-1/dwi/WMA/{sub_id}_{WMA_folder}/FiberClustering/SeparatedClusters/diffusion_measurements_left_hemisphere.csv')
        left_hemisphere_dst = os.path.join(output_left_hemisphere_folder, f'{sub_id}_ses-1_run-1.csv')

        right_hemisphere_src = os.path.join(sub_folder_path, f'ses-1/dwi/WMA/{sub_id}_{WMA_folder}/FiberClustering/SeparatedClusters/diffusion_measurements_right_hemisphere.csv')
        right_hemisphere_dst = os.path.join(output_right_hemisphere_folder, f'{sub_id}_ses-1_run-1.csv')

        # 复制并重命名文件
        if os.path.exists(commissural_src):
            shutil.copy(commissural_src, commissural_dst)
        if os.path.exists(left_hemisphere_src):
            shutil.copy(left_hemisphere_src, left_hemisphere_dst)
        if os.path.exists(right_hemisphere_src):
            shutil.copy(right_hemisphere_src, right_hemisphere_dst)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy and rename diffusion measurement files.')
    parser.add_argument('--subject_folder', required=True, help='Path to the subject folder')
    parser.add_argument('--output_folder', required=True, help='Path to the output folder')
    args = parser.parse_args()

    copy_and_rename_files(args.subject_folder, args.output_folder)
