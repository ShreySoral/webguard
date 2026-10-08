import argparse
from webguard.checker import check_site, save_result

def main():
    parser = argparse.ArgumentParser(description='WebGuard website tester')
    parser.add_argument('url', help='Website to test (https://example.com)')
    parser.add_argument('--max-links', type=int, default=20, help='Max same-host links to check')
    args = parser.parse_args()
    result = check_site(args.url, max_links=max(0, min(args.max_links, 50)))
    save_result(result)
    print(f"{result['status']} | {result['requested_url']} | HTTP {result['http_status']} | {result['load_seconds']}s")
    if result['error']:
        print('Error:', result['error'])

if __name__ == '__main__':
    main()
