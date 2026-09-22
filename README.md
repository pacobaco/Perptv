PerpTV

Perpetual video-jockey automation: generate clips from multiple AI video APIs,
rotate an MP4 library, inject MTV-style VJ bumpers, rebuild HLS playlists, and
host the result.

Stripe billing and optional Tor onion delivery are included as scaffolding.

Pipeline

```text
originals/ → providers → station/media/*.mp4 → station/playlist.m3u8 → nginx HLS → Stripe
```

An M3U8 of file segments is a playlist, not a live switcher.

For a continuous VJ mount, put ffmpeg/MediaMTX or OBS in front of the HLS output
and overlay lower-thirds from vj/overlays.py.

Features

• Weighted provider rotation: Runway, Kling, Luma, Pika
• MP4 library pruning to max_clips
• Clearnet and optional onion HLS playlists
• VJ bumper + ident insertion
• Stripe plan/meter usage hooks
• nginx/systemd/Tor deployment examples
• Provider adapters designed to be replaced when vendor APIs change

Requirements

• Python 3.11+
• ffmpeg
• VPS for public hosting
• API keys for enabled providers
• Stripe keys if selling station hosting
• Owned source clips/stills for image-to-video workflows

Quick start

```bash
cd /opt/perptv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cp config.example.json config.json
mkdir -p originals station/media station/overlays
python tv.py
```

Optional application entry point:

```bash
python app.py
```

────────

requirements.txt

```text
python-dotenv>=1.0
requests>=2.31
stripe>=10.0
```

.env.example

```dotenv
RUNWAY_API_KEY=
KLING_API_KEY=
LUMA_API_KEY=
PIKA_API_KEY=

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_CUSTOMER_ID=
HOST_PLAN=basic

PUBLIC_BASE_URL=https://tv.example.com
ONION_BASE_URL=

STATION_NAME=PerpTV
```

config.example.json

```json
{
  "station": {
    "name": "PerpTV",
    "tagline": "24/7 Perpetual VJ",
    "max_clips": 40,
    "clip_seconds": 8,
    "target_width": 1280,
    "target_height": 720,
    "insert_bumper_every": 4
  },
  "paths": {
    "originals": "originals",
    "media": "station/media",
    "overlays": "station/overlays",
    "playlist": "station/playlist.m3u8"
  },
  "providers": [
    {"name": "runway", "weight": 3, "enabled": true},
    {"name": "kling", "weight": 3, "enabled": true},
    {"name": "luma", "weight": 2, "enabled": true},
    {"name": "pika", "weight": 2, "enabled": true}
  ],
  "prompts": [
    "neon 1990s music-television studio, dancers, CRT stacks, film grain",
    "graffiti block letters PERPTV over zebra-stripe ident, analog glow",
    "video jockey booth, colorful jackets, live concert footage on monitors",
    "hyperkinetic music video montage, saturated lights, handheld camera"
  ]
}
```

Architecture

```text
                         ┌─────────────────────┐
                         │   AI Video APIs      │
                         │ Runway/Kling/Luma/   │
                         │ Pika adapters        │
                         └──────────┬──────────┘
                                    │
                                    ▼
┌──────────────┐          ┌─────────────────────┐
│  originals/  │ ───────► │   PerpTV builder    │
│  owned media │          │ tv.py / app.py      │
└──────────────┘          └──────────┬──────────┘
                                    │
                         normalize / prune / VJ
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  station/media/     │
                         │      *.mp4          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ station/playlist    │
                         │       .m3u8          │
                         └──────────┬──────────┘
                                    │
                           nginx / HLS serving
                              /           \
                             ▼             ▼
                         clearnet       optional Tor
                             │             │
                             └──────┬──────┘
                                    ▼
                              Viewers / apps
```

Stripe billing and usage metering can be attached to the application layer.

Important HLS distinction

A static M3U8 playlist that references MP4 objects is not itself a live video
switcher. For true continuous output, use a media pipeline such as ffmpeg,
MediaMTX, or OBS to sequence the content and publish a live HLS stream.

VJ graphics can be applied upstream with ffmpeg filters or through the overlay
pipeline represented by vj/overlays.py.

Media and rights

Use source clips, stills, music, logos, and generated assets for which you have
the necessary rights or permissions. Provider API terms may impose additional
restrictions on generation, storage, redistribution, or commercial use.

Deployment

A typical VPS deployment can use:

```text
PerpTV application
       │
       ├── ffmpeg / media pipeline
       │
       ├── nginx
       │
       ├── optional Tor onion service
       │
       └── Stripe billing / metering
```

The deploy/ directory can contain nginx, systemd, and Tor configuration
templates appropriate to the selected hosting environment.

Project structure

```text
perptv/
├── README.md
├── app.py
├── tv.py
├── config.example.json
├── .env.example
├── requirements.txt
├── originals/
├── providers/
├── station/
│   ├── media/
│   ├── overlays/
│   └── playlist.m3u8
├── vj/
│   └── overlays.py
├── stripe/
│   └── hooks.py
└── deploy/
    ├── nginx.conf.example
    ├── perptv.service
    ├── perptv.timer
    └── torrc.example
```

Status

This document describes the PerpTV architecture and configuration surface.
Provider integrations, Stripe metering, and deployment files should be treated
as adapters/templates and updated against the current vendor APIs and hosting
environment before production use.
