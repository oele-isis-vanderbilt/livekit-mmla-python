# LiveKit-MMLA
This repository maintains a simple python client to Livekit MMLA API.

Currently, this client supports the following features:
- Get the livekit token.
- Create Rooms
- List Rooms

This is a work in progress and more features will be added soon.

## Installation
```bash
$ git clone git@github.com/oele-isis-vanderbilt/livekit-mmla-python.git
$ cd livekit-mmla
$ pip install .
```

## Usage for a simple token server
First go to https://dashboard.livekit-mmla.org, and create an API key/secret pairs for you account.

Create an `.env` file at the root of this repository with the following content:
```bash
LIVEKIT_MMLA_SERVER_URL=https://api.livekit-mmla.org
LIVEKIT_MMLA_API_KEY=your-api-key
LIVEKIT_MMLA_API_SECRET=your-api-secret
LIVEKIT_MMLA_PROJECT=your-project-name
```

Then install dependencies for the token server:
```bash
$ cd livekit-mmla
$ pip install .[token-server]
```

Then run the token server:
```bash
$ uvicorn token_server:app --reload
```
