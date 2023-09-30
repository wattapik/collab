import json
import uuid
import requests

def get_post_data(folder_name):
    url = f"https://sketchersunited.org/posts/{folder_name.split('by')[0]}"
    headers = {"Accept": "text/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

with open('image.txt', 'r') as file:
    lines = file.readlines()

annotations = []

for line in lines:
    folder_name, x, y, _, _, _ = line.strip().split()
    annotation_id = str(uuid.uuid4())

    post_data = get_post_data(folder_name)
    if post_data:
        annotation_text = f'🖼️ <a href="https://sketchersunited.org/posts/{post_data["post"]["id"]}">{post_data["post"]["title"]}</a> <br>👤 <a href="https://sketchersunited.org/users/{post_data["post"]["profile"]["id"]}">@{post_data["post"]["profile"]["username"]}</a>'
    else:
        annotation_text = "Data not available"

    annotation = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "id": f"#{annotation_id}",
        "type": "Annotation",
        "body": [{
            "type": "TextualBody",
            "value": annotation_text,
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

    annotations.append(annotation)
    print(f"Appended annotation for {folder_name}")

with open('../annotations/annotations.w3c.json', 'w') as output_file:
    json.dump(annotations, output_file, indent=2)

print("Annotations JSON file created.")
