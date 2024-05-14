import argparse
import torch
import cv2
import ultralytics
import pygame
from pygame import gfxdraw
from TrafficLights import TrafficLights
from LightState import LightState

MINIMAL_DETECTION_CONFIDENCE = 0.5
IOU = 0.5
window_size = (700, 700)
background_color = pygame.Color(255, 255, 255)


def draw_light(screen, position, color: pygame.Color) -> None:
    gfxdraw.aacircle(screen, *position, 120, color)
    gfxdraw.filled_circle(screen, *position, 120, color)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="traffic_lights_demo",
        description="Controls traffic lights using Deep Learning."
    )

    parser = argparse.ArgumentParser(description='Controls traffic lights using Deep Learning.')
    parser.add_argument('weights', type=str, help='File containing YOLO\'s weights and biases.')
    parser.add_argument('source', type=str,
        help='Source of video stream such as a camera input or a file. \
        In case of camera, use its id (usually 0). In case of a file, use its path.')
    parser.add_argument('framerate', type=float, nargs='?', default=60,
        help='A minimal duration of a frame in seconds. \
        Notice that processing a frame and inference may take longer than this.')

    return parser


def main() -> None:

    pygame.init()
    if not pygame.font:
        raise Warning("Fonts are disabled.")

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

        if pygame.font:
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill(background_color)
            font = pygame.font.Font(None, 64)

        window_center = ( int(window_size[0]/2), int(window_size[1]/2) )

        while running:

            cap = cv2.VideoCapture(source)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            frame_returned, frame = cap.read()

            if not frame_returned:
                running = False
            elif pygame.key.get_pressed()[pygame.K_q]:
                running = False

            predictions = model(frame, verbose=False, conf=MINIMAL_DETECTION_CONFIDENCE, iou=IOU)
            detected_classes = [ int(detection.cls) for detection in predictions[0].boxes ]
            traffic_lights.update(1/args.framerate,  detected_classes)

            light_color = pygame.Color(0, 0, 0)
            match traffic_lights.get_state():
                case LightState.RED:
                    light_color = pygame.Color(255, 0, 0)

                case LightState.GREEN:
                    light_color = pygame.Color(0, 255, 0)

                case other:
                    raise Warning(f'Unknown color of the traffic light: {other}.')

            screen.fill(background_color)

            text = font.render(f'Timer: {traffic_lights.get_time_left()} s', True, (10, 10, 10))
            screen.blit(text, (10, 10))

            draw_light(screen=screen, position=window_center, color=light_color)

            pygame.display.flip()
            clock.tick(args.framerate)

        cap.release()


if __name__ == '__main__':
    main()
