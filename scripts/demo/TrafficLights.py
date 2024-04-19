from LightState import LightState
import os

class TrafficLights:
    def __init__(self):
        self.__base_green_duration = 15
        self.__base_red_duration = 15
        self.__next_green_bouns_time = 0

        self.__state = LightState.GREEN
        self.__time_left = self.__base_green_duration

        self.__is_running = False

        self.__time_increment = { # in seconds
            "Elderly" : 9,
            "Child" : 9,
            "Adult" : 0,
            "Wheelchair" : 15,
            "Blind" : 15,
            "Suitcase" : 12,
        }

        self.__classes =  list( self.__time_increment.keys() )
        self.__already_detected = {class_name: False for class_name in self.__classes}

    def start(self) -> None:
        self.__is_running = True

    def __update_state(self, elapsed_time: float) -> None:

        self.__time_left -= elapsed_time

        if self.__time_left < 0:
        
            if self.__state == LightState.RED:
                self.__state = LightState.GREEN
                self.__time_left = self.__base_green_duration + self.__next_green_bouns_time
                self.__next_green_bouns_time = 0
                self.__already_detected = {class_name: False for class_name in self.__classes}

            elif self.__state == LightState.GREEN:
                self.__state = LightState.RED
                self.__time_left = self.__base_red_duration

    def __extend_time_after_detection(self, detected_classes: list[int]) -> None:
         for class_id in detected_classes:

            class_name = self.__convert_class_ID_to_name(class_id)

            if self.__already_detected[ class_name ]:    
                continue
            
            elif self.__state == LightState.RED:
                self.__next_green_bouns_time += self.__time_increment[ class_name ]

            elif self.__state == LightState.GREEN:
                self.__time_left += self.__time_increment[ class_name ]
                self.__already_detected[ class_name ] = True       

    def __convert_class_ID_to_name(self, class_id: int) -> str:
        return self.__classes[ class_id ]

    def update(self, elapsed_time: float, classes_detected: list[int]) -> None:
        if not self.__is_running:
            return
        
        self.__update_state(elapsed_time)
        self.__extend_time_after_detection(classes_detected)
    
    def display(self) -> None:
        os.system("clear")
        green = "32"  
        red = "31"  

        color = green if self.__state == LightState.GREEN else red

        print(f"\033[{color}m\u25CF\033[0m", f"Timer: {int(self.__time_left)}")