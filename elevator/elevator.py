import heapq

class Elevator:
    def __init__(self, id, total_floors):
        self.id = id
        self.current_floor = 0
        self.total_floors = total_floors
        self.status = "idle"  # Could be 'moving', 'idle', 'maintenance'
        self.direction = None  # Could be 'up' or 'down'
        
        # Min-heap for floors to go up
        self.up_requests = []
        
        # Max-heap (negated) for floors to go down
        self.down_requests = []

    def add_request(self, floor):
        if floor > self.current_floor:
            heapq.heappush(self.up_requests, floor)
            print(f"Added floor {floor} to up requests for Elevator {self.id}")
        elif floor < self.current_floor:
            heapq.heappush(self.down_requests, -floor)
            print(f"Added floor {floor} to down requests for Elevator {self.id}")

    def update_status(self):
        if self.direction == "up" or (self.direction is None and self.up_requests):
            self.direction = "up"
            self.move_up()
        elif self.direction == "down" or (self.direction is None and self.down_requests):
            self.direction = "down"
            self.move_down()
        else:
            self.status = "idle"
            self.direction = None
            print(f"Elevator {self.id} is now idle at floor {self.current_floor}")

    def move_up(self):
        if self.up_requests and (self.direction == "up" or self.direction is None):
            # Move up by one floor
            self.current_floor += 1
            print(f"Elevator {self.id} moving up to floor {self.current_floor}")

            # Check if we've reached the next requested floor
            if self.current_floor == self.up_requests[0]:
                heapq.heappop(self.up_requests)  # Remove reached floor from requests
                print(f"Elevator {self.id} stopped at floor {self.current_floor}")
            
            # Switch direction if no more up requests and down requests are pending
            if not self.up_requests and self.down_requests:
                self.direction = "down"

    def move_down(self):
        if self.down_requests and (self.direction == "down" or self.direction is None):
            # Move down by one floor
            self.current_floor -= 1
            print(f"Elevator {self.id} moving down to floor {self.current_floor}")

            # Check if we've reached the next requested floor
            if self.current_floor == -self.down_requests[0]:
                heapq.heappop(self.down_requests)  # Remove reached floor from requests
                print(f"Elevator {self.id} stopped at floor {self.current_floor}")
            
            # Switch direction if no more down requests and up requests are pending
            if not self.down_requests and self.up_requests:
                self.direction = "up"

class ElevatorController:
    def __init__(self, num_elevators, total_floors):
        self.elevators = [Elevator(i, total_floors) for i in range(num_elevators)]

    def request_elevator(self, floor, direction):
        best_elevator = self.find_best_elevator(floor, direction)
        if best_elevator:
            print(f"Dispatching elevator {best_elevator.id} to floor {floor}")
            best_elevator.add_request(floor)

    def request_internal(self, elevator_id, destination_floor):
        elevator = self.elevators[elevator_id]
        print(f"Passenger requests floor {destination_floor} from inside elevator {elevator_id}")
        elevator.add_request(destination_floor)

    def find_best_elevator(self, requested_floor, direction):
        best_elevator = None
        min_distance = float('inf')
        
        for elevator in self.elevators:
            if elevator.status == "idle":
                distance = abs(elevator.current_floor - requested_floor)
                if distance < min_distance:
                    best_elevator = elevator
                    min_distance = distance
            elif elevator.direction == direction:
                if direction == "up" and elevator.current_floor <= requested_floor:
                    best_elevator = elevator
                elif direction == "down" and elevator.current_floor >= requested_floor:
                    best_elevator = elevator
        
        return best_elevator

    def step(self):
        for elevator in self.elevators:
            elevator.update_status()

class Building:
    def __init__(self, num_floors, num_elevators):
        self.num_floors = num_floors
        self.elevator_controller = ElevatorController(num_elevators, num_floors)
    
    def request_elevator(self, floor, direction):
        self.elevator_controller.request_elevator(floor, direction)
    
    def request_internal(self, elevator_id, destination_floor):
        self.elevator_controller.request_internal(elevator_id, destination_floor)
    
    def step(self):
        self.elevator_controller.step()
