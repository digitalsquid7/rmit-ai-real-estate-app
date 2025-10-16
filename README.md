# 🏡 HomeMatch

**RMIT Project: Personalised Real Estate Agent**

An application that leverages LLMs and vector databases to transform standard real estate listings into personalized 
narratives that resonate with potential buyers' unique preferences and needs.

## Prerequisites

- Python 3.13

## How to set up

1. Create virtual environment
   ```shell
   venv\Scripts\python -m pip install -r requirements.txt
   ```

2. Install requirements
   ```shell
   venv\Scripts\python -m pip install -r requirements.txt
   ```
   
3. Replace "YOUR API KEY" with your ChatGPT API Key in [main.py](main.py)
   ```python
   os.environ["OPENAI_API_KEY"] = "YOUR API KEY"
   ```
   
## How to run

```shell
venv\Scripts\python main.py
```
