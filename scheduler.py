import time
import schedule

from main import main
from src.reporting.logger import setup_logger


# ============================================================
# CONFIGURATION
# ============================================================

REPORT_TIME = "18:00"

logger = setup_logger()


# ============================================================
# RUN REPORTING SYSTEM
# ============================================================

def run_reporting_system():
    """
    Run the complete automated reporting pipeline.
    """

    logger.info("=" * 60)
    logger.info("STARTING SCHEDULED REPORT")
    logger.info("=" * 60)

    try:

        main()

        logger.info("=" * 60)
        logger.info("SCHEDULED REPORT COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

    except Exception as error:

        logger.exception(
            "SCHEDULED REPORT FAILED: %s",
            error
        )

        logger.info("=" * 60)


# ============================================================
# SCHEDULE REPORT
# ============================================================

schedule.every().day.at(REPORT_TIME).do(
    run_reporting_system
)


# ============================================================
# START SCHEDULER
# ============================================================

logger.info("=" * 60)
logger.info("AUTOMATED REPORTING SCHEDULER")
logger.info("=" * 60)

logger.info(
    "Scheduler is running."
)

logger.info(
    "Report time: %s every day",
    REPORT_TIME
)

logger.info(
    "Press CTRL+C to stop the scheduler."
)


# ============================================================
# SCHEDULER LOOP
# ============================================================

while True:

    try:

        schedule.run_pending()

        time.sleep(1)

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