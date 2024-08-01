# Find Research Keywords
Python script to find keywords from other papers found on a first search


## Usage
Put your api keys into a `.env` file in the current directory:
```
ACM_API_KEY=your_acm_key_here
IEEE_API_KEY=your_ieee_key_here
```

Install requirements
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run script
```python
./find-keywords.py "lora lorawan distributed"
```
