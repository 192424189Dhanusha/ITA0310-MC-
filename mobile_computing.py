"""
MOBILE COMPUTING ASSIGNMENT - EXECUTABLE PROGRAM
Four simulations:
1. Adaptive Handover in Cellular Networks
2. Mobile Data Optimization
3. Energy-Aware Task Scheduling
4. Mobile IP Packet Delivery and Network Switching

Run:
    python mobile_computing.py

This is an educational simulation. Replace the sample values with values
from your own test cases when demonstrating the program.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple


# ----------------------------- QUESTION 1 -----------------------------

def adaptive_handover():
    print("\nQUESTION 1: ADAPTIVE HANDOVER")
    print("Enter signal strengths in dBm. Type 'x' if a neighbour is unavailable.")
    serving = float(input("Serving base-station signal: "))
    n1_raw = input("Neighbour 1 signal: ").strip().lower()
    n2_raw = input("Neighbour 2 signal: ").strip().lower()
    n1 = None if n1_raw == "x" else float(n1_raw)
    n2 = None if n2_raw == "x" else float(n2_raw)

    # The prompt describes a sequence of measurements every 2 seconds.
    # Collect three samples so normal handover can be tested.
    samples = [(serving, n1, n2)]
    for i in range(2, 4):
        print(f"\nMeasurement {i} (2 seconds after previous measurement)")
        s = float(input("Serving signal: "))
        a_raw = input("Neighbour 1 signal (or x): ").strip().lower()
        b_raw = input("Neighbour 2 signal (or x): ").strip().lower()
        a = None if a_raw == "x" else float(a_raw)
        b = None if b_raw == "x" else float(b_raw)
        samples.append((s, a, b))

    counts = [0, 0]
    serving_cell = "SERVING_CELL"
    decision = "NO HANDOVER"

    for index, (s, a, b) in enumerate(samples, start=1):
        neighbours = [a, b]
        print(f"\nSample {index}: Serving={s} dBm, N1={a}, N2={b}")

        if s < -100:
            available = [(value, f"NEIGHBOUR_{i+1}")
                         for i, value in enumerate(neighbours) if value is not None]
            if not available:
                decision = "EMERGENCY: no neighbour available; start link recovery"
                print(decision)
                break
            target = max(available, key=lambda item: item[0])[1]
            decision = f"EMERGENCY HANDOVER to {target}"
            print(decision)
            counts = [0, 0]
            break

        for i, value in enumerate(neighbours):
            if value is not None and value - s >= 8:
                counts[i] += 1
            else:
                counts[i] = 0

        print(f"Consecutive qualifying counts: N1={counts[0]}, N2={counts[1]}")
        qualified = [i for i, count in enumerate(counts) if count >= 3]
        if qualified:
            available_qualified = [(neighbours[i], i) for i in qualified
                                   if neighbours[i] is not None]
            best_index = max(available_qualified)[1]
            decision = f"NORMAL HANDOVER to NEIGHBOUR_{best_index + 1}"
            print(decision)
            break
    else:
        print("No handover: no neighbour met the normal condition for 3 consecutive samples.")

    print("Final decision:", decision)


# ----------------------------- QUESTION 2 -----------------------------

@dataclass
class Resource:
    resource_id: str
    size_mb: float
    priority: int
    energy: float
    wifi_only: bool
    essential: bool = False


def sample_resources():
    # Demonstration data only; change these values for your own scenario.
    return [
        Resource("R1-SecurityPatch", 4, 10, 1.5, False, True),
        Resource("R2-Configuration", 1, 9, 0.4, False, True),
        Resource("R3-MapPackage", 6, 8, 1.8, True, False),
        Resource("R4-MediaPack", 9, 2, 2.5, False, False),
        Resource("R5-AppUpdate", 3, 7, 1.0, False, False),
        Resource("R6-LanguagePack", 2, 5, 0.8, True, False),
        Resource("R7-Database", 5, 8, 1.4, False, True),
        Resource("R8-Theme", 2, 1, 0.5, False, False),
        Resource("R9-Accessibility", 1, 9, 0.3, False, True),
        Resource("R10-OfflineContent", 7, 4, 2.0, True, False),
        Resource("R11-BugFix", 2, 8, 0.7, False, True),
        Resource("R12-OptionalAssets", 4, 3, 1.2, False, False),
    ]


def optimize_mobile_data():
    print("\nQUESTION 2: MOBILE DATA OPTIMIZATION")
    network = input("Network type (mobile/wifi): ").strip().lower()
    if network not in ("mobile", "wifi"):
        print("Unknown network type. Downloads cancelled.")
        return

    energy_limit = float(input("Maximum energy consumption allowed (units): "))
    resources = sample_resources()
    data_limit = 20.0 if network == "mobile" else float("inf")
    if network == "mobile":
        remaining = float(input("Remaining mobile data in MB (maximum 20): "))
        data_limit = min(20.0, max(0.0, remaining))

    eligible = []
    deferred: List[Tuple[Resource, str]] = []
    for r in resources:
        if network == "mobile" and r.wifi_only:
            deferred.append((r, "Wi-Fi-only restriction"))
        else:
            eligible.append(r)

    eligible.sort(key=lambda r: (not r.essential, -r.priority, r.size_mb, r.resource_id))

    selected = []
    used_mb = 0.0
    used_energy = 0.0
    for r in eligible:
        if used_mb + r.size_mb > data_limit:
            deferred.append((r, "Insufficient data allowance"))
        elif used_energy + r.energy > energy_limit:
            deferred.append((r, "Battery/energy threshold"))
        else:
            selected.append(r)
            used_mb += r.size_mb
            used_energy += r.energy

    print("\nDownload order:")
    if selected:
        for r in selected:
            print(f"  {r.resource_id}: {r.size_mb} MB, priority {r.priority}, energy {r.energy}")
    else:
        print("  No resources selected.")
    print(f"Total data selected: {used_mb:.2f} MB")
    print(f"Total energy estimate: {used_energy:.2f} units")
    print("\nDeferred resources:")
    for r, reason in deferred:
        print(f"  {r.resource_id}: {reason}")
    if network == "wifi":
        print("\nWi-Fi mode: Wi-Fi-only resources were eligible; mobile-data cap was not applied.")
    else:
        print("\nMobile mode: Wi-Fi-only resources were excluded and the 20 MB cap was enforced.")


# ----------------------------- QUESTION 3 -----------------------------

@dataclass
class Task:
    task_id: str
    execution_time: float
    energy: float
    deadline: float
    critical: bool
    priority: int


def sample_tasks():
    # Demonstration data only; times are minutes from the current time.
    return [
        Task("T1-CriticalSync", 8, 5.0, 18, True, 10),
        Task("T2-Backup", 12, 2.0, 30, False, 4),
        Task("T3-SafetyAlert", 5, 2.5, 10, True, 9),
        Task("T4-Indexing", 10, 1.5, 16, False, 5),
        Task("T5-CriticalUpload", 6, 4.0, 14, True, 8),
    ]


def schedule_tasks():
    print("\nQUESTION 3: ENERGY-AWARE TASK SCHEDULING")
    battery = float(input("Current battery percentage (example 18): "))
    energy_budget = float(input("Available background energy budget (units): "))
    now = 0.0
    tasks = sample_tasks()
    low_battery = battery < 20.0

    ready, postponed, rejected, infeasible = [], [], [], []
    for t in tasks:
        if t.execution_time <= 0 or t.energy < 0:
            rejected.append((t, "Invalid task parameters"))
            continue
        slack = t.deadline - now - t.execution_time
        if t.deadline <= now:
            (infeasible if t.critical else rejected).append(
                (t, "Deadline already passed"))
        elif low_battery and not t.critical:
            postponed.append((t, "Non-critical task postponed below 20% battery"))
        elif slack < 0:
            (infeasible if t.critical else postponed).append(
                (t, "Cannot finish before deadline"))
        else:
            ready.append((t, slack))

    # Critical first; within each class use earliest deadline, then least slack,
    # then lower energy and higher priority.
    ready.sort(key=lambda item: (not item[0].critical, item[0].deadline,
                                 item[1], item[0].energy, -item[0].priority))

    executed = []
    elapsed = now
    for t, _ in ready:
        if t.energy <= energy_budget and elapsed + t.execution_time <= t.deadline:
            executed.append(t)
            energy_budget -= t.energy
            elapsed += t.execution_time
        elif t.critical:
            infeasible.append((t, "Insufficient energy or deadline feasibility"))
        else:
            postponed.append((t, "Insufficient energy or time"))

    print("\nExecution order:")
    for t in executed:
        print(f"  EXECUTE {t.task_id} | time={t.execution_time} min | energy={t.energy} | deadline={t.deadline}")
    if not executed:
        print("  No task can be executed within the current constraints.")
    print("\nPostponed:")
    for t, reason in postponed:
        print(f"  {t.task_id}: {reason}")
    print("\nRejected:")
    for t, reason in rejected:
        print(f"  {t.task_id}: {reason}")
    print("\nCritical tasks that cannot currently be guaranteed:")
    for t, reason in infeasible:
        print(f"  {t.task_id}: {reason}")
    print(f"\nRemaining energy budget: {energy_budget:.2f} units")
    if low_battery:
        print("Low-battery mode ACTIVE (<20%): non-critical background tasks are deferred.")


# ----------------------------- QUESTION 4 -----------------------------

@dataclass
class Network:
    name: str
    latency_ms: float
    loss_percent: float


def packet_delivery_and_switching():
    print("\nQUESTION 4: MOBILE IP PACKET DELIVERY AND NETWORK SWITCHING")
    networks = []
    for name in ("Home", "Foreign-1", "Foreign-2"):
        latency = float(input(f"{name} latency in ms: "))
        loss = float(input(f"{name} packet loss in percent: "))
        networks.append(Network(name, latency, loss))

    max_latency = float(input("Maximum acceptable latency (ms): "))
    max_loss = float(input("Maximum acceptable packet loss (%): "))
    min_improvement = float(input("Minimum quality-score improvement to switch: "))
    current_name = input("Current network name (Home/Foreign-1/Foreign-2): ").strip()
    current = next((n for n in networks if n.name.lower() == current_name.lower()), networks[0])

    print("\nEnter packet sequence numbers in arrival order, separated by spaces.")
    raw = input("Sequence numbers (example: 1 2 4 4 3 6): ").strip()
    seqs = [int(x) for x in raw.split()] if raw else []
    expected = seqs[0] if seqs else 1
    seen = set()
    missing = set()
    duplicates = []
    out_of_order = []

    for seq in seqs:
        if seq in seen:
            duplicates.append(seq)
            continue
        seen.add(seq)
        if seq > expected:
            out_of_order.append(seq)
            for missing_seq in range(expected, seq):
                if missing_seq not in seen:
                    missing.add(missing_seq)
        elif seq < expected:
            out_of_order.append(seq)
        while expected in seen:
            expected += 1

    print("\nPacket analysis:")
    print("  Duplicate sequence numbers:", duplicates if duplicates else "None")
    print("  Out-of-order arrivals:", out_of_order if out_of_order else "None")
    print("  Missing sequence numbers observed:", sorted(missing) if missing else "None")
    print("  Note: a gap is provisional until a reorder timeout expires.")

    eligible = [n for n in networks
                if n.latency_ms <= max_latency and n.loss_percent <= max_loss]
    # A simple combined score; lower is better. The weights are configurable
    # educational assumptions, with loss expressed in percentage points.
    def score(n):
        return n.latency_ms + 10.0 * n.loss_percent

    if not eligible:
        print("\nNo network meets both quality limits. Keep current network temporarily and monitor.")
        return

    best = min(eligible, key=score)
    if best.name != current.name and score(current) - score(best) >= min_improvement:
        print(f"\nSWITCH RECOMMENDED: {current.name} -> {best.name}")
        print("In a real Mobile IP implementation, update the binding/tunnel and buffer packets briefly.")
    else:
        print(f"\nNO SWITCH: remain on {current.name}.")
        print("The alternative does not meet the improvement margin, or the current network is best.")
    print("Eligible networks:", ", ".join(n.name for n in eligible))


# ----------------------------- MAIN MENU -----------------------------

def main():
    while True:
        print("\n" + "=" * 62)
        print("          MOBILE COMPUTING - FOUR ALGORITHM DEMOS")
        print("=" * 62)
        print("1. Adaptive Handover")
        print("2. Mobile Data Optimization")
        print("3. Energy-Aware Task Scheduling")
        print("4. Mobile IP Packet Delivery and Network Switching")
        print("5. Run all questions")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            adaptive_handover()
        elif choice == "2":
            optimize_mobile_data()
        elif choice == "3":
            schedule_tasks()
        elif choice == "4":
            packet_delivery_and_switching()
        elif choice == "5":
            adaptive_handover()
            optimize_mobile_data()
            schedule_tasks()
            packet_delivery_and_switching()
        elif choice == "0":
            print("Program closed.")
            break
        else:
            print("Invalid choice. Enter 0, 1, 2, 3, 4 or 5.")


if __name__ == "__main__":
    main()
