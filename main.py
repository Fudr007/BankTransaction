from accounts import AccountList, Account

if __name__ == "__main__":
    list_accounts = AccountList()
    list_accounts.import_json("file.json")
