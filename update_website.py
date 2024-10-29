from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class WebsiteUpdateRequest(BaseModel):
    new_url: str

current_website = {
    "url": "http://example.com"
}

@app.put("/update_website/")
async def update_website(request: WebsiteUpdateRequest):
    if not request.new_url:
        raise HTTPException(status_code=400, detail="New URL must be provided")
    current_website["url"] = request.new_url
    return {"message": "Website URL updated successfully", "new_url": current_website["url"]}

@app.get("/current_website/")
async def get_current_website():
    return {"current_url": current_website["url"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
