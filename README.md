# 👾 8bit-GPT: Exploring Human-AI Interaction on Obsolete Macintosh Operating Systems

This repository contains the source code for the artwork installation of `8bit-GPT`, which simulates an LLM on a legacy Macintosh OS emulator. In this case, we use [Basilisk II](https://basilisk.cebix.net/) for emulation.

<p align="center">
<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/ff4e3894-60a1-40e3-b9c6-83f6edb0f08d" />
</p>

## Scripts

The program running on the local machine can be found in `src/local`, where it reads the input from the emulator, sends requests to the model inference server, and writes the output to a shared file location.

Also, the program that runs on the emulator on `THINK C 5.0` can be found in `src/emulator` for reference. This source code can be easily imported in `Basilisk II` upon startup.

## Demo
A demo video of the installation and user interaction with the tool can be found [here](https://drive.google.com/file/d/1B1D9JL8DKrRTY1D8IvnQ4g1002FzxMxW/view?usp=sharing).
