import cv2
import os
import gobjects
import image_proc
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\rhkdd\\Downloads\\Test-e0c32edea99b.json"

def localize_objects(image):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    objects = client.object_localization(
        image=image).localized_object_annotations

    ret_objects = []

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        obj = gobjects.DetectedObjects()
        obj.set_name(object_.name).set_score(object_.score)

        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
            obj.add_position([vertex.x, vertex.y])

        ret_objects.append(obj)

    return ret_objects

def save_and_getImage(frame):
    cv2.imwrite('resources/stream.jpg', frame)

    with open('resources/stream.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    return image

address = "http://20.20.1.4:8160"

cap = cv2.VideoCapture(address)
cap.set(cv2.CAP_PROP_POS_FRAMES, 500)

while(True):
    ret, img = cap.read()

    google_objects = localize_objects(save_and_getImage(img))

    row, col, chs = img.shape

    for obj in google_objects:
        obj.set_image_size([col, row])
        image_proc.make_line(img, obj.get_fixed_positions())

    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

