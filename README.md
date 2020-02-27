# hl7_utils

`hl7_utils` are a suite of HL7 utilities.

## Utilities

### Create HL7 messages from jinja template

Example of running command
```bash
python3 hl7_template_builder.py -i samples/input-data.csv -t samples/hl7-template.j2 -k MRN SYSTEMCODE
```


## Installing
With git:
```bash
git clone https://github.com/dmorand17/hl7_utils
cd hl7_utils
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
source ./env/bin/deactivate
```

With pip (_not yet implemented_):
```bash
pip install hl7_utils
```
