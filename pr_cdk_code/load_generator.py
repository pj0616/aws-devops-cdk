import requests
import argparse
import time
import re
from collections import defaultdict

regex = r".*ip-(.*)\.ec2\.internal"

def get_ip(html_str):

    x = re.findall(regex, html_str)
    if x:
        return x[0]
    else:
        return None


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--delay", required=False, default=0.5, type=float, help="number of seconds (fractional) to wait between requests")
    ap.add_argument("--time", type=int, required=False, default=60, help="number of seconds to send requests")
    ap.add_argument("--url", type=str, required=True, help="URL")

    args = vars(ap.parse_args())

    delay = args['delay']
    run_time = args['time']
    url = args['url']
    print(delay)
    print(run_time)
    print(url)

    time.sleep(2)

    print(f"Running {run_time} seconds against url: {url}")

    ip_addr_count = defaultdict(int)

    start = time.time()
    while time.time() - start < run_time:
        print(f"{int(time.time() - start)} or {run_time} seconds to execute")
        response = requests.get(url)
        print(response.content)
        id_addr = get_ip(f"{response.content}")
        ip_addr_count[id_addr] += 1
        print(ip_addr_count.items())
        time.sleep(delay)


