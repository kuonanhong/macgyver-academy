#!/usr/bin/env python3
"""Weekly market & FX snapshot for the MacGyver Academy static site.

Writes public/academy/data/markets.json (stock performance for every listed
company in data/vendors.json) and public/academy/data/fx.json (TWD exchange
rates used by the regional price display). Standard library only.

  python3 tools/markets-v12/update_markets.py            # quotes + FX
  python3 tools/markets-v12/update_markets.py --fx-only
  python3 tools/markets-v12/update_markets.py --quotes-only
  python3 tools/markets-v12/update_markets.py --check     # validate files, no network

Data sources (all free, no API key; respect their terms and rate limits):
  quotes: Yahoo Finance chart endpoint (unofficial, delayed), fallback Stooq
          daily CSV, and TWSE / TPEx open data for Taiwan listings.
  FX:     open.er-api.com (ExchangeRate-API open access, attribution required),
          fallback fawazahmed0 currency-api on jsDelivr.
Failures never invent values: the previous snapshot of a company is kept and
marked stale, or the company is listed under "failures".
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'public/academy/data'
UA = 'Mozilla/5.0 (MacGyverAcademy weekly snapshot; +https://kuonanhong.github.io/macgyver-academy)'

YAHOO_SUFFIX = {
    'NASDAQ': '', 'NYSE': '', 'NYSEAMERICAN': '', 'TWSE': '.TW', 'TPEx': '.TWO', 'TSE': '.T', 'LSE': '.L',
    'XETRA': '.DE', 'ETR': '.DE', 'FRA': '.F', 'EPA': '.PA', 'EURONEXT': '.PA', 'PAR': '.PA', 'AMS': '.AS', 'EBR': '.BR',
    'SIX': '.SW', 'SWX': '.SW', 'KRX': '.KS', 'KOSDAQ': '.KQ', 'HKEX': '.HK', 'SSE': '.SS', 'SZSE': '.SZ',
    'STO': '.ST', 'OMX': '.ST', 'CPH': '.CO', 'HEL': '.HE', 'OSL': '.OL', 'OSE': '.OL', 'MIL': '.MI', 'BIT': '.MI',
    'BME': '.MC', 'TSX': '.TO', 'ASX': '.AX', 'NSE': '.NS',
}
TV_PREFIX = {
    'NASDAQ': 'NASDAQ', 'NYSE': 'NYSE', 'NYSEAMERICAN': 'AMEX', 'TWSE': 'TWSE', 'TPEx': 'TPEX', 'TSE': 'TSE', 'LSE': 'LSE',
    'XETRA': 'XETR', 'ETR': 'XETR', 'FRA': 'FWB', 'EPA': 'EURONEXT', 'EURONEXT': 'EURONEXT', 'PAR': 'EURONEXT', 'AMS': 'EURONEXT',
    'EBR': 'EURONEXT', 'SIX': 'SIX', 'SWX': 'SIX', 'KRX': 'KRX', 'KOSDAQ': 'KRX', 'HKEX': 'HKEX', 'SSE': 'SSE', 'SZSE': 'SZSE',
    'STO': 'OMXSTO', 'OMX': 'OMXSTO', 'CPH': 'OMXCOP', 'HEL': 'OMXHEX', 'OSL': 'OSL', 'OSE': 'OSL', 'MIL': 'MIL', 'BIT': 'MIL',
    'BME': 'BME', 'TSX': 'TSX', 'ASX': 'ASX', 'NSE': 'NSE',
}
STOOQ_SUFFIX = {'NASDAQ': '.us', 'NYSE': '.us', 'NYSEAMERICAN': '.us', 'TSE': '.jp', 'LSE': '.uk', 'XETRA': '.de', 'ETR': '.de', 'HKEX': '.hk'}
FX_CODES = ['USD', 'EUR', 'JPY', 'KRW', 'CNY', 'HKD', 'MOP', 'SGD', 'MYR', 'THB', 'VND', 'IDR', 'PHP', 'INR', 'PKR', 'BDT', 'LKR', 'NPR',
            'MMK', 'KHR', 'LAK', 'MNT', 'KZT', 'UZS', 'AZN', 'GEL', 'AMD', 'AED', 'SAR', 'QAR', 'KWD', 'BHD', 'OMR', 'JOD', 'ILS', 'IRR',
            'IQD', 'LBP', 'GBP', 'CHF', 'DKK', 'NOK', 'SEK', 'ISK', 'PLN', 'CZK', 'HUF', 'RSD', 'BAM', 'MKD', 'ALL', 'BGN', 'RON', 'MDL',
            'UAH', 'BYN', 'RUB', 'TRY', 'CAD', 'MXN', 'COP', 'PEN', 'CLP', 'ARS', 'BRL', 'VES', 'UYU', 'PYG', 'BOB', 'CRC', 'GTQ', 'DOP',
            'AUD', 'NZD', 'FJD', 'ZAR', 'NGN', 'KES', 'EGP', 'MAD', 'DZD', 'TND', 'GHS', 'ETB', 'TZS', 'UGX', 'RWF', 'XOF']


def symbols(sec: dict) -> dict:
    ex, sym = sec['exchange'], str(sec['symbol']).strip()
    ysym = sym
    if ex == 'HKEX' and sym.isdigit():
        ysym = sym.zfill(4)
    yahoo = ysym.replace('.', '-') + YAHOO_SUFFIX.get(ex, '') if ex in ('NASDAQ', 'NYSE', 'NYSEAMERICAN') else ysym + YAHOO_SUFFIX.get(ex, '')
    tv_sym = sym.replace('-', '_') if ex in ('STO', 'OMX', 'CPH', 'HEL') else sym
    tv = f"{TV_PREFIX.get(ex, ex)}:{tv_sym}"
    stooq = (sym.lower().replace('.', '-') + STOOQ_SUFFIX[ex]) if ex in STOOQ_SUFFIX else ''
    return {'yahoo': yahoo, 'tradingView': tv, 'stooq': stooq}


class Fetcher:
    def __init__(self, fixtures: Path | None = None, delay: float = 0.35):
        self.fixtures, self.delay, self.calls = fixtures, delay, 0

    def get(self, url: str, timeout: int = 20) -> bytes:
        if self.fixtures:
            key = urllib.parse.quote(url, safe='')[:200]
            path = self.fixtures / key
            if not path.exists():
                raise urllib.error.URLError('fixture missing: ' + url)
            return path.read_bytes()
        if self.calls:
            time.sleep(self.delay)
        self.calls += 1
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json,text/csv,*/*'})
        last = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return r.read(4_000_000)
            except urllib.error.HTTPError as e:
                last = e
                if e.code in (429, 500, 502, 503, 504):
                    time.sleep(2 + attempt * 3)
                    continue
                raise
            except (urllib.error.URLError, TimeoutError) as e:
                last = e
                time.sleep(1 + attempt * 2)
        raise last


def pct(new: float, old: float | None) -> float | None:
    if old in (None, 0) or new is None or not math.isfinite(old) or not math.isfinite(new):
        return None
    return round((new / old - 1) * 100, 2)


def summarize(dates: list[dt.date], closes: list[float], currency: str) -> dict:
    pairs = [(d, c) for d, c in zip(dates, closes) if c is not None and math.isfinite(c) and c > 0]
    if len(pairs) < 2:
        raise ValueError('not enough price history')
    pairs.sort()
    d_last, last = pairs[-1]
    def back(days: int):
        target = d_last - dt.timedelta(days=days)
        older = [c for d, c in pairs if d <= target]
        return older[-1] if older else None
    year_start = [c for d, c in pairs if d.year < d_last.year]
    window = [c for d, c in pairs if d >= d_last - dt.timedelta(days=365)]
    weekly, seen = [], set()
    for d, c in pairs:
        key = d.isocalendar()[:2]
        if key in seen:
            weekly[-1] = round(c, 4)
        else:
            seen.add(key); weekly.append(round(c, 4))
    return {
        'price': round(last, 4), 'currency': currency, 'asOf': d_last.isoformat(),
        'previousClose': round(pairs[-2][1], 4), 'changePct1d': pct(last, pairs[-2][1]),
        'changePct1w': pct(last, back(7)), 'changePct1m': pct(last, back(30)), 'changePct3m': pct(last, back(91)),
        'changePctYtd': pct(last, year_start[-1] if year_start else None), 'changePct1y': pct(last, back(365)),
        'high52': round(max(window), 4), 'low52': round(min(window), 4), 'spark': weekly[-53:],
    }


def from_yahoo(f: Fetcher, ysym: str) -> dict:
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ysym)}?range=1y&interval=1d&includePrePost=false&events=div%2Csplit'
    data = json.loads(f.get(url))
    res = (data.get('chart') or {}).get('result') or []
    if not res:
        raise ValueError((data.get('chart') or {}).get('error') or 'empty result')
    r = res[0]
    ts = r.get('timestamp') or []
    closes = ((r.get('indicators') or {}).get('quote') or [{}])[0].get('close') or []
    gmt = (r.get('meta') or {}).get('gmtoffset') or 0
    dates = [dt.datetime.fromtimestamp(t + gmt, dt.timezone.utc).date() for t in ts]
    meta = r.get('meta') or {}
    out = summarize(dates, closes, meta.get('currency') or '')
    out['source'] = 'Yahoo Finance chart (delayed)'
    listed = meta.get('longName') or meta.get('shortName') or ''
    if listed:
        out['listedName'] = str(listed)[:120]
    return out


STOP = {'inc', 'corp', 'corporation', 'co', 'ltd', 'limited', 'plc', 'ag', 'se', 'sa', 'nv', 'group', 'holdings', 'holding',
        'company', 'the', 'and', 'of', 'technologies', 'technology', 'international', 'industries', 'systems', 'kk', 'asa', 'ab', 'spa'}


def tokens(name: str) -> set[str]:
    import re
    return {t for t in re.findall(r'[a-z0-9]+', (name or '').casefold()) if len(t) > 1 and t not in STOP}


def name_matches(vendor: dict, listed: str) -> bool | None:
    """True/False when the exchange's company name can be compared, None when unknown."""
    if not listed:
        return None
    sec = vendor.get('security') or {}
    ours = tokens(vendor.get('nameEn', '')) | tokens(sec.get('parentEn', ''))
    theirs = tokens(listed)
    if not ours or not theirs:
        return None
    # Accept shared words or an abbreviation (e.g. "TSMC" vs "Taiwan Semiconductor Manufacturing").
    import re
    initials = ''.join(w[0] for w in re.findall(r'[a-z0-9]+', listed.casefold()))
    return bool(ours & theirs) or any(len(t) >= 3 and t in initials for t in ours)


