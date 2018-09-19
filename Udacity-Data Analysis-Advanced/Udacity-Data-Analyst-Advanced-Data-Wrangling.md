---
title: '[Udacity/DA] 1 Data Wrangling'
date: 2018-06-01 07:24:32
categories: Data Science
tags:
- Udacity
- pandas
---
Gather data from a variety of sources and in a variety of formats, assess its quality and tidiness, then clean it. Inplementations with pandas.

<!-- more -->
---
## GATHER

### Web Scraping

####  Mining from html file text
- BeautifulSoup: find(), find_all(), .contents()
- API: eg.wiki — wptools.page().get().data

#### Downloading files from the internet 
- requests: get().content

```python
import shutil

import requests

url = 'http://example.com/img.png'
response = requests.get(url, stream=True)
with open('img.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
```

### Reading Different Data Format
#### Open/Save files
- os: path.exist(), path.join(a, b, mode = ‘wb’), makedirs(), listdir()
- glob: glob('pathname/*.txt’)
- with open(path, encoding=‘utf-8’) as file:   —返回Iterator
- file.read() / readline()
#### JSON
- JSON — store data in the form of dictionay
  - JSON object — dict
  - JSON array   — list (a list of values of a certain key)
    ```python
    # reading json into dataframe
    tweet_list=[]
    with open('tweet_json.txt','r') as f:
      for row in f:
          json_dict= json.loads(row)  
          to_append= {
              'tweet_id':json_dict['id'],
              'retweet_count':json_dict['retweet_count'],
              'favorite_count':json_dict['favorite_count']
          }
          tweet_list.append(to_append)
    df_json=pd.DataFrame(tweet_list, columns=['tweet_id','retweet_count','favorite_count'])
    ```
#### SQL
- RDBMS (Relational Database Management System) — use SQL to intereact with
- 与sql db交互:from sqlalchemy import create_engine
- 初始化数据库 engine = create_engine(’sqlite:///bestofrt.db')
- 写入 df.to_sql(‘master’, engine, index=False)
- 读取 pd.read_sql(’SELECT * FROM master’, engine)
#### CSV
- read_csv(filename, 'r')
- df.to_csv('filename', index=False)

### Encoding
Unicode — a Character Sets (char : number)
UTF-8 — an Encoding (number to 0/1)

---

## ASSESS
### Issue Types
#### Completeness
df[df.column].isnull()]
#### Tidiness
Structural issue
#### Quality
- Validity
- Inaccuracy
- Consistency

### Methods
- df.head(), df.tail(), df.sample()
- list(df)
- df.info()
- df.duplicated()

- pd.Series.value_counts()
- pd.Series.describe()
- pd.Series.isnull(), pd.Series.notnull()

---

## CLEAN
- Define: what to do according to Completeness/Quality / Tidiness issues we recorded during ASSESS.
- Code: make a copy first — df_clean = df.copy(); then do according to Define
- Test: Reassess the data to see if changes have been made

### Completeness
- Concatenate two tables: pd.concat([df1, df2], axis=0, ignore_index=True)      [row-wise]
- Add a column: df.col_new = …..

### Tidiness
- Select rows by index: df.ilocs[st:ed]
- Select columns: df[[col1, col2, ... ]]
- Drop a column: df.drop(col, axis=1) or  df = df[condition]
- Drop a row: df[df.col != condition]
- 2 variables in one column(): 
  - In need of extraction: pd.Series.str.extract(pat, expand=True)      [when True, return df]
  - Already splitted: pd.Series.str.split(pat=whitespace, n=-1, expand=False )
- 3 variables in two column(): pd.melt(id_ vars, var_name, value_name)
- Merge two tables: pd.merge(df1, df2, left_on = 'col1', right_on='col2', how=‘inner’)       [column-wise]
- Lowercase, Uppercase: str.lower(), str.upper()
- Change column name: 

### Quality
- List unique values in a columne: pd.Series.unique()
- Covert to another type
    -  pd.Series.astype(type)  [int, str, 'category' ]
    - pd.to_datetime(pd.Series)

- Slice: pd.Series.str[start:end]
- Strip: pd.Series.str.strip(to_strip)
- Pad: pd.Series.str.pad(num, side='left', fillchar=' ')
- Replace: pd.Series.replace(to_replace, value)
- Apply Function: df.apply(func, axis=0, **kwds)
  eg. Convert full names to abbreviations for States
  ```python
  # dictionary for states and their abbreviations
  state_abbrev = {'California': 'CA',
  				'New York': 'NY',
  				'Illinois': 'IL',
                  'Florida': 'FL',
                  'Nebraska': 'NE'}
  
  # func to be used
  def abbreviate_state(patient):
      if patient['state'] in state_abbrev.keys():
          abbrev = state_abbrev[patient['state']]
          return abbrev
      else:
          return patient['state']
  # apply
  patients_clean['state'] = patients_clean.apply(abbreviate_state, axis=1)
  ```
- Modify a cell
  - mask = patients_clean.locating_column == locating_column_value    [find the row] 
  - column_name = 'weight'   [find the column]
  - df.loc[mask, column_name] = blablabla   [modify the cell]
  eg. Change 'weight' from kg to lbs for 'Zaitseva'
  ```python
  weight_kg = patients_clean.weight.sort_values()[0]
  mask = patients_clean.surname == 'Zaitseva'
  column_name = 'weight'
  patients_clean.loc[mask, column_name] = weight_kg * 2.20462
  ```
- Void value: np.nan

## Read More
[1. Regular Expressions](https://regexone.com/lesson/capturing_groups?)

