# exOmics Searchpage Codes

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
  fig, data_json = tableBar(gene, feature, dataset, disease, specimen, conn)
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
  fig_stack = stackBox(gene, feature, dataset, specimen, conn)
  fig_nonstack = nonStackBox(gene, feature, dataset, specimen, conn)
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
  fig = heatMap(gene, feature, dataset, disease, specimen, conn)
  ```

4. Comparison box plot

- [ ] TODO

## About repo

- If you need to run a script locally, put it in the `/scripts/` directory. Won't be updated to the online repo.
- You can refer to `/scripts/example.py` for writing new scripts, or you can write any new scripts from scratch. However, do not modify `/scripts/example.py` directly.
- Do not reveal any database secrets in a file, if the file is seen by git.
