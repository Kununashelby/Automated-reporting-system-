import time
import schedule

from main import main


# ============================================================
# CONFIGURATION
# ============================================================

REPORT_TIME = "18:00"


# ============================================================
# RUN REPORTING SYSTEM
# ============================================================

def run_reporting_system():
    """
    Run the complete automated reporting pipeline.
    """

    print("\n")
    print("========================================")
    print("STARTING SCHEDULED REPORT")
    print("========================================")

    try:

        main()

        print("\n========================================")
        print("SCHEDULED REPORT COMPLETED")
        print("========================================")

    except Exception as error:

        print("\n========================================")
        print("SCHEDULED REPORT FAILED")
        print("========================================")

        print(f"Error: {error}")


# ============================================================
# SCHEDULE REPORT
# ============================================================

schedule.every().day.at(REPORT_TIME).do(
    run_reporting_system
)


# ============================================================
# START SCHEDULER
# ============================================================

print("========================================")
print("AUTOMATED REPORTING SCHEDULER")
print("========================================")

print()
print("Scheduler is running.")
print(f"Report time: {REPORT_TIME} every day")
print("Press CTRL+C to stop the scheduler.")
print()


# ============================================================
# SCHEDULER LOOP
# ============================================================

while True:

    try:

        schedule.run_pending()

        time.sleep(1)

    except KeyboardInterrupt:

        print("\n")
        print("========================================")
        print("SCHEDULER STOPPED")
        print("========================================")

        break

    except Exception as error:

        print("\n")
        print("========================================")
        print("SCHEDULER ERROR")
        print("========================================")

        print(f"Error: {error}")

        print("\nScheduler will continue running...")

        time.sleep(5)