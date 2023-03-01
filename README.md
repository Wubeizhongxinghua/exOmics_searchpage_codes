# exOmics Searchpage Codes

***!! 注意：entity不再作为函数 `select_molecule_entity_value`的output，而是作为input。在网页中进行选择。***


**This repo. is for restoring and updating code used for exOmics search page.**

The site of web page prototype is: https://cc.mockplus.cn/s/7QMjg54avJO

*The following contents are updating records and todos.*

1. Table & barplot

- [X] Code
- [X] Prototype
- [X] Tables of projection of sites of SNP, Editing to genes

- Use function:
  ```python
  from tableBar import tableBar
  import pandas as pd
  import pymysql
  import ...

  conn = ...
  fig, data_json = tableBar(gene, feature, dataset, disease, specimen, entity, conn)
  ```

2. Boxplot

- [X] Code of not stacked barplot
- [X] Code of stacked barplot
- [X] Prototype

+ Use function:
  ```python
  from nonStackBox import nonStackBox
  from stackBox import stackBox
  import pandas as pd
  import pymysql
  import ...

  conn = ...
  fig_stack = stackBox(gene, feature, dataset, specimen, entity, conn)
  fig_nonstack = nonStackBox(gene, feature, dataset, specimen, entity, conn)
  ```

3. Heatmap

- [X] Code
- [X] Prototype
- [X] Tables of projection of sites of SNP, Editing to genes

+ Use function:
  ```python
  from heatMap import heatMap
  import pandas as pd
  import pymysql
  import ...

  conn = ...
  fig = heatMap(gene, feature, dataset, specimen, entity, conn)
  ```

4. Comparison box plot

- [X] Code
- [ ] Prototype

+ Use function:

```python
import pandas as pd
from matplotlib.figure import Figure
import numpy as np
import matplotlib.cm as cm
from copy import copy
from plots.select_molecole_entity_value import select_molecule_entity_value
from statannotations.Annotator import Annotator
import matplotlib as mpl
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
from comparison import comparison

conn = ...
fig = comparison(gene, feature, dataset, specimen, entity, conn)
```

## About repo

- If you need to run a script locally, put it in the `/scripts/` directory. Won't be updated to the online repo.
- You can refer to `/scripts/example.py` for writing new scripts, or you can write any new scripts from scratch. However, do not modify `/scripts/example.py` directly.
- Do not reveal any database secrets in a file, if the file is seen by git.
