python -m llama_cpp.server ^
--model C:\LLM\TheBloke\CodeLlama-7B-Instruct-GGUF\codellama-7b-instruct.Q4_K_M.gguf ^
--n_gpu_layers 10 ^
--n_ctx 8192 ^
--n_batch 512 ^
--chat_format chatml ^
--verbose True ^
--cache False