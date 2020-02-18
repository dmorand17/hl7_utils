import csv_utils
from pathlib import Path
import shutil
import os.path
import datetime
import argparse

parser = argparse.ArgumentParser(description='This script will generate a file based on a template and csv file')
parser.add_argument('-i', '--input', help='input file containing mapping to be used in template', required=True, action='store')
parser.add_argument('-t', '--template', help='template filename', required=True, action='store')
args = parser.parse_args()

csvhandler = csv_utils.CSVHandler(args.input)

csv_jinja = csv_utils.CSVJinja()
template_globals = {
    'now' : datetime.datetime.now()
}

rendered = csv_jinja.render_template(args.template,csvhandler.rows(),**template_globals)

# print(csvhandler.headers())
rendered = csv_jinja.render_template_to_dict(args.template,csvhandler.rows(),csvhandler.headers(),rowkey="MRN",**template_globals)
# print(rendered)

p = Path(".msgs")
if p.is_dir():
    shutil.rmtree(".msgs")
p.mkdir()

# Create 1..n files
file_suffix = ".txt"
for render in rendered:
    msgs = render.get("template").split("<<MSG>>")
    print(render)
    
    for i,msg in enumerate(msgs,1):
        filename = render.get("key") +"-" + str(i) + "-" + "adt-" + file_suffix
        complete_path = os.path.join(".msgs/",filename)

        with open(complete_path,"w", newline='\r') as hl7msg:
            hl7msg.write(msg)