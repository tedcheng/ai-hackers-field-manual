# Deploy MPT-6B Model on Replicate
## Testing locally (on LamdaLabs instance)
```bash
# clone this repo and navigate to this example
git clone https://github.com/tedcheng/ai-hackers-field-manual.git
cd ai-hackers-field-manual/examples/replicate_deploy

sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
#interactive python
sudo cog run python
#run prediction (code in predict.py)
sudo cog predict -i prompt="where is the capital of California" 
```

## Pushing to Replicate
### To be added

## Interacting with Replicate Model
```bash
poetry run python test.py
```
