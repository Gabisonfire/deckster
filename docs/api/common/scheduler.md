Module common.scheduler
=======================

Functions
---------

    
`add_job(job, interval, id, paused=False, args=[])`
:   Adds a job to the scheduler
    
    Args:
        job (func): A function to execute
        interval (integer): The interval, in seconds
        id (string): An id to assign the job for retrieval
        paused (bool, optional): Start as paused. Defaults to False.
        args (list, optional): A list of arguments to pass to the function. Defaults to [].

    
`clear_jobs()`
:   Removes all jobs from the pool

    
`stop_jobs()`
:   Stops all jobs

    
`toggle_job(id, state)`
:   Toggles a job paused or started
    
    Args:
        id (string): The id of the job to toggle
        state (bool): True to resume, false to pause