from collections import defaultdict
from itertools import chain

def flatten_csl(record, name):
    attributes = []
    for attr in record.get(name, "") or record.get("SVO_relationships", []):
        if isinstance(attr, str):
            attributes.extend(s.strip() for s in attr.split(",") if s.strip())
        elif isinstance(attr, dict):
            for key, value in attr.items():
                if isinstance(value, str):
                    attributes.extend(s.strip() for s in value.split(",") if s.strip())
    return attributes

def flatten_csl2(record, name):
    return [s.strip() for attr in (record.get(name, "") or record.get("SVO_relationships", [])) for s in attr.split(",") if s.strip()]

def common_with_reference(reference, compare_func):
    def wrapper(datasets):
        common = defaultdict(int)
        datasets_to_compare = list(datasets)
        mapped_dataset = {name: {tuple(int(i) for i in k.split(",") if i.isdigit()): v for k, v in data.items()} for name, data in datasets.items()}

        for i in mapped_dataset[reference]:
            reference_record = mapped_dataset[reference][i]
            for name in datasets_to_compare:
                target_record = mapped_dataset[name].get(i)
                if target_record:
                    common[name] += compare_func(target_record, reference_record)

        return dict(common)

    return wrapper

def common_with_reference2(reference, compare_func):
    def wrapper(datasets):
        common = defaultdict(int)
        datasets_to_compare = list(datasets)

        mapped_dataset = {name: {tuple(map(int, k.split(","))): v for k, v in data.items()} for name, data in datasets.items()}

        for i in mapped_dataset[reference]:
            reference_record = mapped_dataset[reference][i]
            for name in datasets_to_compare:
                target_record = mapped_dataset[name].get(i)
                if target_record:
                    common[name] += compare_func(target_record, reference_record)

        return dict(common)

    return wrapper

def common_in_csl(property_name):
    def compare_func(target_record, reference_record):
        reference_attributes = flatten_csl(reference_record, property_name)
        attributes = flatten_csl(target_record, property_name)
        return sum(1 for attr in attributes if attr in reference_attributes)

    return compare_func