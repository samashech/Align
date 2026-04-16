import requests
import time
import os

# Upload a dummy file to get user_id
files = {'resume': ('dummy.pdf', b'dummy content')}
resp = requests.post('http://localhost:5000/upload', files=files, data={'job_type': 'Full Time'})
print("Upload response:", resp.json())
user_id = resp.json().get('user_id')

if user_id:
    # check debug-jobs
    for i in range(5):
        time.sleep(2)
        resp2 = requests.get(f'http://localhost:5000/debug-jobs/{user_id}')
        print(f"Status {i}:", resp2.json())
