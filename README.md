# TDD-LLM

Autonomous Software Development: A Pipeline for Test-Driven Development utilizing Large Language Models

## Description

This is an implementation of a LangChain-Pipeline aiming to improve Python-Code-Generation by simulating test-driven-development loops to generate a minimum-viable-product with no human intervention.

## Getting Started

### Dependencies
* GPU with Cuda-Support
* Windows 10/11
* Llama-cpp-python (using Visual Studio C++-Compiler and CuBlas-Support)
* see requirements.txt (some files in the generatedfiles-folder may use unspecified libraries)

### Installing

Clone the Repository: You can clone the repository using Git by running the following command in your terminal or command prompt:

```bash
git clone https://github.com/aysey001/TDD-LLM.git
```
### Executing Program

* Modify the user_message.txt, insert custom prompt
* start llm inference server
```
\bin\server_7b.bat
```
* run simple_loop.py
```
python \src\simple_loop.py
```

## Current Features
* Entry/Exit at any stage
* Supply custom prompt at any Stage
* Select application type (currently supports Flask-Application and Console Application)


## Authors

Aydin Yusuf Seyhan


## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments
Inspiration, code snippets, etc.
