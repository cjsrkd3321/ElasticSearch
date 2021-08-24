def print_fail_reason(func: object, result: dict) -> None:
    print(f"[{__name__} -> {func.__name__}] [{result['status']}] {result['error']['root_cause']}")


def create_index(es, index_name: str) -> bool:
    is_created = False
    if (not es.indices.exists(index=index_name)) and es.indices.create(index=index_name)[
        "acknowledged"
    ]:
        is_created = True
    return is_created


def delete_index(es, index_name: str) -> bool:
    is_deleted = False
    if es.indices.exists(index=index_name) and es.indices.delete(index=index_name)["acknowledged"]:
        is_deleted = True
    return is_deleted


def create_document(
    es, index_name: str, content: dict, document_id: str, ignore: list = [400, 404, 409]
) -> bool:
    is_created = False
    result = es.create(index=index_name, body=content, id=document_id, ignore=ignore)
    if result.get("result", "") == "created":
        is_created = True
    else:
        print_fail_reason(create_document, result)
    return is_created


def get_document_using_id(es, index_name: str, document_id: str) -> dict:
    document = {}
    result = es.search(index=index_name, body={"query": {"match": {"_id": document_id}}})
    if result["hits"]["total"]["value"]:  # value is 1 then,
        document = result["hits"]["hits"][0]["_source"]
    else:
        print_fail_reason(get_document_using_id, result)
    return document


def get_document(es, index_name: str, content: dict) -> dict:
    document = {}
    result = es.search(index=index_name, body=content)
    if result["hits"]["total"]["value"]:  # value is 1 then,
        document = result["hits"]["hits"][0]["_source"]
    else:
        print_fail_reason(get_document_using_id, result)
    return document


def update_document_using_id(
    es, index_name: str, document_id: str, content: dict, ignore: list = [400, 404, 409]
) -> bool:
    is_updated = False
    result = es.update(index=index_name, id=document_id, body={"doc": content}, ignore=ignore)
    if result.get("result", "") == "updated":
        is_updated = True
    elif result.get("result", "") == "noop":
        print("No updated(maybe data equal before update).")
    else:
        print_fail_reason(get_document_using_id, result)
    return is_updated


def delete_document_using_id(
    es, index_name: str, document_id: str, ignore: list = [400, 404, 409]
) -> bool:
    is_deleted = False
    result = es.delete(index=index_name, id=document_id, ignore=ignore)
    if result.get("result", "") == "deleted":
        is_deleted = True
    elif result.get("result", "") == "not_found":
        print("Not found data.")
    else:
        print_fail_reason(delete_document_using_id, result)
    return is_deleted
