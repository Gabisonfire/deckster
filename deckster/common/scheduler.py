from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()
sched.start()

def add_job(job, interval):
    sched.add_job(job, 'interval', seconds=interval)
    
def stop_jobs():
    sched.shutdown()