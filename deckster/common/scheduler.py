import logging
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger("deckster")

sched = BackgroundScheduler(timezone="America/New_York")
logger.debug("Sarting scheduler")
sched.start()

def add_job(job, interval, id, paused = False, args = []):
    """Adds a job to the scheduler

    Args:
        job (func): A function to execute
        interval (integer): The interval, in seconds
        id (string): An id to assign the job for retrieval
        paused (bool, optional): Start as paused. Defaults to False.
        args (list, optional): A list of arguments to pass to the function. Defaults to [].
    """
    logger.info(f"Adding job {id} as '{'paused' if paused else 'started'}'")
    if paused:
        sched.add_job(job, 'interval', seconds=interval, next_run_time=None, id=id, args=args)
    else:
        sched.add_job(job, 'interval', seconds=interval, id=id, args=args)

def stop_jobs():
    """Stops all jobs
    """
    sched.remove_all_jobs()
    sched.shutdown()

def clear_jobs():
    """Removes all jobs from the pool
    """
    sched.remove_all_jobs()

def toggle_job(id, state):
    """Toggles a job paused or started

    Args:
        id (string): The id of the job to toggle
        state (bool): True to resume, false to pause
    """
    logger.info(f"Setting job {id} to '{'resumed' if state else 'paused'}'")
    if state:
        sched.resume_job(id)
    else:
        sched.pause_job(id)
