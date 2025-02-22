from fastapi import FastAPI, HTTPException, Response
import aiohttp

app = FastAPI()

@app.get("/http-dog/{code}")
async def get_http_dog(code: int):
    if not 100 <= code <= 599:
        raise HTTPException(status_code=400, detail="Invalid HTTP status code")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://http.dog/{code}.jpg") as response:
                if response.status != 200:
                    raise HTTPException(status_code=404, detail="Image not found")
                
                image_data = await response.read()
                return Response(content=image_data, media_type="image/jpeg")
                
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail="Failed to fetch image")

@app.get("/test")
async def read_root():
    return {"message": "Hello World"}