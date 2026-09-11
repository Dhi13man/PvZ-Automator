# PvZ-Automator

OpenCV Python bot that auto-plays Plants vs. Zombies by reading the game window and clicking plants, sun, and lawn positions. It is a computer-vision automation experiment, not a trained game-playing model.

## Install

Requires Python 3 and a Windows environment (the capture path uses Win32 screen recording).

```sh
git clone https://github.com/Dhi13man/PvZ-Automator.git
cd PvZ-Automator
pip install numpy opencv-python
```

Template images in the repo (`sun.png`, `seed.png`, `lawn.png`) are the match targets the bot looks for on screen.

## Use

1. Start Plants vs. Zombies in a visible window.
2. Run `python main.py`.
3. The bot starts a Win32 capture thread (`computer_vision_handler.py`) and drives clicks through `pvz_automate.py`.

Set `should_visualize=True` in `main.py` to watch the CV output window while it runs.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
