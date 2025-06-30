class PickupRequest:
    def __init__(self, customer_id, preferred_time, flexibility=False):
        # store customer id
        self.customer_id = customer_id
        # store preferred time slot as a string, e.g., "4-5 PM"
        self.preferred_time = preferred_time
        # store if customer is flexible with time slot
        self.flexibility = flexibility
        # assigned slot will be filled later
        self.assigned_time = None
        # flag to show if incentive was given
        self.incentive_awarded = False


class TimeSlot:
    def __init__(self, time_range, max_capacity):
        # store time range, e.g., "4-5 PM"
        self.time_range = time_range
        # max number of pickup requests this slot can hold
        self.max_capacity = max_capacity
        # list of assigned pickup requests
        self.assigned_requests = []

def calculate_score(slot, request):
    # if slot matches preferred time, score is low
    if slot.time_range == request.preferred_time:
        base_score = 1
    else:
        base_score = 5

    # add penalty if slot is near full
    fill_ratio = len(slot.assigned_requests) / slot.max_capacity
    penalty = fill_ratio * 10

    # if customer is flexible, reduce penalty slightly
    if request.flexibility:
        penalty *= 0.8

    return base_score + penalty

def assign_slot(request, slots):
    best_slot = None
    best_score = float('inf')

    for slot in slots:
        if len(slot.assigned_requests) >= slot.max_capacity:
            continue

        score = calculate_score(slot, request)
        if score < best_score:
            best_score = score
            best_slot = slot

    if best_slot:
        best_slot.assigned_requests.append(request)
        request.assigned_time = best_slot.time_range

        # award incentive if flexible and slot is not preferred
        if request.flexibility and best_slot.time_range != request.preferred_time:
            request.incentive_awarded = True

# create slots
slots = [
    TimeSlot("9-10 AM", max_capacity=3),
    TimeSlot("10-11 AM", max_capacity=3),
    TimeSlot("11-12 PM", max_capacity=3)
]

# create requests
requests = [
    PickupRequest("C001", "10-11 AM", flexibility=True),
    PickupRequest("C002", "10-11 AM", flexibility=False),
    PickupRequest("C003", "11-12 PM", flexibility=True),
    PickupRequest("C004", "9-10 AM", flexibility=False),
    PickupRequest("C005", "10-11 AM", flexibility=True)
]

# assign each request to a slot
for req in requests:
    assign_slot(req, slots)

# show results
print("--- Pickup Schedule ---")
for req in requests:
    print(f"Customer: {req.customer_id} | Preferred: {req.preferred_time} | Assigned: {req.assigned_time} | Incentive: {'✔' if req.incentive_awarded else '✘'}")

print("\n--- Slot Utilization ---")
for slot in slots:
    print(f"Slot {slot.time_range}: {len(slot.assigned_requests)}/{slot.max_capacity}")
