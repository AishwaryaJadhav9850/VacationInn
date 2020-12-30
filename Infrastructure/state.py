from typing import Optional
from data.owner import Owner
import Services.services as serv

active_account:Optional[Owner]=None

def reload_account():
    global active_account
    if not active_account:
        return
    active_account=serv.find_account_by_email(active_account.email)

