# tiny-chess-01

A chess engine in at most 4,096 bytes of Python, entered in the [make.fun tiny-chess-01 bounty](https://make.fun/c/tiny-chess-01).

It plays 8 games through the env at `MAKEFUN_ENV_URL` (`POST /game`, `POST /move`), one move at a time, with a bounded alpha-beta search and quiescence — no clock, no unseeded randomness, so every replay is byte-for-byte identical.

[![make.fun bounty](https://shields.make.fun/tiny-chess-01/entry)](https://make.fun/c/tiny-chess-01)
[![make.fun leaderboard](https://shields.make.fun/tiny-chess-01/leaderboard)](https://make.fun/c/tiny-chess-01/leaderboard)
[![make.fun status](https://shields.make.fun/tiny-chess-01/status)](https://make.fun/c/tiny-chess-01)
