import os
import os.path


def merge_folds(data_dir):
    """
    Given data directory (which holds folds)
    merges all files within these folds and returns them to
    data_dir/Merged_Folds/
    """
    all_files = []
    roots = []
    for (root, dirs, files) in os.walk(data_dir):
        all_files += files
        roots.append(root)
    print(roots)
    dir_name = os.path.join(roots[0], "Merged_Folds")
    os.mkdir(dir_name)
    for file in files:
        for root in roots:
            try:
                rf = open(os.path.join(root, file), 'r')
                with open(os.path.join(dir_name, file), 'a') as wf:
                    for line in rf:
                        wf.write(line)
                rf.close()
            except IOError:
                continue
    return dir_name

if __name__ == '__main__':
    from sys import args
    merge_folds(args[1])
