#!/usr/bin/env python3
import argparse
import daemon


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('txid')
    parser.add_argument('--dev', action='store_true')
    parser.add_argument('--networkid')
    parser.add_argument('--port')
    args = parser.parse_args()

    if args.dev:
        d = daemon.Daemon(port=args.port, cookie_dir=f'~/.tapyrus/dev-{args.networkid}')
    else:
        d = daemon.Daemon(port=args.port, cookie_dir=f'~/.tapyrus/prod-{args.networkid}')

    txid = args.txid

    txn, = d.request('getrawtransaction', [[txid, True]])
    vin = txn['vin']

    fee = 0.0
    for txi in txn['vin']:
        prev_txid = txi['txid']
        prev_tx, = d.request('getrawtransaction', [[prev_txid, True]])
        index = txi['vout']
        prev_txo = prev_tx['vout'][index]
        print(f"{prev_txid}:{index:<5} {prev_txo['value']:+20.8f}")
        fee += prev_txo['value']

    for i, txo in enumerate(txn['vout']):
        print(f"{txid}:{i:<5} {-txo['value']:+20.8f}")
        fee -= txo['value']

    print(f"Fee = {1e6 * fee:.2f} uBTC = {1e8 * fee / txn['vsize']:.2f} sat/vB")

if __name__ == '__main__':
    main()
