def total_svos(datasets):
    return {dataset: sum(data["total_SVOs"] for data in data_list.values()) for dataset, data_list in datasets.items()}