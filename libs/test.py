import os
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
FILES = os.path.join(CUR_PATH, 'tpdf_templates')
f1 = os.path.join(FILES, 'NewName','fields.json')
print(f1)