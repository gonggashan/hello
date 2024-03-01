from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import PlainTextResponse
import subprocess
import os

app = FastAPI()

@app.post("/execute_script")
async def execute_script(serviceName: str = Form(...), env: str = Form(...)):
    script_directory = f"/home/ec2-user/k8s/{env}/{serviceName}/"
    script_path = f"{script_directory}{serviceName}.sh"

    try:
        # 切换到脚本所在目录
        os.chdir(script_directory)

        # 使用 subprocess 运行 Bash 脚本，传入额外的环境参数
        command = ["sudo", "bash", "-x", script_path]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # 提取执行过程和结果
        execution_output = result.stdout
        execution_error = result.stderr
        response_content = f"release success\n{execution_output}"

        return PlainTextResponse(content=response_content, status_code=200)
    except FileNotFoundError:
        return PlainTextResponse(content="Script not found", status_code=404)
    except subprocess.CalledProcessError as e:
        response_content = f"Error executing script: {e.stderr}"
        return PlainTextResponse(content=response_content, status_code=200)
    except Exception as e:
        response_content = f"An unexpected error occurred: {str(e)}"
        return PlainTextResponse(content=response_content, status_code=200)
    finally:
        # 最终还原到原来的工作目录
        os.chdir(os.path.expanduser("~"))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)