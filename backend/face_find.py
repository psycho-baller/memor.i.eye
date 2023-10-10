from deepface import DeepFace
import sys

from shared import get_conn, get_cohere_client

co = get_cohere_client()

_id = int(sys.argv[1])
test_path = 'pictures/' + sys.argv[1] + '.jpg'

def emotion_to_desc(emotion):
    if emotion == "angry":
        return "angry"
    elif emotion == "disgust":
        return "disgusted"
    elif emotion == "fear":
        return "fearful"
    elif emotion == "happy":
        return "happy"
    elif emotion == "sad":
        return "sad"
    elif emotion == "surprise":
        return "surprised"
    elif emotion == "neutral":
        return "neutral"
    print("unknown emotion", emotion)
    sys.exit(1)


with get_conn() as conn:
    with conn.cursor() as cur:
        try:
            obj = DeepFace.analyze(img_path = test_path, actions = ['age', 'gender', 'race', 'emotion'])
            region = obj['region']
            cur.execute("SELECT gaze_x, gaze_y FROM Image WHERE id = %s", (_id,))
            row = cur.fetchone()
            gaze_x = row['gaze_x']
            gaze_y = row['gaze_y']
            if True or (gaze_x >= region['x'] and gaze_x <= region['x'] + region['w'] and gaze_y >= region['y'] and gaze_y <= region['y'] + region['h']):
                caption = "A " + str(obj['age']) + " looking " + obj['dominant_race'] + " " + obj['gender'] + " who looks " + emotion_to_desc(obj['dominant_emotion']) + "."
                print(caption)
                embed = co.embed(texts=[caption]).embeddings[0]
                cur.execute("UPDATE Image SET embed = %s WHERE id = %s", (",".join(map(str, embed)), _id))
                for emotion in ['angry', 'disgust', 'fear', 'sad']:
                    if obj['emotion'][emotion] > 90:
                        print(f"didn't save picture because {emotion} is {obj['emotion'][emotion]}")
                        sys.exit(0)
            else:
                print("not looking at face ", _id)
                sys.exit(0)

        except ValueError:
            print("no faces", _id)
            sys.exit(0)

        cur.execute("SELECT id FROM Image WHERE valid = true");

        for valid_face in cur:
            result = DeepFace.verify(img1_path=test_path, img2_path='pictures/' + str(valid_face['id']) + '.jpg')
            print(result)
            if result['distance'] < 0.2:
                print(_id, "already in dataset")
                sys.exit(0)
            print(result)

        for i in range(5):
            try:
                print("attempting to update database for ", _id)
                cur.execute("UPDATE Image SET valid = true WHERE id = %s", (_id,))
                break
            except SerializationFailure:
                print("retrying")

        print("accepted l ", _id)
