[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/haralampije1/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/haralampije1/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# tiny-chess-01

A chess engine in at most 4,096 bytes of Python, entered in the [make.fun tiny-chess-01 bounty](https://make.fun/bounty/tiny-chess-01).

It plays 8 games through the env at `MAKEFUN_ENV_URL` (`POST /game`, `POST /move`), one move at a time, with a bounded PVS+TT search and quiescence — no clock, no unseeded randomness, so every replay is byte-for-byte identical.

Repack via `makefun compress engine.py --out main.py`.
