from notifications.digest import daily_digest_volunteer, weekly_digest_volunteer
from datetime import datetime, timedelta
import django_rq
import os


VOLUNTEER_DIGEST_HOUR = int(os.getenv("VOLUNTEER_DIGEST_HOUR", "9"))
VOLUNTEER_DIGEST_MINUTE = int(os.getenv("VOLUNTEER_DIGEST_MINUTE", "0"))

VOLUNTEER_DIGEST_WEEKLY_DAY = int(os.getenv("VOLUNTEER_DIGEST_WEEKLY_DAY", "6"))
VOLUNTEER_DIGEST_WEEKLY_HOUR = int(os.getenv("VOLUNTEER_DIGEST_WEEKLY_HOUR", "19"))
VOLUNTEER_DIGEST_WEEKLY_MINUTE = int(os.getenv("VOLUNTEER_DIGEST_WEEKLY_MINUTE", "0"))


def setup():
    """Initialises our scheduled jobs.
    If the scheduled time changes, these values will be updated accordingly.
    """
    # Get the scheduler and existing scheduled jobs.
    scheduler = django_rq.get_scheduler('default')

    # 1. Daily digest emails for volunteers.
    schedule(scheduler,
        VOLUNTEER_DIGEST_HOUR, 
        VOLUNTEER_DIGEST_MINUTE,
        daily_digest_volunteer)

    #2. Weekly digest email for volunteers.
    schedule_weekly(scheduler, VOLUNTEER_DIGEST_WEEKLY_DAY,
                    VOLUNTEER_DIGEST_WEEKLY_HOUR,
                    VOLUNTEER_DIGEST_WEEKLY_MINUTE,
                    weekly_digest_volunteer)

def schedule_weekly(scheduler, day, hour, minute, function):
    # Define time to schedule the next weekly job

    now = datetime.now()

    #days until the next weekly send date
    days = (day - now.weekday()) % 7

    scheduled_time = datetime(hour=hour, minute=minute,
                              year=now.year, month=now.month, day=now.day)
    if days > 0:
        # happening in future
        scheduled_time = scheduled_time + timedelta(days=days)
    elif scheduled_time <= now: # today is scheduled day and time has already passed
        scheduled_time = scheduled_time + timedelta(days=7)

    # Check if the job has been created yet.
    job = get_job_for_function(scheduler, function)
    if job:
        # Always recreate jobs so the scheduled time is updated.
        scheduler.cancel(job)

    # Schedule a new job.
    scheduler.schedule(
        scheduled_time=scheduled_time,
        func=function,
        interval=86400 * 7,
        repeat=None # repeat forever
    )






def schedule(scheduler, hour, minute, function):
    """Schedules functions to run daily at a specific time.
    This function is idempotent, it can be ran many times.
    """
    # Define the time to send the first email.


    now = datetime.now()
    scheduled_time = datetime(
        hour=hour, minute=minute, 
        year=now.year, 
        month=now.month, 
        day=now.day)

    # Ensure the scheduled time is in the future.
    # This wont be the case if scheduled_time's hour
    # and minute have already passed today.
    if scheduled_time < now:
        scheduled_time = scheduled_time + timedelta(days=1)

    # Check if the job has been created yet.
    job = get_job_for_function(scheduler, function)
    if job:

        # Always recreate jobs so the scheduled time is updated.
        scheduler.cancel(job)

    # Schedule a new job.
    scheduler.schedule(
        scheduled_time=scheduled_time,
        func=function,
        interval=86400,
        repeat=None # repeat forever
    )

def get_job_for_function(scheduler, function):
    """Returns a job for a given function, if it exists."""
    func_name = fqdn(function)
    for job in scheduler.get_jobs():
        if job.func_name == func_name:
            return job

def job_exists(scheduler, function):
    """Checks if a job exists for a given function."""
    jobs = scheduler.get_jobs()
    return fqdn(function) in map(lambda job: job.func_name, jobs)

def fqdn(function):
    """Returns the FQDN for a function."""
    return ".".join([function.__module__, function.__name__])
