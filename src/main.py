import os
import uuid
from typing import Annotated

from fastapi import FastAPI, HTTPException, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": 200}


@app.post("/edit-file/")
async def edit_file(file: Annotated[bytes, File()], script: Annotated[str, Form()]):
    # 一時的なファイル保存先の設定
    temp = f"{str(uuid.uuid4())}"

    with open(temp, "wb") as buffer:
        buffer.write(file)

    try:
        exec(script, globals())
        return FileResponse(temp, filename=temp)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": 500, "detail": str(e)})
    finally:
        # 一時ファイルの削除
        if os.path.exists(temp):
            os.remove(temp)
