from iota import *
import random
import time

def main():
    node = 'http://nodes.iota.fm:80'
    # https://field.carriota.com:443
    # http://nodes.iota.fm:80
    api = Iota(node)
    gna_result = api.get_new_addresses()
    address = gna_result['addresses'][0]
    print(address)
    message = TryteString.from_unicode("Hello")
    tag = 'CBCFCFCECBC9CCCCCICHCCCACFC'
    print(message)
    send_message(api, address, tag, message)
    transactions = get_transactions(api, address)
    print(transactions)


def send_message(api, address, tag, message):
        send_confirmation = False
        while not send_confirmation:
            try:
                print("Sending message to the tangle...")
                api.send_transfer(
                  depth = 100,
                  transfers = [
                    ProposedTransaction(
                      address =
                        Address(
                          address,
                        ),
                      value = 0,
                      tag = Tag(tag),
                      message = message,
                    ),
                  ],
                )
                send_confirmation = True
                print("The message was successfully attached to the tangle")
                print()
            except:
                print("Error: Retrying tangle attachment")
                print()
                time.sleep(20)
                pass

def get_transactions(api, address):
        print("Searching the tangle messages...")
        new_transactions = []
        transaction_dict = api.find_transactions(bundles=None, \
                            addresses=[address], tags=None, approvees=None)
        print(transaction_dict)
        for transaction_hash in transaction_dict['hashes']:
            trytes = api.get_trytes([transaction_hash])['trytes'][0]
            print(trytes)
            transaction = Transaction.from_tryte_string(trytes)
            print(transaction)
            message = transaction.signature_message_fragment
            print(message)
            new_transactions.append(message)
        print("Complete")
        print()
        return new_transactions

main()
