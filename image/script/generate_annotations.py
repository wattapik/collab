import json
import uuid
import aiohttp
import asyncio

async def get_post_data(session, folder_name):
    url = f"https://sketchersunited.org/posts/{folder_name.split('by')[0]}"
    headers = {"Accept": "text/json"}
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.json()
        return None

async def process_line(session, line):
    folder_name, x, y, _, _, _ = line.strip().split()
    annotation_id = str(uuid.uuid4())

    post_data = await get_post_data(session, folder_name)
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
            "language": "en",
            "tag": folder_name
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

async def main():
    annotations = []
    async with aiohttp.ClientSession() as session:
        with open('image.txt', 'r') as file:
            lines = file.readlines()

        tasks = [process_line(session, line) for line in lines]
        annotations = await asyncio.gather(*tasks)

    with open('../annotations/annotations.w3c.json', 'w') as output_file:
        json.dump(annotations, output_file, indent=2)

    print("Annotations JSON file created.")

# Run the asynchronous code
asyncio.run(main())
