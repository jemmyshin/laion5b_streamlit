import os
import time
from jina import Client
from docarray import DocumentArray, Document



root_path = '/Users/jemfu/Desktop/tm_designs'
trademarks = os.listdir(root_path)

c = Client(host='grpcs://special-python-448971d4aa.wolf.jina.ai')

da = DocumentArray()

for tm in trademarks:
    doc = Document(id=tm, uri=os.path.join(root_path, tm)).load_uri_to_blob()
    doc.uri = None
    da.append(doc)

batch_size = 256
idx = 0
print("start encoding ...")
s_0 = time.time()
while idx < len(da):
    start_idx = idx
    end_idx = min(idx+batch_size, len(da))

    tmp_da = da[start_idx:end_idx]
    s = time.time()
    c.post('/index', tmp_da)
    print("done a batch, cost: {}".format(time.time() - s))
    idx += batch_size

s_1 = time.time()
print("encoding takes: {}".format(s_1 - s_0))
