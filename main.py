from pathlib import Path
from trackers.mind import DaylioTracker, OldDataException
from trackers import flatten_json
import orjson


def main():
    print("Starting ETL...")
    backup_dir = Path(r"C:\Users\roder\OneDrive\ToolData\DaylioData")
    tracker = DaylioTracker(backup_path=backup_dir)
    try:
        tracker.get_data().ingest_data()
    except OldDataException as e:
        print(f"{e}")
    except FileNotFoundError as e:
        print(f"{e}")
    finally:
        print("Finished.")

    print("Flattening Json...")
    daylio_json_path = Path("data/ingested/daylio.json")
    flattened_path = Path("data/flat_daylio.json")
    json = orjson.loads(daylio_json_path.read_bytes())

    flattened_json = flatten_json(json, max_depth=4)  # not working

    with flattened_path.open("wb") as f:
        f.write(orjson.dumps(flattened_json, option=orjson.OPT_INDENT_2))

    print("Finished.")


if __name__ == "__main__":
    main()
