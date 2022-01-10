from collections import Counter, defaultdict
import pandas as pd


def compute_progress(name, out_name):
    df = pd.read_csv(name)
    df["Key Result"].replace(regex=r'</*div>', value="", inplace=True)
    df["Key Result method"].replace(regex=r'</*div>', value="", inplace=True)
    objectives = []

    key_results = []
    key_results_done = []
    for (_, row) in df.iterrows():
        if(row["Work Item Type"] == "Objective"):
            objectives.append({"title": row["Title"], "id": row["ID"], "features": [
            ], "Assigned To": row["Assigned To"], "Area Path": row["Area Path"]})

    for (_, row) in df.iterrows():
        if (row["Work Item Type"] == "Feature"):
            progress = 100 if row["State"] in [
                "Done", "Closed", "Resolved"] else 0
            Kresults = row["Key Result"].split(
                ", ") if isinstance(row["Key Result"], str) else []
            Kresults_methods = row["Key Result method"].split(
                ", ") if isinstance(row["Key Result method"], str) else []

            for krm in Kresults_methods:
                obj = list(filter(lambda x: str(x["id"]) == krm, objectives))
                if len(obj):
                    obj[0]["features"].append({"id": row["ID"],
                                               "title": row["Title"], "state": row["State"],
                                               "id": row["ID"],
                                               "progress": progress, "Key Result": [{'key': k, 'progress': progress} for k in Kresults]})

            for k in Kresults:
                key_results.append(k)

                if progress == 100:
                    key_results_done.append(k)

    key_results_map = Counter(key_results)
    key_results_done_map = Counter(key_results_done)
    key_set = set(key_results)
    for obj in objectives:
        d = {}
        for feature in obj["features"]:
            for k in feature["Key Result"]:
                key = k["key"]
                k["progress"] = 100 * key_results_done_map[key] / \
                    key_results_map[key]
        if len(obj['features']):
            obj["progress"] = sum(
                map(lambda x: x["progress"], obj["features"]))/len(obj["features"])
        else:
            print(obj)

    list_progress = []

    for obj in objectives:
        key_res = []
        features = defaultdict(list)
        for feature in obj["features"]:
            for k in feature["Key Result"]:
                features[k["key"]].append(
                    feature["title"]
                )
                if k['key'] not in key_res:
                    list_progress.append(
                        {
                            'Objective': obj['title'],
                            'Key Result': k['key'],
                            "Id Objective": obj['id'],
                            "Progress Objective": obj["progress"],

                            'Progress Key Result': k['progress'],
                            'Area Path': obj['Area Path'],
                            'Assigned To': obj['Assigned To'],
                        })

                    key_res.append(k["key"])

                line = [x for x in list_progress if x["Key Result"]
                        == k["key"] and x["Objective"] == obj["title"]][0]
                line["Feature"] = ", ".join(features[k["key"]])

    df_progress = pd.DataFrame(list_progress)

    df_progress.to_excel(out_name, index=False)


if __name__ == "__main__":
    import sys
    _, input_file, output_file = sys.argv
    compute_progress(input_file, output_file)
