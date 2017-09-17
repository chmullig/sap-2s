import sys, os
import csv
import tempfile
import subprocess

SELECT_CMD = "gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER -dFirstPage={start} -dLastPage={end} -sOutputFile=\"{destination}\" \"{file}\""
MERGE_CMD = " gs  -o {merged}  -sDEVICE=pdfwrite  -dColorConversionStrategy=/LeaveColorUnchanged  -dEncodeColorImages=false  -dEncodeGrayImages=false  -dEncodeMonoImages=false {files}"

tmpdir = tempfile.mkdtemp()
print(tmpdir)
files = []
subprocess.run("pandoc intro.md -s -o intro.pdf", shell=True)
with open("contents.csv") as csvf:
    contents = csv.DictReader(csvf)
    for i, entry in enumerate(contents):
        if entry['start']:
            destination = "{}_{}".format(i, entry['file'])
            files.append("\""+tmpdir+"/"+destination+"\"")
            cmd = SELECT_CMD.format(destination=tmpdir+"/"+destination, **entry)
            print(cmd)
            subprocess.run(cmd, shell=True)
        else:
            files.append("\""+entry['file']+"\"")
print(tmpdir)
cmd = MERGE_CMD.format(merged="merged.pdf", files=" ".join(files))
print(cmd)
subprocess.run(cmd, shell=True)
