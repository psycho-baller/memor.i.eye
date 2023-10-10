from google.cloud import vision
from google.oauth2 import service_account
import requests
import sys

from shared import get_conn, get_cohere_client

credentials = service_account.Credentials.from_service_account_file('./keys.json')

co = get_cohere_client()
go = vision.ImageAnnotatorClient(credentials=credentials)

def get_caption_from_desc(desc):
    response = co.generate(prompt=f'''Given the objects in an image, this program will generate a description

Objects: Airplane,Truck,Truck left,Truck left
Description: Image showing an airplane and truck at the center with two trucks on the left
--
Objects: Chair top,Chair top left,Packaged goods
Description: Image showing Packaged goods at the center with a chair at the top and a chair at the top left
--
Objects: Packaged goods,Packaged goods bottom left,Packaged goods bottom right,Packaged goods left,Packaged goods right,Packaged goods right,Packaged goods right,Packaged goods right,Packaged goods right,Packaged goods top right
Description: Image showing Packaged goods at the center with four objects around it
--
Objects: {desc}
Description:''',
temperature=0.9,max_tokens=100,stop_sequences=["--"])
    return response.generations[0].text.split("--")[0].strip()

def get_image_desc(url):
    image = vision.Image(content=requests.get(url).content)
    objects = go.object_localization(image=image).localized_object_annotations
    object_descriptions = []
    for object_ in objects:
        if object_.score < 0.5:
            continue
        mean_x = 0
        mean_y = 0
        for vertex in object_.bounding_poly.normalized_vertices:
            mean_x += vertex.x
            mean_y += vertex.y
        mean_x /= len(object_.bounding_poly.normalized_vertices)
        mean_y /= len(object_.bounding_poly.normalized_vertices)
        description = object_.name
        if mean_y < (1/3):
            description += " top"
        elif mean_y > (2/3):
            description += " bottom"

        if mean_x < (1/3):
            description += " left"
        elif mean_x > (2/3):
            description += " right"
        object_descriptions.append(description)
    object_descriptions.sort()

    return ",".join(object_descriptions)

with get_conn() as conn:
    with conn.cursor() as cur:
        id_ = int(sys.argv[1])
        cur.execute("SELECT url FROM Image WHERE id = %s", (id_,))
        url = cur.fetchone()['url']

        description = get_image_desc(url)
        caption = get_caption_from_desc(description)
        embed = co.embed(texts=[caption]).embeddings[0]

        cur.execute("UPDATE Image SET embed = %s, description = %s WHERE id = %s", (",".join(map(str, embed)), caption, id_))

