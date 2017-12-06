class Point(object):


    def __init__(self, time=0,coordinate=0.0,timeLong=0):
        self.time = time
        self.coordinate = coordinate
        self.dimension = len(coordinate)
        self.timeLong = timeLong

    def print1(self):
        print(self.time)