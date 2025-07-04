import random
import time
import csv
import matplotlib.pyplot as plt

class PickupRequest:
    def __init__(self, customer_id, preferred_time, flexibility=False):
        # store customer id
        self.customer_id = customer_id
        # store preferred time slot
        self.preferred_time = preferred_time
        # store if customer is flexible
        self.flexibility = flexibility
        # assigned slot
        self.assigned_time = None
        # incentive flags
        self.incentive_awarded = False
        self.incentive_value = 0.0
        # waitlist flag
        self.waitlisted = False

class TimeSlot:
    def __init__(self, time_range, max_capacity):
        # store time range
        self.time_range = time_range
        # max capacity for the slot
        self.max_capacity = max_capacity
        # assigned requests
        self.assigned_requests = []

def calculate_score(slot, request):
    # base score for preferred match
    if slot.time_range == request.preferred_time:
        base_score = 1
    else:
        base_score = 5

    # add penalty based on fill ratio
    fill_ratio = len(slot.assigned_requests) / slot.max_capacity
    penalty = fill_ratio * 10

    # adjust it if customer is flexible
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

    if not best_slot:
        print(f"warning: no available slot for {request.customer_id}")
        request.waitlisted = True
        request.assigned_time = "WAITLISTED"
        return

    best_slot.assigned_requests.append(request)
    request.assigned_time = best_slot.time_range

    if request.flexibility and best_slot.time_range != request.preferred_time:
        request.incentive_awarded = True
        request.incentive_value = 1.0  # example: $1 off

# fifo version
def assign_slot_fifo(request, slots):
    for slot in slots:
        if len(slot.assigned_requests) < slot.max_capacity:
            slot.assigned_requests.append(request)
            request.assigned_time = slot.time_range
            return
    request.waitlisted = True
    request.assigned_time = "WAITLISTED"

# generate slots
slots_template = [
    TimeSlot("9-10 AM", max_capacity=10),
    TimeSlot("10-11 AM", max_capacity=10),
    TimeSlot("11-12 PM", max_capacity=10),
    TimeSlot("12-1 PM", max_capacity=10)
]

# generate random requests
def generate_requests(num_requests, slots):
    requests = []
    for i in range(num_requests):
        preferred = random.choices(
            [slot.time_range for slot in slots],
            weights=[3, 3, 3, 1]
        )[0]
        flexible = random.choice([True, False])
        requests.append(PickupRequest(f"C{i+1:03}", preferred, flexibility=flexible))
    return requests

# generate same requests for both
requests_fifo = generate_requests(32, slots_template)
requests_smart = [PickupRequest(r.customer_id, r.preferred_time, r.flexibility) for r in requests_fifo]

# make fresh slots for both
slots_fifo = [TimeSlot(s.time_range, s.max_capacity) for s in slots_template]
slots_smart = [TimeSlot(s.time_range, s.max_capacity) for s in slots_template]

# run fifo
start_fifo = time.time()
for req in requests_fifo:
    assign_slot_fifo(req, slots_fifo)
end_fifo = time.time()

# run smartslot
start_smart = time.time()
for req in requests_smart:
    assign_slot(req, slots_smart)
end_smart = time.time()

# show fifo results
print("\n--- FIFO Schedule ---")
for req in requests_fifo:
    print(f"Customer: {req.customer_id} | Preferred: {req.preferred_time} | Assigned: {req.assigned_time}")

# show smartslot results
print("\n--- SmartSlot Schedule ---")
for req in requests_smart:
    status = "WAITLISTED" if req.waitlisted else req.assigned_time
    print(f"Customer: {req.customer_id} | Preferred: {req.preferred_time} | Assigned: {status} | Incentive: {'✔' if req.incentive_awarded else '✘'} (${req.incentive_value:.2f})")

# compare summaries
fifo_waitlisted = sum(r.waitlisted for r in requests_fifo)
smart_waitlisted = sum(r.waitlisted for r in requests_smart)
smart_incentives = sum(r.incentive_awarded for r in requests_smart)

print("\n--- Comparison Summary ---")
print(f"FIFO Waitlisted: {fifo_waitlisted} | Runtime: {end_fifo - start_fifo:.6f} s")
print(f"SmartSlot Waitlisted: {smart_waitlisted} | Runtime: {end_smart - start_smart:.6f} s")
print(f"SmartSlot Incentives Given: {smart_incentives}")

# visualize smartslot slot utilization
slot_labels = [slot.time_range for slot in slots_smart]
slot_counts = [len(slot.assigned_requests) for slot in slots_smart]
slot_caps = [slot.max_capacity for slot in slots_smart]

plt.figure(figsize=(8, 4))
plt.bar(slot_labels, slot_counts, label="SmartSlot Assigned")
plt.plot(slot_labels, slot_caps, color="red", linestyle="--", label="Max Capacity")
plt.title("SmartSlot Slot Utilization")
plt.xlabel("Time Slot")
plt.ylabel("Number of Assigned Requests")
plt.legend()
plt.show()
