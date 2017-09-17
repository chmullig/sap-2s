import sys, os
import csv
import tempfile
import subprocess
import shutil

SELECT_CMD = "gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER -dFirstPage={start} -dLastPage={end} -sOutputFile=\"{destination}\" \"{source}\""
MERGE_CMD = " gs  -o {merged}  -sDEVICE=pdfwrite  -dColorConversionStrategy=/LeaveColorUnchanged  -dEncodeColorImages=false  -dEncodeGrayImages=false  -dEncodeMonoImages=false {files}"

tmpdir = tempfile.mkdtemp()
print(tmpdir)
files = []
subprocess.run("pandoc README.md -s -o README.pdf", shell=True)
with open("contents.csv") as csvf:
    contents = csv.DictReader(csvf)
    for i, entry in enumerate(contents):
        if entry['start']:
            destination = "{}_{}".format(i, entry['file'])
            fn = os.path.join(tmpdir, entry['directory'] + destination)
            files.append("\""+fn+"\"")
            cmd = SELECT_CMD.format(destination=fn,  source=os.path.join(entry['directory'], entry['file']), **entry)
            print(cmd)
            subprocess.run(cmd, shell=True)
        else:
            fn = os.path.join(entry['directory'], entry["file"])
            files.append("\""+fn+"\"")
print(tmpdir)
print(files)
cmd = MERGE_CMD.format(merged="merged.pdf", files=" ".join(files))
print(cmd)
subprocess.run(cmd, shell=True)

shutil.rmtree(tmpdir)