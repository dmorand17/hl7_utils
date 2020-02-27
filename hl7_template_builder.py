from csv_utils.csv_handler import CSVHandler, InputDelim
from csv_utils.csv_jinja import CSVJinja
from pathlib import Path
import shutil
import os.path
import datetime
import argparse

parser = argparse.ArgumentParser(description='This script will generate a file based on a template and csv file')
parser.add_argument('-i', '--input', help='input file containing mapping to be used in template', required=True, action='store')
parser.add_argument('-t', '--templates', help='template filename(s)', required=True, action='store', nargs='+')
parser.add_argument('-k', '--keys', help='key(s) to use for unique files', required=True, action='store', nargs='+')
parser.add_argument('-d', '--delim', help='delimiter used in csv input file', action='store', default='comma', type=InputDelim, choices=list(InputDelim))
parser.add_argument('--concat', help='concatenate messages', action='store_true')
args = parser.parse_args()


p = Path(".msgs")
if p.is_dir():
    shutil.rmtree(".msgs")
p.mkdir()

csvhandler = CSVHandler(args.input,delim=args.delim)
csv_jinja = CSVJinja()

template_globals = {
    'now' : datetime.datetime.now()
}

#rendered = csv_jinja.render_template(args.template,csvhandler.rows(),**template_globals)
# print(csvhandler.headers())
# print(rendered)

key = lambda r: '-'.join([r[key] for key in args.keys])
templates = []
for template in args.templates:
    template_renders = {
        'name':template
    }
    template_renders['rendered'] = csv_jinja.render_template_to_list(template,csvhandler.rows(),csvhandler.headers(),rowkey=key,**template_globals)
    templates.append(template_renders)

# Create 1..n files
file_suffix = ".txt"

if args.concat is True:
    for template in templates:
        rendered_templates = [render.get("template") for render in template.get("rendered")]
        
        filename = template.get("name") + "concatenated-msg" + file_suffix
        complete_path = os.path.join(".msgs/",filename)
        with open(complete_path,"w", newline='\n') as hl7msg:
            hl7msg.write("\n".join(rendered_templates))
else:
    for c,template in enumerate(templates,1):
        for render in [render for render in template.get("rendered")]:
            msgs = render.get("template").split("<<MSG>>")
            print(render)
            for i,msg in enumerate(msgs,1):
                filename = str(c) + "-" + render.get("key") +"-" + str(i) + "-" + "msg-" + file_suffix
                complete_path = os.path.join(".msgs/",filename)

                with open(complete_path,"w", newline='\r') as hl7msg:
                    hl7msg.write(msg)