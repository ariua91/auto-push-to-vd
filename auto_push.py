from datetime import datetime, timedelta
import requests

from secret_keys import ENV, CLIENT_ID, CLIENT_SECRET, COOKIE, RANDOM_TASK_ID


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

    returns:
     - FROM time object
     - TO time object
     - SUBMIT ALL DATE

    KNOWN BUGS: Negative Time Zones
    '''
    current_dt = datetime.utcnow() + timedelta(hours=tzoffset)
    return (datetime.strftime(current_dt,
                              '%Y-%m-%dT06:00:00+08:00'),
            datetime.strftime(current_dt + timedelta(days=1),
                              '%Y-%m-%dT05:59:59+08:00'),
            datetime.strftime(current_dt + timedelta(days=1),
                              '%Y-%m-%d')
    )


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


def push_vd(variables, push_date):
    'Push push_date tasks to VD'
    env, cookie = (
        variables['env'],
        variables['cookie']
    )
    tmp = requests.put(
        'https://{}.versafleet.co/tasks/submit_all'.format(env),
        json= {"date":push_date},
        headers={"cookie":cookie}
    )
    return tmp


def random_get(variables):
    'Do a random GET to refresh cookie'
    env, cookie, rand_task_id = (
        variables['env'],
        variables['cookie'],
        variables['rand_task_id']
    )
    tmp = requests.get(
        'https://{!s}.versafleet.co/tasks/{!s}'.format(env, rand_task_id),
        headers={"cookie":cookie}
    )
    return tmp





variables = {
    'env': ENV,
    'c_id': CLIENT_ID,
    'c_secret': CLIENT_SECRET,
    'cookie': COOKIE,
    'rand_task_id': RANDOM_TASK_ID
}

time_from, time_to, push_date = get_times(2)
task_cnt = get_num_tasks(variables, time_from, time_to, 20, 0)

if task_cnt > 0:
    tmp = push_vd(variables, push_date)
    if VERBOSE:
        print "SUBMIT ALL PUT"
    write_to_log(LOGFN,
                 "Num Assigned: {!s}. Made a SUBMIT ALL call. Status:{!s}".format(
                     task_cnt, tmp.status_code
                 ))
else:
    tmp = random_get(variables)
    if VERBOSE:
        print "Just a GET to refresh"
    write_to_log(LOGFN,
                 "Num Assigned: {!s}. GET to refresh. Status:{!s}".format(
                     task_cnt, tmp.status_code
                 ))
