from indeed import get_indeed_jobs
from so import get_so_jobs

indeed_jobs = get_indeed_jobs()
so_jobs = get_so_jobs()

jobs = so_jobs + indeed_jobs

print(jobs)