from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import List, Optional


@dataclass
class Subscription:
    name: str
    monthly_cost: float
    next_billing: date


class SubscriptionTracker:
    def __init__(self, storage_path: str = "subscriptions.json"):
        self.storage_path = Path(storage_path)
        self.subscriptions: List[Subscription] = []
        self._load()

    def _load(self) -> None:
        if self.storage_path.exists():
            data = json.loads(self.storage_path.read_text())
            self.subscriptions = [
                Subscription(
                    name=item["name"],
                    monthly_cost=item["monthly_cost"],
                    next_billing=date.fromisoformat(item["next_billing"]),
                )
                for item in data
            ]

    def _save(self) -> None:
        data = [asdict(sub) for sub in self.subscriptions]
        # convert date objects to ISO strings
        for d in data:
            d["next_billing"] = d["next_billing"].isoformat()
        self.storage_path.write_text(json.dumps(data, indent=2))

    def add_subscription(self, sub: Subscription) -> None:
        self.subscriptions.append(sub)
        self._save()

    def remove_subscription(self, name: str) -> bool:
        for i, sub in enumerate(self.subscriptions):
            if sub.name == name:
                del self.subscriptions[i]
                self._save()
                return True
        return False

    def update_subscription(
        self, name: str, monthly_cost: Optional[float] = None, next_billing: Optional[date] = None
    ) -> bool:
        for sub in self.subscriptions:
            if sub.name == name:
                if monthly_cost is not None:
                    sub.monthly_cost = monthly_cost
                if next_billing is not None:
                    sub.next_billing = next_billing
                self._save()
                return True
        return False

    def list_subscriptions(self) -> List[Subscription]:
        return list(self.subscriptions)

    def monthly_total(self) -> float:
        return sum(sub.monthly_cost for sub in self.subscriptions)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Subscription tracking service")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a subscription")
    add_parser.add_argument("name")
    add_parser.add_argument("cost", type=float)
    add_parser.add_argument("next_billing")

    remove_parser = subparsers.add_parser("remove", help="Remove a subscription")
    remove_parser.add_argument("name")

    subparsers.add_parser("list", help="List all subscriptions")
    subparsers.add_parser("total", help="Show monthly total cost")

    args = parser.parse_args()
    tracker = SubscriptionTracker()

    if args.command == "add":
        billing_date = date.fromisoformat(args.next_billing)
        tracker.add_subscription(
            Subscription(name=args.name, monthly_cost=args.cost, next_billing=billing_date)
        )
    elif args.command == "remove":
        if not tracker.remove_subscription(args.name):
            print(f"Subscription {args.name} not found")
    elif args.command == "list":
        for sub in tracker.list_subscriptions():
            print(f"{sub.name} - £{sub.monthly_cost:.2f} - Next: {sub.next_billing}")
    elif args.command == "total":
        print(f"Total monthly cost: £{tracker.monthly_total():.2f}")
    else:
        parser.print_help()
