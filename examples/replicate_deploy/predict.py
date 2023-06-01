# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
from torch import cuda, bfloat16
import transformers
import torch
from transformers import StoppingCriteria, StoppingCriteriaList
from tensorizer import TensorDeserializer
from tensorizer.utils import no_init_or_tensor, convert_bytes, get_mem_usage

class Predictor(BasePredictor):
    def setup(self):
        device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
        local_model_path = "model"
        model = 'mosaicml/mpt-7b-instruct'

        if os.path.exists(local_model_path) and os.path.isdir(local_model_path):
            model = local_model_path
        
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            model,
            trust_remote_code=True,
            torch_dtype=bfloat16,
            max_seq_len=2048
        )
        self.model.eval()
        self.model.to(device)
        print(f"Model loaded on {device}")
        self.tokenizer = transformers.AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")

    def predict(self, prompt: str = Input(description="Prompt")) -> str:
        # mtp-7b is trained to add "<|endoftext|>" at the end of generations
        stop_token_ids = tokenizer.convert_tokens_to_ids(["<|endoftext|>"])
        # define custom stopping criteria object
        class StopOnTokens(StoppingCriteria):
            def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
                for stop_id in stop_token_ids:
                    if input_ids[0][-1] == stop_id:
                        return True
                return False
        stopping_criteria = StoppingCriteriaList([StopOnTokens()])
        
        generate_text = transformers.pipeline(
            model=self.model, tokenizer=self.tokenizer,
            task='text-generation',
            device=device,
            # we pass model parameters here too
            stopping_criteria=stopping_criteria,  # without this model will ramble
            temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
            top_p=0.15,  # select from top tokens whose probability add up to 15%
            top_k=0,  # select from top 0 tokens (because zero, relies on top_p)
            max_new_tokens=64,  # mex number of tokens to generate in the output
            repetition_penalty=1.1  # without this output begins repeating
        )
        res = generate_text(prompt)
        return(res[0]["generated_text"])
