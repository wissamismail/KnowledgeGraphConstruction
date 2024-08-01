import json
from os import path
import getAllSVOs,getVerbs,getObjects,getStems
directory = "E:/workspaces/RDF/TTtoRDF/TEXTtoKG/"

dataset_names = [
    "literature.json",
    "medical-articles.json",
    "moviescripts.json",
    "news-press-releases.json",
]

models = ["GPT-4", "SpaCy", "NLTK", "LLAMA3"]

metrics = {
    "totalSVOs": lambda data: getAllSVOs.total_svos(data),
    "commonVerbs": lambda data: getVerbs.common_verbs(data),
    "commonStem": lambda data: getStems.common_stem(data),
    "commonObject": lambda data: getObjects.common_objects(data),
}

results = {}

for dataset_name in dataset_names:
    loaded_data = {}

    for model in models:
        print(path.join(directory, 'myResult/Using_' + model, dataset_name))
        with open(path.join(directory,  'myResult/Using_' + model, dataset_name), "r",encoding="utf-8") as f:
            loaded_data[model] = json.load(f)


    for name, func in metrics.items():

        if name not in results:
            print(name + ": not in results")
            results[name] = {}
        print("name: " + name + "-  dataset_name:" + dataset_name)
        results[name][dataset_name] = func(loaded_data)

with open(path.join(directory, "results.json"), "w") as f:
    json.dump(results, f, indent=2)

print("Comparison complete. Results saved to results.json.")