import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

from qdrant_client import QdrantClient, models
from app.config import settings

apply_changes = "--apply" in sys.argv

# Read the expected chunks saved by your latest ingestion.
expected = Counter()

for path in Path("processed_data/true").glob("*.json"):
    data = json.loads(path.read_text(encoding="utf-8"))

    if data["source_type"] != "true":
        raise RuntimeError(f"Unexpected source type in {path}")

    for chunk in data["chunks"]:
        expected[("true", data["filename"], chunk)] += 1

if not expected:
    raise RuntimeError("No saved chunks found in processed_data/true.")

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

stored = defaultdict(list)
offset = None

try:
    while True:
        points, offset = client.scroll(
            collection_name=settings.QDRANT_COLLECTION,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        for point in points:
            payload = point.payload or {}

            # Leave other source types untouched.
            if payload.get("source_type") != "true":
                continue

            key = (
                payload["source_type"],
                payload.get("source"),
                payload.get("text"),
            )
            stored[key].append(point.id)

        if offset is None:
            break

    # Stop if stored data differs from the saved ingestion.
    unknown = set(stored) - set(expected)
    missing = [
        key for key, count in expected.items()
        if len(stored.get(key, [])) < count
    ]

    if unknown or missing:
        raise RuntimeError(
            "Stored data differs from processed_data/true. "
            "Nothing deleted. Share this error before continuing."
        )

    delete_ids = []

    for key, ids in stored.items():
        # Preserve the number of occurrences in the saved document.
        ids = sorted(ids, key=str)
        delete_ids.extend(ids[expected[key]:])

    print(f"Expected true-data points: {sum(expected.values())}")
    print(f"Stored true-data points: {sum(map(len, stored.values()))}")
    print(f"Extra points to remove: {len(delete_ids)}")

    if apply_changes and delete_ids:
        for start in range(0, len(delete_ids), 100):
            client.delete(
                collection_name=settings.QDRANT_COLLECTION,
                points_selector=models.PointIdsList(
                    points=delete_ids[start:start + 100]
                ),
                wait=True,
            )

        print("Cleanup completed. Kept the existing embeddings.")
    elif apply_changes:
        print("No extra points to remove.")
    else:
        print("Preview only. Nothing deleted.")

finally:
    client.close()