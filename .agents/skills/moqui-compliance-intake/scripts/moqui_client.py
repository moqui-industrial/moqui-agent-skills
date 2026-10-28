#!/usr/bin/env python3
"""Minimal client of a running Moqui instance for the compliance skills (standard library only, runs with python3 -I).

    from moqui_client import Moqui
    m = Moqui()                                   # env MOQUI_URL (http://localhost:8080), MOQUI_AUTH (john.doe:moqui)
    m.rest('compliance/search', queryString='emergency stop', target='hooks')   # GET /rest/s1/...
    m.tree('IEC-62443-3-2-2020-EN', '4.6.7')     # an item with its ancestors and children (CLOBs decoded)
    m.mcp('plan_norm_project', rootProductId='X') # an MCP tool of moqui-mcp, result parsed
    m.load_xml('<entity-facade-xml>...</entity-facade-xml>')   # Tools > Entity > Data Import (needs the tools app)

Reading goes through REST and MCP, which decode text; the SQL Runner returns CLOB columns as escaped literals and is
left to read-only checks. Writing goes through services (MCP) where one exists, and through Data Import for plain records
(products, classification, assets, devices): a load never deletes, it creates or updates.
"""
import base64
import http.cookiejar
import json
import os
import re
import sys
import urllib.parse
import urllib.request

MCP_VERSION = '2026-07-28'


class MoquiError(RuntimeError):
    pass


class Moqui:
    def __init__(self, url=None, auth=None, timeout=300):
        self.url = (url or os.environ.get('MOQUI_URL', 'http://localhost:8080')).rstrip('/')
        self.user, _, self.password = (auth or os.environ.get('MOQUI_AUTH', 'john.doe:moqui')).partition(':')
        self.timeout = timeout
        self._basic = 'Basic ' + base64.b64encode(f'{self.user}:{self.password}'.encode()).decode()
        self._opener = None
        self._mcp_id = 0

    # ---- REST (basic authentication) ----
    def rest(self, path, **params):
        q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
        req = urllib.request.Request(f'{self.url}/rest/s1/{path.lstrip("/")}' + (f'?{q}' if q else ''),
                                     headers={'Authorization': self._basic, 'Accept': 'application/json'})
        return self._json(req)

    def tree(self, agreement_id, seq_id=None, **params):
        return self.rest('compliance/tree', agreementId=agreement_id, agreementItemSeqId=seq_id, **params)

    def search(self, query, target=None, page_size=10, **params):
        return self.rest('compliance/search', queryString=query, target=target, pageSize=page_size, **params)

    # ---- MCP (moqui-mcp generic service tools) ----
    def mcp(self, name, **arguments):
        self._mcp_id += 1
        meta = {'io.modelcontextprotocol/protocolVersion': MCP_VERSION, 'io.modelcontextprotocol/clientCapabilities': {},
                'io.modelcontextprotocol/clientInfo': {'name': 'moqui-agent-skills', 'version': '1'}}
        body = {'jsonrpc': '2.0', 'id': self._mcp_id, 'method': 'tools/call',
                'params': {'name': name, 'arguments': arguments, '_meta': meta}}
        req = urllib.request.Request(f'{self.url}/mcp', json.dumps(body).encode(), headers={
            'Authorization': self._basic, 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
            'MCP-Protocol-Version': MCP_VERSION, 'Mcp-Method': 'tools/call', 'Mcp-Name': name})
        r = self._json(req)
        if 'error' in r:
            raise MoquiError(f'{name}: {r["error"]}')
        res = r['result']
        text = res['content'][0]['text'] if res.get('content') else ''
        if res.get('isError'):
            raise MoquiError(f'{name}: {text[:500]}')
        try:
            return json.loads(text)
        except ValueError:
            return text

    # ---- screens (form session with its token) ----
    def _session(self):
        if self._opener is None:
            self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
            self._opener.open(f'{self.url}/Login', timeout=self.timeout).read()
            data = urllib.parse.urlencode({'username': self.user, 'password': self.password}).encode()
            self._opener.open(f'{self.url}/Login/login', data, timeout=self.timeout).read()
        return self._opener

    def token(self, page):
        html = self._session().open(f'{self.url}{page}', timeout=self.timeout).read().decode('utf-8', 'replace')
        m = re.search(r'name="moquiSessionToken" value="([^"]+)"', html)
        if not m:
            raise MoquiError(f'no session token on {page}: login failed for {self.user} or no access')
        return m.group(1)

    def post_screen(self, page, transition, **fields):
        fields['moquiSessionToken'] = self.token(page)
        data = urllib.parse.urlencode(fields).encode()
        return self._session().open(f'{self.url}{page}/{transition}', data, timeout=self.timeout).read().decode('utf-8', 'replace')

    def load_xml(self, xml_text):
        """Load entity-facade-xml records through Tools > Entity > Data Import; returns the number of records loaded."""
        html = self.post_screen('/apps/tools/Entity/DataImport', 'load', xmlText=xml_text)
        m = re.search(r'Loaded (\d+) records', html)
        if not m:
            errs = re.findall(r'(?:Error|error)[^<]{0,300}', html)
            raise MoquiError('data import failed: ' + ' | '.join(e for e in errs if 'errorMessage' not in e)[:800])
        return int(m.group(1))

    def sql(self, query, group='transactional', limit=500):
        """Read-only SQL through Tools > Entity > SQL Runner (basic authentication); rows as lists of strings, header
        first. CLOB columns come back as escaped literals: read texts through rest()/tree() instead."""
        import html as _html
        data = urllib.parse.urlencode({'groupName': group, 'limit': limit, 'sql': query}).encode()
        req = urllib.request.Request(f'{self.url}/apps/tools/Entity/SqlRunner', data, headers={'Authorization': self._basic})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            s = r.read().decode('utf-8', 'replace')
        rest = re.sub(r'<table.*?</table>', '', s, flags=re.S)
        err = re.findall(r'\b\w*(?:Exception|SQLError)\b[^<]{0,300}', rest)
        if err:
            raise MoquiError(f'sql: {err[0]}')
        rows = []
        for t in re.findall(r'<table.*?</table>', s, re.S):
            for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
                rows.append([re.sub(r'\s+', ' ', _html.unescape(re.sub(r'<[^>]+>', '', c))).strip()
                             for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.S)])
        return rows

    def existing(self, table, column, ids, group='transactional'):
        """The subset of ids present in table.column (ids are quoted; only [A-Za-z0-9_.-] allowed)."""
        ids = sorted(set(ids))
        bad = [i for i in ids if not re.fullmatch(r'[A-Za-z0-9_.\-]+', i)]
        if bad:
            raise MoquiError(f'invalid ids: {bad[:5]}')
        found = set()
        for k in range(0, len(ids), 200):
            chunk = ids[k:k + 200]
            rows = self.sql(f"SELECT {column} FROM {table} WHERE {column} IN ({','.join(repr(i) for i in chunk)})", group)
            found |= {r[0] for r in rows[1:]}
        return found

    def _json(self, req):
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            raise MoquiError(f'{req.full_url}: HTTP {e.code} {e.read().decode("utf-8", "replace")[:300]}')


def xml_attr(value):
    return (str(value).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;'))


if __name__ == '__main__':
    m = Moqui()
    print(json.dumps(m.rest(sys.argv[1], **dict(a.split('=', 1) for a in sys.argv[2:])), indent=1, ensure_ascii=False)[:4000]
          if len(sys.argv) > 1 else __doc__)