def from_stooq(f: Fetcher, ssym: str, currency: str) -> dict:
    start = (dt.date.today() - dt.timedelta(days=400)).strftime('%Y%m%d')
    raw = f.get(f'https://stooq.com/q/d/l/?s={urllib.parse.quote(ssym)}&d1={start}&i=d').decode('utf-8', 'replace')
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows or 'Close' not in rows[0]:
        raise ValueError('no stooq data')
    dates = [dt.date.fromisoformat(r['Date']) for r in rows]
    closes = [float(r['Close']) for r in rows]
    out = summarize(dates, closes, currency)
    out['source'] = 'Stooq daily (delayed)'
    return out


def from_twse_close(f: Fetcher, symbol: str, otc: bool) -> dict:
    """Latest daily close only (no history) from Taiwan exchange open data."""
    if otc:
        rows = json.loads(f.get('https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes'))
        row = next((r for r in rows if str(r.get('SecuritiesCompanyCode')) == symbol), None)
        price = float(str(row['Close']).replace(',', '')) if row else None
    else:
        rows = json.loads(f.get('https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'))
        row = next((r for r in rows if str(r.get('Code')) == symbol), None)
        price = float(str(row['ClosingPrice']).replace(',', '')) if row and row.get('ClosingPrice') else None
    if not price:
        raise ValueError('symbol not in Taiwan open data')
    return {'price': price, 'currency': 'TWD', 'asOf': dt.date.today().isoformat(), 'spark': [],
            'source': ('TPEx' if otc else 'TWSE') + ' open data (daily close)'}


