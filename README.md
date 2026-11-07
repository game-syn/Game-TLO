# Game-TLO

A game-development project repository. The engine, gameplay scope, and production details have not been defined yet; update this README as the project takes shape.

## Development environment

This repository includes a GitHub Codespaces dev container at `.devcontainer/devcontainer.json`, configured as a high-resource C++ environment with Git LFS and Vulkan development tools.

To get started:

1. Open this repository on GitHub.
2. Select **Code** → **Codespaces** → **Create codespace on `main`**.
3. Choose the largest machine type available to your account or organization.

The dev container requests 32 CPUs, 64 GB of memory, and 128 GB of storage. GitHub only offers machine types supported by your account, organization policies, and current availability; the request does not guarantee a particular machine. Codespaces is a development environment, not a substitute for a local GPU workstation or a game-engine editor that requires a supported desktop environment.

## Included tooling

The container installs C++ development tooling, CMake/Ninja support, Git LFS, and Vulkan development utilities. These are a general-purpose starting point, not an engine-specific toolchain. Add the required engine and project build steps after choosing an engine and target platforms.

## Large assets

Use Git LFS for large binary assets such as source art, audio, and other files that should not be stored as ordinary Git blobs. Confirm the repository's LFS storage and bandwidth limits before adding substantial assets.

## Project status

This repository is currently a starter setup. Add the game description, engine/version, build and test instructions, contribution guidance, and asset workflow here when those decisions are made.
