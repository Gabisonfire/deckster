import logging
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger("deckster")

sched = BackgroundScheduler(timezone="America/New_York")
logger.debug("Sarting scheduler")
sched.start()

def add_job(job, interval, id, paused = False, args = []):
    logger.info(f"Adding job {id} as '{'paused' if paused else 'started'}'")
    if paused:
        sched.add_job(job, 'interval', seconds=interval, next_run_time=None, id=id, args=args)
    else:
        sched.add_job(job, 'interval', seconds=interval, id=id, args=args)

def stop_jobs():
    sched.remove_all_jobs()
    sched.shutdown()

def clear_jobs():
    sched.remove_all_jobs()

def toggle_job(id, state):
    logger.info(f"Setting job {id} to '{'resumed' if state else 'paused'}'")
    if state:
        sched.resume_job(id)
    else:
        sched.pause_job(id)
