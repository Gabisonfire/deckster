from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(timezone="America/New_York")
sched.start()

def add_job(job, interval, id, paused = False):
    if paused:
        sched.add_job(job, 'interval', seconds=interval, next_run_time=None, id=id)
    else:
        sched.add_job(job, 'interval', seconds=interval, id=id)

def stop_jobs():
    sched.shutdown()

def toggle_job(id, state):
    if state:
        sched.resume_job(id)
    else:
        sched.pause_job(id)
