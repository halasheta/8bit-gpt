# 8bit-GPT: Exploring Human-AI Interaction on Obsolete Macintosh OS

This repository contains the source code for the artwork installation of `8bit-GPT`, which simulates an LLM on a legacy Macintosh OS emulator. In this case, we use `Basilisk II` for emulation/

The program running on the local machine can be found in `src/local`, where it reads the input from the emulator, sends requests to the model inference server, and writes the output to a shared file location.

The program that runs on the emulator on `THINK C 5.0` can also be found in `src/emulator` for reference. This source code can be easily imported in `Basilisk II` upon startup.