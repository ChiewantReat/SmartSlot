# SmartSlot

## Overview

SmartSlot is a simple greedy scheduling algorithm designed to optimize grocery store pickup services. Unlike static or FIFO-based slot assignment, SmartSlot dynamically assigns each customer request to the best available time slot based on a scoring system that balances customer preference, current slot capacity, and flexibility. Flexible customers may receive small incentives to shift to underused slots, reducing congestion during peak times.

## How It Works

- Each request is scored for all available time slots.
- The score factors in:
  - Whether the slot matches the customer’s preferred time.
  - How full the slot already is.
  - Whether the customer is flexible.
- The slot with the lowest score is chosen.
- Flexible customers may get an incentive if shifted.
- If no slots are available, the request is waitlisted.
- SmartSlot is compared to a FIFO baseline.

## Requirements

- Python
- `matplotlib` for chart visualization

Install dependencies:
```bash
pip install matplotlib
