# Initial reconnaissance

To get the rough idea behind the problem of traffic lights
we went to the pedestrian crossing on the Plac Grunwaldzki in Wrocław
to eye ball the time which takes pedestrians to cross the 4 lane crossing.

As the result of measuring on stopwatch the time mentioned action takes for 
the couple of people we arrived to the conclusion for the crossing we used
it took roughly 10 seconds on average to go from one end of crossing to the 
other one, going over 4 lanes.

Using this rough estimation we came to conclusion that our system should be able 
to respond to pedestrians in less than 2 seconds - rough time for the walking length
of one lane, which in some cases can be half of the crossing.


## Notes

Collected information should be only used to eliminate AI models that have reaction times
way too slow for practical usage in our problem.


# Initial model selection

To select the best candidate model for our problem, we measured the times of AI models capable 
of image segmentation. For that we checked how long it takes for selected models to process one
image, which should give us rough estimate of capability for real time video processing.


| model                        | time (seconds) |
| --------------------------- | ---------------- |
| FasterRCNN_ResNet50_FPN_V2   | 5 |
| Hybridnets                   | 0.9 sekund |
| YOLOP                        | 0.13 |
| SSD                          | 0.20 |

