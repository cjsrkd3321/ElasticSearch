# Usage

```python
import my_es
import sys, warnings
from elasticsearch import Elasticsearch


if not sys.warnoptions:
    warnings.simplefilter("ignore")

es = Elasticsearch()

# True if created, False if failed
print(my_es.create_index(es=es, index_name="test_index"))

# True if created, False if failed
print(
    my_es.create_document(
        es=es, index_name="test_index", content={"hello": "world"}, document_id="TEST-11"
    )
)

# Document if succeeded, Empty document if failed.
print(my_es.get_document_using_id(es=es, index_name="test_index", document_id="TEST-11"))

# True if created, False if failed
print(
    my_es.update_document_using_id(
        es=es, index_name="test_index", document_id="TEST-11", content={"hello": "nope"}
    )
)

# True if created, False if failed
print(my_es.delete_document_using_id(es=es, index_name="test_index", document_id="TEST-11"))

# True if created, False if failed
print(my_es.delete_index(es=es, index_name="test_index"))
```
