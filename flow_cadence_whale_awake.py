import requests, time

def flow_whale():
    print("Flow — Cadence Whale Awakens (> $5M FLOW moved in one tx)")
    seen = set()
    while True:
        r = requests.get("https://flowscan.org/api/transactions?limit=40&order=desc")
        for tx in r.json().get("data", []):
            h = tx["hash"]
            if h in seen: continue
            seen.add(h)

            # Pure FLOW transfer (not contract interaction)
            if tx.get("status") != "SEALED": continue
            if len(tx.get("events", [])) < 2: continue

            amount = 0.0
            for event in tx["events"]:
                if event["type"] == "FlowToken.Transferred" or "TokensWithdrawn" in event["type"]:
                    try:
                        amount += float(event["values"]["amount"])
                    except:
                        continue

            if amount >= 5_000_000:  # > 5 million FLOW (~$5M+ at times)
                print(f"CADENCE WHALE AWAKENED\n"
                      f"{amount:,.0f} FLOW moved in one breath\n"
                      f"From: {tx.get('payer', '')[:12]}...\n"
                      f"Tx: https://flowscan.org/transaction/{h}\n"
                      f"→ NBA Top Shot, Dapper Labs, or mega-whale just moved\n"
                      f"→ Flow rarely sees this size — something big is happening\n"
                      f"{'-'*80}")
        time.sleep(2.9)

if __name__ == "__main__":
    flow_whale()
