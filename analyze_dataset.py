import pandas as pd
import os

base_path = 'C:/Users/Samuel/Desktop/Cyber-Threat-Detection/CSV/CSV'
folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

print('Total attack categories:', len(folders))
print('\nAttack categories:', folders)
print('\nFile sizes and row counts:')
total_size = 0
total_rows = 0
class_info = []

for folder in folders:
    folder_path = os.path.join(base_path, folder)
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    folder_size = 0
    folder_rows = 0
    for file in files:
        file_path = os.path.join(folder_path, file)
        size = os.path.getsize(file_path) / (1024*1024)
        folder_size += size
        total_size += size
        # Count rows without loading all data
        with open(file_path, 'r') as f:
            row_count = sum(1 for line in f) - 1  # Subtract header
        folder_rows += row_count
        total_rows += row_count
    
    class_info.append({'class': folder, 'files': len(files), 'size_mb': folder_size, 'rows': folder_rows})
    print(f'{folder}: {len(files)} file(s), {folder_size:.2f} MB, {folder_rows:,} rows')

print(f'\nTotal dataset size: {total_size:.2f} MB ({total_size/1024:.2f} GB)')
print(f'Total rows: {total_rows:,}')

# Sort by row count to see imbalance
print('\nClass distribution (sorted by row count):')
class_info_sorted = sorted(class_info, key=lambda x: x['rows'], reverse=True)
for info in class_info_sorted:
    print(f"{info['class']}: {info['rows']:,} rows ({info['rows']/total_rows*100:.2f}%)")
