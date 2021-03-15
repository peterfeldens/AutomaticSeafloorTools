# Make all images without .jpg as empty examples
# If no empty examples are needed, do not execute this cell

import automatic_seafloor_functions as asf

def make_empty(files, PFAD):
    for f in tqdm(files):
        filename = os.path.basename(f)
        basename = os.path.splitext(filename)[0]
        try:
            f = open(PFAD + basename + ".txt")
            f.close()
        except IOError:
            os.mknod(PFAD + basename + ".txt")
    return

files = asf.getfiles('jpg', '/content/images/train/')
make_empty(files, '/content/images/train/')

files = asf.getfiles('jpg', '/content/images/test/')
make_empty(files, '/content/images/test/')