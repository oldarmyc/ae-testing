"""

Code adapted from https://github.com/Anaconda-Platform/ae5_controller

"""
from multiprocessing import Pool
from stress_test.cluster import AECluster


import argparse
import logging
import time


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    filename='testing.log',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def cleanup_sessions(cluster):
    sessions = cluster._get('sessions').json()
    for session in sessions:
        cluster._delete(f"sessions/{session.get('id')}")


def cleanup_projects(cluster):
    projects = cluster._get('projects').json()
    for project in projects:
        cluster._delete(f"projects/{project.get('id')}")


def create_start_helper(args):
    return create_and_start_project(*args)


def create_and_start_project(user, url):
    cluster = AECluster(url)
    cluster.login(user, user)
    create_object = {'name': f'Test project - {user}'}
    project_details = None
    try:
        create_response = cluster._post('projects', json=create_object)
        project_details = create_response.json()
    except Exception as e:
        logging.info(f'Exception on project create: {e}')
        return

    if create_response.status_code == 201:
        logging.info(
            f"Project created for {project_details.get('owner')} created."
            " Waiting to start project session"
        )
        # Wait before starting the project
    else:
        message = (
            f"{create_response.status_code}: "
            f"{project_details['error']['message']}"
        )
        logging.info(
            f"{message} - Project was not created successfully for {user}"
        )
        return

    # Having to wait to not hit API limits
    time.sleep(10)
    start_response = None
    try:
        start_response = cluster._post(
            f"projects/{project_details.get('id')}/sessions"
        )
        start_details = start_response.json()
    except Exception as e:
        logging.info(f'Exception on project start: {e}')
        return

    if start_response.status_code == 202:
        logging.info(
            f"Project {start_details.get('state')} "
            f"for {start_details.get('owner')}"
        )
    else:
        message = (
            f"{start_response.status_code}: "
            f"{start_details['error']['message']}"
        )
        logging.info(
            f'{message} - Project session could not be started for {user}'
        )

    return


def handle_arguments():
    description = ('Process to simulate usage over time for the AE5 system')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--url',
        required=True,
        help=('Specify the URL for the AE5 system to test')
    )
    parser.add_argument(
        '--username',
        required=False,
        default='anaconda-enterprise',
        help=(
            'Administrator username to login to AE5 install.'
            ' Default is anaconda-enterprise'
        )
    )
    parser.add_argument(
        '--password',
        required=False,
        default='anaconda-enterprise',
        help=(
            'Adminsitrator password to login to AE5 install.'
            ' Default is anaconda-enterprise'
        )
    )
    parser.add_argument(
        '--cycles',
        required=False,
        default=100,
        help='Cycles or run throughs to perform on the system.'
    )
    parser.add_argument(
        '--pool-size',
        required=False,
        default=20,
        help=(
            'Pool size for the threading operation, and should be equal to '
            'the user count setup in the system to use. Default of 20'
        )
    )
    parser.add_argument(
        '--user-prefix',
        required=False,
        default='user',
        help=(
            'User prefix so that users can create and start projects and '
            'sessions. Default is user where each user is assumed to be in '
            'the following format: PREFIX01 where 01 is the number of the '
            'thread being executed and relates to the pool-size variable. '
            'By default this expects the system to have user01 - user20 setup '
            'with the password to be the same as the username.'
        )
    )
    args = parser.parse_args()
    return args


def run_cleanup(url, username, password):
    # Cleaning things up to ensure starting from a blank slate
    cleanup_cluster = AECluster(url)
    cleanup_cluster.login(username, password)
    logging.info('Stopping all sessions')
    cleanup_sessions(cleanup_cluster)
    logging.info('Removing all projects')
    cleanup_projects(cleanup_cluster)
    del cleanup_cluster


def main():
    args = handle_arguments()
    cycles = int(args.cycles)
    pool_size = int(args.pool_size)
    end_range = pool_size + 1

    logging.info('Cleaning up projects and sessions before testing')
    run_cleanup(args.url, args.username, args.password)
    for i in range(0, cycles):
        logging.info(f'Starting cycle {i} of {cycles}')

        # Creating and starting the projects
        with Pool(pool_size) as p:
            cluster_args = [
                (
                    f'{args.user_prefix}{k:02d}',
                    args.url
                ) for k in range(1, end_range)
            ]
            p.map(create_start_helper, cluster_args)

        logging.info('Sleeping to let ensure we do not hit API Limits')
        time.sleep(60)

        logging.info('Cleaning up projects and sessions')
        run_cleanup(args.url, args.username, args.password)

    logging.info('Testing completed')   


if __name__ == '__main__':
    main()
