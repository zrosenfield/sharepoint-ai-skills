# Give every source pptx a unique slide-master / layout ID range so decks assembled from many
# one-slide files never collide (Copilot renumbers masters from 2147483648 but keeps layout IDs).
import zipfile, re, sys, os, shutil, glob
BASE = 2147483648
def fix(path, k):
    off = BASE + 10000 * (k + 1)
    src = zipfile.ZipFile(path); out = path + ".tmp"; dst = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    n = [0]
    def ren(m):
        old = int(m.group(2)); new = off + (old - BASE); n[0] += 1
        return '%sid="%d"' % (m.group(1), new)
    for item in src.infolist():
        data = src.read(item.filename)
        if item.filename == "ppt/presentation.xml" or re.match(r"ppt/slideMasters/slideMaster\d+\.xml$", item.filename):
            s = data.decode("utf-8")
            s = re.sub(r'(<p:sldMasterId )id="(\d+)"', ren, s)
            s = re.sub(r'(<p:sldLayoutId )id="(\d+)"', ren, s)
            data = s.encode("utf-8")
        dst.writestr(item, data)
    dst.close(); src.close(); shutil.move(out, path); return n[0]
files = sorted(glob.glob("content/slides/*.pptx")) + sorted(glob.glob("content/templates/*.pptx"))
for k, f in enumerate(files):
    print(os.path.basename(f), fix(f, k))
