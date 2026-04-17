from pathlib import Path
from trackers.mind import DaylioTracker, OldDataException


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


if __name__ == "__main__":
    main()
