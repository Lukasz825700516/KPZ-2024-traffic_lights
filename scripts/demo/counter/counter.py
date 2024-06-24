import argparse
import torch
import cv2
import ultralytics
import pygame
from pygame import gfxdraw
from TrafficLights import TrafficLights
from LightState import LightState

MINIMAL_DETECTION_CONFIDENCE = 0.5 # [0, 1]
MINIMAL_DETECTION_CONFIDENCE_PER_X_FRAME = 0.6
IOU = 0.5 # [0, 1]
TICK_PERIOD = 75 # in frames
FRAMES_AVG = 20
window_size = (1600, 900) # in pixels
background_color = pygame.Color(255, 255, 255) # RGBA
    
label_avg_dict = {
    0 : 0.0,
    1 : 0.0,
    2 : 0.0,
    3 : 0.0,
    4 : 0.0,
    5 : 0.0,
    6 : 0.0,
    7 : 0.0
}
label_count_dict = {
    0 : 0,
    1 : 0,
    2 : 0,
    3 : 0,
    4 : 0,
    5 : 0,
    6 : 0,
    7 : 0
}



def draw_light(screen, position, color: pygame.Color) -> None:
    gfxdraw.aacircle(screen, *position, 60, color)
    gfxdraw.filled_circle(screen, *position, 60, color)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Controls traffic lights using Deep Learning.')
    parser.add_argument('weights', type=str, help='File containing YOLO\'s weights and biases.')
    parser.add_argument('source', type=str,
        help='Source of video stream such as a camera input or a file. \
        In case of camera, use its id (usually 0). In case of a file, use its path.')
    parser.add_argument('framerate', type=float, nargs='?', default=60,
        help='A minimal duration of a frame in seconds. \
        Notice that processing a frame and inference may take longer than this.')

    return parser

def convert_opencv_img_to_pygame(opencv_image):
    opencv_image = opencv_image[:,:,::-1]  
    shape = opencv_image.shape[1::-1]
    pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')

    return pygame_image

def main() -> None:
    pygame.init()
    if not pygame.font:
        raise Warning("Fonts are disabled.")

    pygame.display.set_caption('Intelligent Traffic Ligths')
    parser = create_parser()
    args = parser.parse_args()

    device = torch.device(
        "cuda:0" if torch.cuda.is_available()
        else "cpu"
    )

    model = ultralytics.YOLO(args.weights,)
    model = model.to(device)

    with TrafficLights() as traffic_lights:

        if args.source.isdigit():
            source = int(args.source)
        else:
            source = args.source

        screen = pygame.display.set_mode(window_size)
        clock = pygame.time.Clock()
        running = True

        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill(background_color)
        font = pygame.font.Font(None, 64)

        window_center = ( int(window_size[0]/12), int(window_size[1]/8) )
        count_frames = 0
        detected_classes = []
        frame_counter = 0
        cap = cv2.VideoCapture(source)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            frame_returned, frame = cap.read()

            if not frame_returned:
                running = False
            elif pygame.key.get_pressed()[pygame.K_q]:
                running = False

            predictions = model(frame, verbose=False, conf=MINIMAL_DETECTION_CONFIDENCE, iou=IOU)
            
            
            annotated_frame = predictions[0].plot()
            
            for result in predictions:
                boxes = result.boxes.cpu().numpy()
                for i in range (len(boxes.cls)):
                    label_avg_dict[int(boxes.cls[i])] += boxes.conf[i]
                    label_count_dict[int(boxes.cls[i])] += 1

            if count_frames <= FRAMES_AVG:
                count_frames += 1
                detected_classes = []
            else:
                for i in range (len(label_avg_dict)):
                    if label_count_dict[i]:
                        label_avg_dict[i] /= label_count_dict[i]
                    if label_avg_dict[i] > MINIMAL_DETECTION_CONFIDENCE_PER_X_FRAME:
                        print("GREEN LIGHT FOR LABEL: " + str(i))
                        detected_classes.append(i)
                    label_count_dict[i] = 0
                    label_avg_dict[i] = 0.0
                count_frames = 0

            frame = cv2.resize(annotated_frame, window_size, interpolation=cv2.INTER_AREA)
            
            if (clock.get_fps() != 0.0):
                traffic_lights.update(1/clock.get_fps(),  detected_classes)

            light_color = pygame.Color(0, 0, 0)
            match traffic_lights.get_state():
                case LightState.RED:
                    light_color = pygame.Color(255, 0, 0)

                case LightState.GREEN:
                    light_color = pygame.Color(0, 255, 0)

                case LightState.BLINKING_GREEN:
                    if frame_counter < TICK_PERIOD/1.7:
                        light_color = pygame.Color(0, 255, 0)
                    else:
                        light_color = background_color

                case other:
                    light_color = pygame.Color(255, 255, 255)

            screen.fill(background_color)

            text = font.render(f'Timer: {traffic_lights.get_time_left()} s', True, (255, 255, 255))
            screen.blit(convert_opencv_img_to_pygame(frame), (0, 0))
            screen.blit(text, (10, 10))
            draw_light(screen=screen, position=window_center, color=light_color)

            pygame.display.flip()
            
            clock.tick(args.framerate)
            frame_counter += 1
            frame_counter %= TICK_PERIOD

        cap.release()


if __name__ == '__main__':
    main()