def update_quotes(f: Fetcher) -> dict:
    vendors = json.loads((DATA / 'vendors.json').read_text('utf-8'))
    old = {}
    try:
        old = json.loads((DATA / 'markets.json').read_text('utf-8')).get('quotes', {})
    except Exception:
        pass
    quotes, failures = {}, []
    listed = [v for v in vendors['vendors'] if isinstance(v.get('security'), dict) and v['security'].get('symbol')]
    cache, review = {}, []
    for i, v in enumerate(listed, 1):
        sec = v['security']; ids = symbols(sec)
        base = {'symbol': sec['symbol'], 'exchange': sec['exchange'], 'listingCurrency': sec.get('currency', ''), **ids}
        errors = []
        if ids['yahoo'] in cache:  # divisions sharing a parent's listing: fetch once
            quotes[v['id']] = {**base, **cache[ids['yahoo']]}
            continue
        for attempt in ('yahoo', 'stooq', 'twse'):
            try:
                if attempt == 'yahoo':
                    q = from_yahoo(f, ids['yahoo'])
                elif attempt == 'stooq' and ids['stooq']:
                    q = from_stooq(f, ids['stooq'], sec.get('currency', ''))
                elif attempt == 'twse' and sec['exchange'] in ('TWSE', 'TPEx'):
                    q = from_twse_close(f, sec['symbol'], sec['exchange'] == 'TPEx')
                else:
                    continue
                q = {**q, 'retrievedAt': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}
                match = name_matches(v, q.get('listedName', ''))
                if match is False:
                    q['nameMismatch'] = True
                    review.append({'vendorId': v['id'], 'nameEn': v.get('nameEn'), 'symbol': f"{sec['exchange']}:{sec['symbol']}", 'listedName': q['listedName']})
                cache[ids['yahoo']] = q
                quotes[v['id']] = {**base, **q}
                break
            except Exception as e:  # noqa: BLE001 — record and try the next source
                errors.append(f'{attempt}: {str(e)[:120]}')
        else:
            if v['id'] in old:
                quotes[v['id']] = {**old[v['id']], 'stale': True}
            failures.append({'vendorId': v['id'], 'symbol': f"{sec['exchange']}:{sec['symbol']}", 'errors': errors})
        if i % 25 == 0:
            print(f'  {i}/{len(listed)} securities processed', flush=True)
    return {'version': 12, 'updatedAt': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
            'source': 'Yahoo Finance chart endpoint (unofficial, delayed); fallbacks Stooq daily CSV and TWSE/TPEx open data.',
            'disclaimer': '每週更新的延遲行情快照，只供課程延伸閱讀，不構成投資建議；即時走勢請用 TradingView 或交易所官方資料。',
            'disclaimerEn': 'Weekly, delayed market snapshot for course context only; not investment advice. Use TradingView or official exchange data for live prices.',
            'count': len(quotes), 'quotes': quotes, 'failures': failures, 'reviewTickers': review}


