import pandas as pd
from google.cloud import storage
import requests


def UpdateDisneyQueues(*args, **kwargs):
    client = storage.Client()
    bucket = client.get_bucket('bucket_queues')

    stats = storage.Blob(bucket=bucket, name='queue_times.csv').exists(client)

    if stats:
        df = pd.read_csv('gs://bucket_queues/queue_times.csv', index_col=False)
    else:
        df = pd.DataFrame(columns=['Date', 'Time', 'Ride', 'WaitTime', 'IsOpen'])

    ride_details = []
    for park_id in [4, 28]:
        queue_times = requests.get(f'https://queue-times.com/parks/{park_id}/queue_times.json').json()
        for land in queue_times['lands']:
            for ride in land['rides']:
                date, time = ride['last_updated'][:-5].split('T')
                ride_details.append([date, time, ride['name'], ride['wait_time'], ride['is_open']])

    new_df = pd.DataFrame(columns=['Date', 'Time', 'Ride', 'WaitTime', 'IsOpen'], data=ride_details)
    combined_df = pd.concat([df, new_df])

    bucket.blob('queue_times.csv').upload_from_string(combined_df.to_csv(index=False), 'text/csv')
    return "Complete"


if __name__ == '__main__':
    main()
