import argparse
import os
from pathlib import Path

from intelligence.airline_collectors import AirIndiaCollector, EaseMyTripCollector, IndigoCollector, SkyscannerCollector
from intelligence.data import load_cpi_airfare_weight, load_weights
from intelligence.models import Weights
from intelligence.pipeline import collect_and_calculate
from intelligence.storage import IntelligenceRepository
from intelligence.mysql_storage import create_mysql_repositories


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect permitted airline fares and calculate AeroIndex intelligence")
    parser.add_argument("--origin", default="DEL")
    parser.add_argument("--destination", default="BOM")
    parser.add_argument("--travel-date", required=True, help="ISO date, for example 2026-09-15")
    parser.add_argument("--period", choices=("base", "current"), default="current")
    parser.add_argument("--source", choices=("airlines", "skyscanner", "easemytrip"), default="skyscanner")
    parser.add_argument("--windows", default="1,7,15,30,45")
    parser.add_argument("--weights", type=Path, help="Authoritative route weights CSV")
    parser.add_argument("--cpi-airfare-file", type=Path, help="Official CPI Airfare item-weight CSV")
    parser.add_argument("--cpi-sector", default="Rural", choices=("Rural", "Urban", "Combined"))
    parser.add_argument("--source-db", type=Path, default=Path("data/source.db"))
    parser.add_argument("--result-db", type=Path, default=Path("data/results.db"))
    parser.add_argument("--backend", choices=("sqlite", "mysql"), default="sqlite")
    parser.add_argument("--mysql-host", default="127.0.0.1")
    parser.add_argument("--mysql-port", type=int, default=3306)
    parser.add_argument("--mysql-user", default="root")
    parser.add_argument("--airindia-fare-selector")
    parser.add_argument("--indigo-fare-selector")
    parser.add_argument("--skyscanner-fare-selector", default='[data-backpack-ds-component="Text"]')
    parser.add_argument("--easemytrip-fare-selector", default=".value")
    parser.add_argument("--headed", action="store_true", help="Show the browser while collecting")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    windows = [int(value.strip()) for value in args.windows.split(",")]
    if args.backend == "mysql":
        source, results = create_mysql_repositories(args.mysql_host, args.mysql_port, args.mysql_user, os.getenv("MYSQL_PASSWORD"))
    else:
        source = IntelligenceRepository(args.source_db)
        results = IntelligenceRepository(args.result_db)
    if args.weights and args.weights.exists():
        route_weights = load_weights(args.weights)
    else:
        route_weights = Weights(route_weights={})
    if args.cpi_airfare_file and args.cpi_airfare_file.exists():
        cpi_weight = load_cpi_airfare_weight(args.cpi_airfare_file, sector=args.cpi_sector)
        route_weights = Weights(route_weights.route_weights, route_weights.window_weights, cpi_weight.airfare_weight, route_weights.route_weight_metadata, route_weights.window_weight_metadata, cpi_weight.airfare_weight_metadata)
    source.save_weights(route_weights)

    collectors = []
    for window in windows:
        if args.source == "skyscanner":
            collectors.append(SkyscannerCollector(args.origin, args.destination, args.travel_date, args.period, window, args.skyscanner_fare_selector, not args.headed))
        elif args.source == "easemytrip":
            collectors.append(EaseMyTripCollector(args.origin, args.destination, args.travel_date, args.period, window, args.easemytrip_fare_selector, not args.headed))
        else:
            if not args.airindia_fare_selector or not args.indigo_fare_selector:
                raise SystemExit("--airindia-fare-selector and --indigo-fare-selector are required with --source airlines")
            collectors.extend((
                AirIndiaCollector(args.origin, args.destination, args.travel_date, args.period, window, args.airindia_fare_selector, not args.headed),
                IndigoCollector(args.origin, args.destination, args.travel_date, args.period, window, args.indigo_fare_selector, not args.headed),
            ))
    try:
        report = collect_and_calculate(source, results, collectors)
    except (RuntimeError, ValueError) as error:
        print(f"Collection blocked: {error}")
        return
    finally:
        source.close()
        results.close()
    if report["apix"] is None:
        print(f"Calculation blocked: {report.get('weighting_status', 'missing input')}")
    else:
        print(f"APIx: {report['apix']:.4f}")
    print(f"Saved source data to {args.source_db}")
    print(f"Saved result report to {args.result_db}")


if __name__ == "__main__":
    main()