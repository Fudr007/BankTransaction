# BankTransaction

A simple multithreaded bank app with Accounts and Transactions (deposit/transfer), plus a small interactive console UI built with generators.

## Features

- Account model with validation, deposit and withdraw
- Thread-safe Transfer and Deposit transactions (per-account locks)
- Worker pool to process queued transactions
- Generator-based console workflow for user input

## Project layout

- accounts.py — Account and AccountList models
- transactions.py — DepositTransaction, TransferTransaction
- worker.py — TransactionWorkerPool
- user_input.py — generator-based UI helpers and menu()
- main.py — program entry point invoking menu()
- tests.py — unit tests for models, transactions and UI generators

## Requirements

- Python 3.10+ (standard library only)

## Running the app

On Windows PowerShell:

1) Create or edit the JSON with initial accounts (optional). A sample file bank_accounts.json is included.
2) Run the program:

   python .\main.py

Follow on-screen prompts to create accounts, deposit, transfer, and control the worker pool.

## Running tests

From the project root:

   python -m unittest -v

The tests exercise:
- Account validation and balance changes
- DepositTransaction and TransferTransaction execution and validation
- Concurrency safety for transfers
- Generator-based user input flows (submitting to a mocked worker pool)

## Notes

- Account balances are stored as float internally. Account.deposit/withdraw currently accept integers; conversions are handled in user_input for interactive flows.
- The worker pool is optional to run tests; tests mock it when needed.