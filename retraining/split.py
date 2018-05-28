import os
from shutil import copyfile

rootDir="./original_data"

classes = os.listdir(rootDir)

class_to_files = {}
for data_class in classes:
    files = os.listdir(os.path.join(rootDir, data_class))
    class_to_files[data_class] = files

SPLIT_DATA_DIR = "split_data"
TRAIN_DIR = "train"
TEST_DIR = "test"

os.mkdir(SPLIT_DATA_DIR)
os.mkdir(os.path.join(SPLIT_DATA_DIR, TRAIN_DIR))
os.mkdir(os.path.join(SPLIT_DATA_DIR, TEST_DIR))

for data_class in classes:
    files = class_to_files[data_class]
    num_files = len(class_to_files[data_class])
    train_num = int(0.7 * num_files)
    test_num = int((1 - 0.7) * num_files)
    
    train_set = files[0:train_num]
    test_set = files[train_num+1:]

    os.mkdir(os.path.join(SPLIT_DATA_DIR, TRAIN_DIR, data_class)) 
    os.mkdir(os.path.join(SPLIT_DATA_DIR, TEST_DIR, data_class)) 

    for file in train_set:
        src = os.path.join(rootDir, data_class, file)
        dst = os.path.join(SPLIT_DATA_DIR, TRAIN_DIR, data_class, file)
        copyfile(src, dst)

    for file in test_set:
        src = os.path.join(rootDir, data_class, file)
        dst = os.path.join(SPLIT_DATA_DIR, TEST_DIR, data_class, file)
        copyfile(src, dst)

# for path, dirs, files in os.walk(rootDir):
    # print(dirs)
    # for filename in files:
        # fullpath = os.path.join(path, filename)
        # # print(fullpath)


