# git_test

## Subscription Tracking Service

This repository includes a simple Python script, `subscription_tracker.py`, for tracking recurring subscriptions. The script stores data in `subscriptions.json` and provides a small CLI to add, remove, list and total subscriptions.

### Usage

Add a subscription:

```bash
python3 subscription_tracker.py add "Netflix" 10.99 2023-12-01
```

Remove a subscription:

```bash
python3 subscription_tracker.py remove "Netflix"
```

List current subscriptions:

```bash
python3 subscription_tracker.py list
```

Show total monthly cost:

```bash
python3 subscription_tracker.py total
```
