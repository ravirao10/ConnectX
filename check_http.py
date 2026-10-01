import urllib.request
import urllib.error

for path in ['/', '/auth/login', '/auth/register', '/feed', '/admin/dashboard']:
    url = 'http://127.0.0.1:5001' + path
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            print(path, resp.status, len(resp.read()))
    except urllib.error.HTTPError as e:
        print(path, 'HTTPError', e.code)
        try:
            print(e.read().decode('utf-8', errors='ignore')[:1000])
        except Exception:
            pass
    except Exception as e:
        print(path, type(e).__name__, e)
