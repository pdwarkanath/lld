class Status:
    IDLE = "idle"
    MOVING = "moving"
    MAINTENANCE = "maintenance"

class Direction:
    UP = "up"
    DOWN = "down"
class Elevator:
    def __init__(self, id, num_floors):
        self.id = id
        self.current_floor = 0
        self.status = Status.IDLE
        self.direction = None
        self.requests = [0]*num_floors

    def add_request(self, floor):
        self.requests[floor] = 1
        self.status = Status.MOVING
        if not self.direction:
            self.direction = Direction.UP if floor > self.current_floor else Direction.DOWN
    
    def complete_request(self, floor):
        self.requests[floor] = 0        

    def move(self):
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1
        if self.requests[self.current_floor]:
            self.complete_request(self.current_floor)
            print(f"Stopping at floor {self.current_floor}")
    
    def update_status(self):
        self.move()
        if self.status == Status.MOVING:
            if sum(self.requests) == 0:
                self.status = Status.IDLE
                self.direction = None
            elif self.direction == Direction.UP:
                if self.current_floor == len(self.requests) - 1 or sum(self.requests[self.current_floor+1:]) == 0:
                    self.direction = Direction.DOWN
            elif self.direction == Direction.DOWN:
                if self.current_floor == 0 or sum(self.requests[:self.current_floor]) == 0:
                    self.direction = Direction.UP
        elif self.status == Status.IDLE:
            if sum(self.requests) > 0:
                self.status = Status.MOVING
                self.direction = Direction.UP if self.requests[self.current_floor] else Direction.DOWN
class Building:
    def __init__(self, num_elevators, num_floors):
        self.num_floors = num_floors
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]

    def request_elevator(self, floor, direction):
        best_elevator = self.find_best_elevator(floor, direction)
        if best_elevator:
            print(f"Dispatching elevator {best_elevator.id} to floor {floor}")
            best_elevator.add_request(floor)

    def find_best_elevator(self, requested_floor, direction):
        best_elevator = None
        min_distance = self.num_floors + 1

        # Strategy: 
        # 1. If an elevator is moving in the requested direction and is at a floor less than the requested floor, assign it.
        # 2. Assign closest idle elevator.
        # 3. Assign closest elevator
        for elevator in self.elevators:
            if elevator.direction == direction:
                if direction == Direction.UP and elevator.current_floor <= requested_floor:
                    best_elevator = elevator
                    break
                elif direction == Direction.DOWN and elevator.current_floor >= requested_floor:
                    best_elevator = elevator
                    break
            elif elevator.status == Status.IDLE:
                distance = abs(elevator.current_floor - requested_floor)
                if distance < min_distance:
                    best_elevator = elevator
                    min_distance = distance
        min_distance = self.num_floors + 1
        if not best_elevator:
            for elevator in self.elevators:
                distance = abs(elevator.current_floor - requested_floor)
                if distance < min_distance:
                    best_elevator = elevator
                    min_distance = distance
        return best_elevator

    def step(self):
        for elevator in self.elevators:
            elevator.update_status()

# Client code

building = Building(2, 10)
building.request_elevator(4, Direction.UP)
building.request_elevator(5, Direction.UP)
building.request_elevator(6, Direction.DOWN)

for i in range(10):
    if i == 5:
        building.request_elevator(9, Direction.DOWN)
    building.step()
