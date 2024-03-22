from fastapi import FastAPI
from dragons96_tools.fastapi import wrapper_exception_handler
from dragons96_tools.models import R

app = FastAPI()


@app.get('/')
def hello():
    return R.ok(data='Hello')


app = wrapper_exception_handler(app)
