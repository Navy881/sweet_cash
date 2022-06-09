
def create_category_tree(transaction_categories: list):
    result = []

    while transaction_categories:

        sub_category = transaction_categories.pop(0)

        if sub_category.parent_category_id is None:
            result.append(sub_category)
            continue

        for parent_candidate in transaction_categories:
            if parent_candidate.sub_categories is None:
                parent_candidate.sub_categories = []
            if sub_category.parent_category_id == parent_candidate.id:
                parent_candidate.sub_categories.append(sub_category)
                break

        if len(parent_candidate.sub_categories) > 0 and len(transaction_categories) > 0:
            continue

        result.append(sub_category)

    result = list(reversed(result))

    return result