def update_fx(f: Fetcher) -> dict:
    errors = []
    try:
        data = json.loads(f.get('https://open.er-api.com/v6/latest/TWD'))
        if data.get('result') != 'success' or data.get('base_code') != 'TWD':
            raise ValueError('unexpected response')
        rates = {k: float(v) for k, v in data['rates'].items() if k in FX_CODES + ['TWD'] and float(v) > 0}
        when = dt.datetime.fromtimestamp(int(data['time_last_update_unix']), dt.timezone.utc).isoformat(timespec='seconds')
        source = 'ExchangeRate-API open access (open.er-api.com) — Rates By Exchange Rate API'
    except Exception as e:  # noqa: BLE001
        errors.append('open.er-api.com: ' + str(e)[:120])
        data = json.loads(f.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/twd.json'))
        rates = {k.upper(): float(v) for k, v in data['twd'].items() if k.upper() in FX_CODES and float(v) > 0}
        when = data['date'] + 'T00:00:00+00:00'
        source = 'fawazahmed0/exchange-api (jsDelivr)'
    rates['TWD'] = 1.0
    if len(rates) < 20 or not 0.005 < rates.get('USD', 0) < 0.1:
        raise ValueError('FX sanity check failed')
    return {'version': 12, 'base': 'TWD', 'status': 'live', 'updatedAt': when, 'source': source,
            'note': '每週更新的參考匯率；結帳金額以伺服器報價為準。', 'rates': dict(sorted(rates.items())), 'errors': errors}


def write(path: Path, value: dict) -> None:
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    tmp.replace(path)


def check() -> int:
    ok = True
    for name in ('markets.json', 'fx.json'):
        p = DATA / name
        if not p.exists():
            print(f'{name}: missing (run without --check to create it)'); continue
        d = json.loads(p.read_text('utf-8'))
        if name == 'fx.json':
            bad = [k for k, v in d.get('rates', {}).items() if not (isinstance(v, (int, float)) and v > 0)]
            print(f"fx.json: {len(d.get('rates', {}))} rates, status {d.get('status')}, updated {d.get('updatedAt')}" + (f', invalid {bad}' if bad else ''))
            ok &= not bad
        else:
            q = d.get('quotes', {})
            bad = [k for k, v in q.items() if not (isinstance(v.get('price'), (int, float)) and v['price'] > 0)]
            print(f"markets.json: {len(q)} quotes, {len(d.get('failures', []))} failures, updated {d.get('updatedAt')}" + (f', invalid {bad}' if bad else ''))
            ok &= not bad
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--fx-only', action='store_true')
    ap.add_argument('--quotes-only', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--fixtures', type=Path, help='offline test responses (directory)')
    a = ap.parse_args()
    if a.check:
        return check()
    f = Fetcher(a.fixtures)
    status = 0
    if not a.quotes_only:
        try:
            write(DATA / 'fx.json', update_fx(f)); print('fx.json updated')
        except Exception as e:  # noqa: BLE001
            print('FX update failed; previous file kept:', e, file=sys.stderr); status = 2
    if not a.fx_only:
        m = update_quotes(f)
        write(DATA / 'markets.json', m)
        print(f"markets.json: {m['count']} quotes, {len(m['failures'])} failures, {len(m['reviewTickers'])} ticker names to review")
        for r in m['reviewTickers'][:40]:
            print(f"  ? {r['vendorId']}: {r['nameEn']} ≠ {r['symbol']} “{r['listedName']}” — check public/academy/data/vendors.json")
        if m['count'] == 0:
            status = 2
    return status


if __name__ == '__main__':
    sys.exit(main())
