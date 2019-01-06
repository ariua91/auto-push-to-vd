## AT 23,03:47 & 0,1:45 Check the correct time range - are there any ASSIGNED tasks?

## if so, login to VF and push to VD

### I need to call
#### PUT https://api-staging.versafleet.co/tasks/submit_all
#### json= {"date":"2019-01-06"}


from datetime import datetime, timedelta
import requests
from secret_keys import ENV, CLIENT_ID, CLIENT_SECRET



LOGFN = 'logs/' + datetime.strftime(datetime.utcnow() + timedelta(hours=8),
                                    '%y-%U-logs.txt')
VERBOSE = True

def write_to_log(logfn, logtext):
    with open(logfn, 'a') as f:
        f.write(datetime.strftime(
            datetime.utcnow() + timedelta(hours=8),
            '%y-%m-%dT%H:%M:%S+08:00 | '
        ))
        f.write(logtext + '\n')


def get_times(tzoffset):
    '''
    Given a tzoffset int in hours (6hours for this client)
    return a FROM time object & TO time object

    KNOWN BUGS: Negative Time Zones
    '''
    current_dt = datetime.utcnow() + timedelta(hours=tzoffset) - timedelta(days=2)
    return (datetime.strftime(current_dt,
                              '%Y-%m-%dT{:02d}:00:00+08:00'.format(tzoffset)),
            datetime.strftime(current_dt + timedelta(days=1),
                              '%Y-%m-%dT{:02d}:59:59+08:00'.format(tzoffset - 1)))


def get_num_tasks(varibales, time_from, time_to, per_pg, archived):
    '''
    Get all tasks
    '''
    env, c_id, c_secret = variables['env'], variables['c_id'], variables['c_secret']
    pg = 1
    acted_on, total_tasks = 0, 999999999
    while acted_on < total_tasks:
        tmp = requests.get(
            "https://{!s}.versafleet.co/api/tasks?"
            "client_id={!s}&client_secret={!s}"
            "&page={!s}&per_page={!s}"
            "&state=assigned"
            "&from_datetime={!s}&to_datetime={!s}&archived={!s}".format(
                env,
                c_id,
                c_secret,
                pg,
                per_pg,
                time_from,
                time_to,
                archived
            )
        )
        acted_on += len(tmp.json()['tasks'])
        total_tasks = tmp.json()['meta']['total']
        pg += 1
        if VERBOSE:
            print "GOT {!s} / {!s} tasks".format(acted_on, total_tasks)
            print tmp
    return acted_on







variables = {
    'env': ENV,
    'c_id': CLIENT_ID,
    'c_secret': CLIENT_SECRET
}
time_from, time_to = get_times(2)
task_cnt = get_num_tasks(variables, time_from, time_to, 20, 0)

if task_cnt > 0:
    print task_cnt
