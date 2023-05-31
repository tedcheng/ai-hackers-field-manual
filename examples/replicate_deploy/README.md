# Deploy MPT-7B Model on Replicate
## Testing locally (on LamdaLabs instance)
```bash
# Clone this repo and navigate to this example
git clone https://github.com/tedcheng/ai-hackers-field-manual.git
cd ai-hackers-field-manual/examples/replicate_deploy

# Configure cog
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog

#interactive python
sudo cog run python

#run prediction (code in predict.py)
sudo cog predict -i prompt="where is the capital of California" 
```

## Pushing to Replicate
```bash
# create a model page on replicate
cog login
cog push r8.im/<your-replicate-profile>/<model-name>
```

## Interacting with Replicate Model
```bash
poetry run python test.py
```
