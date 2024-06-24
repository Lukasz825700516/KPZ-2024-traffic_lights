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
            "Adult" : 0,
            "Child" : 9,
            "Elderly" : 9,
            "Wheelchair" : 15,
            "Blind" : 15,
            "Suitcase" : 12,
            "Stroller" : 7,
            "X" : 0
        }

        self.__classes =  list( self.__time_increment.keys() )
        self.__already_detected = {class_name: False for class_name in self.__classes}

    def __enter__(self) -> 'TrafficLights':
        self.__is_running = True
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.__is_running = False

    def __update_state(self, elapsed_time: float) -> None:
        self.__time_left -= elapsed_time

        if self.__time_left > 0:
            return

        match self.__state:
            case LightState.GREEN:
                self.__state = LightState.RED
                self.__time_left = self.__base_red_duration
                self.__already_detected = {class_name: False for class_name in self.__classes}
            case LightState.RED:
                self.__state = LightState.GREEN
                self.__time_left = self.__base_green_duration + self.__next_green_bouns_time
                self.__next_green_bouns_time = 0
            case other:
                raise Exception(f"Unexpected state of TrafficLights: {other}")

    def __extend_time_after_detection(self, detected_classes: list[int]) -> None:
         for class_id in detected_classes:

            class_name_in = self.__convert_class_ID_to_name(class_id)
            time_inc = 0
            max_time_inc_already = 0
            
            if self.__already_detected[ class_name_in ]:
                continue
            
            for class_name, is_detected in self.__already_detected.items():
                if is_detected == True:
                    if self.__time_increment[class_name] > max_time_inc_already :
                        max_time_inc_already = self.__time_increment[class_name]
            
            if self.__time_increment[class_name_in] >= max_time_inc_already :
                time_inc = self.__time_increment[class_name_in] - max_time_inc_already
            else:
                time_inc = self.__time_increment[class_name_in]
                
            match self.__state:
                case LightState.GREEN:
                    self.__time_left += time_inc
                    self.__already_detected[ class_name_in ] = True
                case LightState.RED:
                    self.__next_green_bouns_time += time_inc
                    self.__already_detected[ class_name_in ] = True

    def __convert_class_ID_to_name(self, class_id: int) -> str:
        return self.__classes[ class_id ]

    def update(self, elapsed_time: float, classes_detected: list[int]) -> None:
        if not self.__is_running:
            raise RuntimeWarning('Cannot update state of the TrafficLights object, which is NOT running. Use `with TrafficLights() as tf:` instead.')

        self.__update_state(elapsed_time)
        self.__extend_time_after_detection(classes_detected)

    def get_state(self) -> LightState:
        START_BLINKING_WHEN_LEFT = 3
        if self.__state == LightState.GREEN and self.__time_left <= START_BLINKING_WHEN_LEFT and self.__time_left > 0:
            return LightState.BLINKING_GREEN
        return self.__state

    def get_time_left(self) -> int:
        return int(self.__time_left)
