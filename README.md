# pyarxiv

Implementation of Arxiv [http://arxiv.org/help/api/index](API)

## Usage

Output three papers where in the title contains words "dark matter"
```python
import pyarxiv

data = pyarxiv.PyArxiv()
print(data.parse(data.query('dark matter', max_items=3))['entries'])
```

If you want search by authors.
```python
import pyarxiv

data = pyarxiv.PyArxiv()
print(data.parse(data.queryByAuthor(['bengio'])))
```

