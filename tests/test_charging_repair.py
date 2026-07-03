from __future__ import annotations

from evrptw.metrics import evaluate_route_metrics
from evrptw.models import Instance, Node, NodeType, Vehicle
from evrptw.repairs import insert_anticipatory_charging_stations, insert_charging_stations


def test_charging_repair_inserts_reachable_station_without_reordering_customers() -> None:
    instance = Instance(
        "repair_toy",
        (
            Node("D0", NodeType.DEPOT, 0.0, 0.0, 0.0, 0.0, 1_000.0, 0.0),
            Node("S1", NodeType.STATION, 50.0, 0.0, 0.0, 0.0, 1_000.0, 0.0),
            Node("C1", NodeType.CUSTOMER, 60.0, 0.0, 1.0, 0.0, 1_000.0, 0.0),
        ),
        Vehicle(
            battery_capacity=80.0,
            load_capacity=10.0,
            consumption_rate=1.0,
            inverse_refueling_rate=0.1,
            average_velocity=1.0,
        ),
    )
    baseline_routes = [["D0", "C1", "D0"]]
    baseline_metrics = evaluate_route_metrics(
        instance,
        baseline_routes,
        method="BASELINE",
        seed=1,
        runtime_seconds=0.0,
    )

    repair = insert_charging_stations(instance, baseline_routes)
    repaired_routes = [list(route) for route in repair.routes]
    repaired_metrics = evaluate_route_metrics(
        instance,
        repaired_routes,
        method="REPAIRED",
        seed=1,
        runtime_seconds=repair.runtime_seconds,
    )

    assert baseline_metrics.energy_violations == 1
    assert repaired_routes == [["D0", "C1", "S1", "D0"]]
    assert repaired_metrics.feasible is True
    assert repaired_metrics.energy_violations == 0
    assert repair.inserted_station_count == 1
    assert repair.unrepaired_legs == ()


def test_anticipatory_repair_inserts_before_customer_becomes_stranded() -> None:
    instance = Instance(
        "anticipatory_repair_toy",
        (
            Node("D0", NodeType.DEPOT, 0.0, 0.0, 0.0, 0.0, 1_000.0, 0.0),
            Node("S1", NodeType.STATION, 40.0, 0.0, 0.0, 0.0, 1_000.0, 0.0),
            Node("C1", NodeType.CUSTOMER, 50.0, 0.0, 1.0, 0.0, 1_000.0, 0.0),
            Node("C2", NodeType.CUSTOMER, 80.0, 0.0, 1.0, 0.0, 1_000.0, 0.0),
        ),
        Vehicle(
            battery_capacity=100.0,
            load_capacity=10.0,
            consumption_rate=1.0,
            inverse_refueling_rate=0.1,
            average_velocity=1.0,
        ),
    )
    baseline_routes = [["D0", "C1", "C2", "D0"]]

    late_repair = insert_charging_stations(instance, baseline_routes)
    late_routes = [list(route) for route in late_repair.routes]
    late_metrics = evaluate_route_metrics(
        instance,
        late_routes,
        method="LATE_REPAIR",
        seed=1,
        runtime_seconds=late_repair.runtime_seconds,
    )

    anticipatory_repair = insert_anticipatory_charging_stations(instance, baseline_routes)
    anticipatory_routes = [list(route) for route in anticipatory_repair.routes]
    anticipatory_metrics = evaluate_route_metrics(
        instance,
        anticipatory_routes,
        method="ANTICIPATORY_REPAIR",
        seed=1,
        runtime_seconds=anticipatory_repair.runtime_seconds,
    )

    assert late_metrics.energy_violations == 1
    assert late_repair.unrepaired_legs == ("route 1 C2->D0",)
    assert anticipatory_routes == [["D0", "C1", "S1", "C2", "S1", "D0"]]
    assert anticipatory_metrics.feasible is True
    assert anticipatory_metrics.energy_violations == 0
    assert anticipatory_repair.inserted_station_count == 2
    assert anticipatory_repair.unrepaired_legs == ()


def test_anticipatory_repair_records_unreachable_risk_without_reordering() -> None:
    instance = Instance(
        "anticipatory_unreachable_toy",
        (
            Node("D0", NodeType.DEPOT, 0.0, 0.0, 0.0, 0.0, 1_000.0, 0.0),
            Node("S1", NodeType.STATION, 20.0, 50.0, 0.0, 0.0, 1_000.0, 0.0),
            Node("C1", NodeType.CUSTOMER, 70.0, 0.0, 1.0, 0.0, 1_000.0, 0.0),
        ),
        Vehicle(
            battery_capacity=100.0,
            load_capacity=10.0,
            consumption_rate=1.0,
            inverse_refueling_rate=0.1,
            average_velocity=1.0,
        ),
    )
    baseline_routes = [["D0", "C1", "D0"]]

    repair = insert_anticipatory_charging_stations(instance, baseline_routes)
    repaired_routes = [list(route) for route in repair.routes]

    assert repaired_routes == baseline_routes
    assert repair.inserted_station_count == 0
    assert repair.unrepaired_legs == ("route 1 D0->C1", "route 1 C1->D0")
