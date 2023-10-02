import json
import uuid

def process_line(line):
    folder_name, x, y, _, _, _ = line.strip().split()
    annotation_id = str(uuid.uuid4())

    annotation = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "id": f"#{annotation_id}",
        "type": "Annotation",
        "body": [{
            "type": "TextualBody",
            "value": folder_name,
            "format": "text/html",
            "language": "en"
        }],
        "target": {
            "selector": {
                "type": "FragmentSelector",
                "conformsTo": "http://www.w3.org/TR/media-frags/",
                "value": f"xywh=pixel:{int(x)*1000},{int(y)*1000},1000,1000"
            }
        }
    }

    print(f"Appended annotation for {folder_name}")
    return annotation

annotations = []
with open('../image.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        annotations.append(process_line(line))

with open('../../annotations/annotations.w3c.json', 'w') as output_file:
    json.dump(annotations, output_file, indent=2)

print("Annotations JSON file created.")
