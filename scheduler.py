import time
import schedule

from main import main
from src.reporting.logger import setup_logger
from src.reporting.database import (
    create_database,
    load_settings,
)

DB_PATH = "data/reporting.db"

logger = setup_logger()


def run_reporting_system():
    logger.info("=" * 60)
    logger.info("STARTING SCHEDULED REPORT")
    logger.info("=" * 60)

    try:
        main()

        logger.info("=" * 60)
        logger.info(
            "SCHEDULED REPORT COMPLETED SUCCESSFULLY"
        )
        logger.info("=" * 60)

    except Exception as error:
        logger.exception(
            "SCHEDULED REPORT FAILED: %s",
            error
        )

        logger.info("=" * 60)


def load_report_settings():
    """
    Load the current settings from SQLite.
    """

    return load_settings(DB_PATH)


def get_report_time():
    """
    Get the currently configured report time.
    """

    settings = load_report_settings()

    return settings.get(
        "report_time",
        "18:00"
    )


def schedule_report(report_time):
    """
    Schedule the report for the specified time.
    """

    schedule.clear()

    schedule.every().day.at(
        report_time
    ).do(run_reporting_system)

    logger.info(
        "Report scheduled for %s every day.",
        report_time
    )


def check_for_setting_changes(current_time):
    """
    Check SQLite for changes to the report time.
    """

    new_time = get_report_time()

    if new_time != current_time:

        logger.info(
            "Report time changed: %s -> %s",
            current_time,
            new_time
        )

        schedule_report(new_time)

        return new_time

    return current_time


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

create_database(DB_PATH)


# --------------------------------------------------
# INITIAL SETTINGS
# --------------------------------------------------

current_report_time = get_report_time()

schedule_report(current_report_time)


logger.info("=" * 60)
logger.info("AUTOMATED REPORTING SCHEDULER")
logger.info("=" * 60)

logger.info(
    "Scheduler is running."
)

logger.info(
    "Current report time: %s",
    current_report_time
)

logger.info(
    "Settings are checked automatically."
)

logger.info(
    "Press CTRL+C to stop the scheduler."
)


# --------------------------------------------------
# SCHEDULER LOOP
# --------------------------------------------------

while True:

    try:

        schedule.run_pending()

        current_report_time = check_for_setting_changes(
            current_report_time
        )

        time.sleep(5)

    except KeyboardInterrupt:

        logger.info(
            "Scheduler stopped by user."
        )

        break

    except Exception as error:

        logger.exception(
            "Scheduler error: %s",
            error
        )

        time.sleep(5)