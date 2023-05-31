# Deploy MPT-6B Model on Replicate
## Testing locally (on LamdaLabs instance)
```bash
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
sudo cog run python #interactive python
sudo cog predict -i prompt="where is the capital of California" #run prediction (code in predict.py)
```

## Pushing to Replicate
### To be added

## Interacting with Replicate Model
```bash
poetry run python test.py
```