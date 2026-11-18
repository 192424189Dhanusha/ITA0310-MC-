# Mobile Computing Assignment – Four Algorithm Demonstrations

This repository contains a beginner-friendly Python command-line program for the four Mobile Computing assignment questions.

## Requirements
- Python 3.9 or newer
- No external Python packages are required

## Run the program (Windows)
1. Download or clone this repository.
2. Open Command Prompt in the project folder.
3. Run:

```bash
python mobile_computing.py
```

If `python` is not recognised, try:

```bash
py mobile_computing.py
```

## Menu
- 1: Adaptive Handover
- 2: Mobile Data Optimization
- 3: Energy-Aware Task Scheduling
- 4: Mobile IP Packet Delivery and Network Switching
- 5: Run all four demonstrations
- 0: Exit

## Important notes
- The assignment statement does not provide the actual 12 resource sizes/priorities/energy costs, the five task values, or exact network-quality thresholds. The program therefore uses clearly labelled sample values for Questions 2 and 3, and asks the user to enter network measurements and thresholds for Questions 1 and 4.
- Change the sample records in `sample_resources()` and `sample_tasks()` to match values supplied by your lecturer, if any.
- The packet-loss and latency score in Question 4 is an educational example: `latency_ms + 10 * loss_percent`. Tune the weight and thresholds to the application's requirements.
- This is a simulation of the decision logic, not a real cellular modem, Mobile IP tunnel, or operating-system scheduler.

## Assignment rubric mapping
Each question's algorithm is intended to demonstrate:
- Analytical decomposition
- Logical conditions and decision-making
- Pseudocode/control structures (write these separately on paper as required)
- Edge cases and justification
