
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="SSB Mock Accounts API")

# Temporary storage: data remains while this API process runs
accounts = {}

class AccountRequest(BaseModel):
    customer_id: str
    account_type: str


@app.post("/acctservice/acctmgmt/accounts")
def create_account_request(request: AccountRequest):
    if request.customer_id in accounts:
        raise HTTPException(
            status_code=409,
            detail="Customer account already exists",
        )

    account = {
        "customer_id": request.customer_id,
        "account_type": request.account_type,
        "account_status": "ACTIVE",
        "balance": 1000.00,
    }

    accounts[request.customer_id] = account
    
    return {
        "status": "success",
        "message": "Account stored successfully",
        "account": account,
    }
    

@app.get("/acctservice/acctmgmt/accounts/{customer_id}")
def get_account(customer_id: str):
    account = accounts.get(customer_id)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )
    return {
        "status": "success",
        "account": account,
    }
    