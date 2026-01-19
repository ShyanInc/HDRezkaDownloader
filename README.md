# HDRezkaTool

A powerful Python tool for downloading movies and TV series from HDRezka. This tool provides a convenient command-line interface to search, browse, and download content with various quality options.

## Features

- 🔍 Search functionality for movies and TV series
- 🎬 Support for both movies and TV series downloads
- 📺 Multiple download options for TV series:
  - Download entire season
  - Download specific episodes
  - Download multiple seasons
  - Download complete series
- 🎥 Quality selection (720p by default)
- 📝 Download history tracking
- 🔄 Resume interrupted downloads
- 🌐 Russian language interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/HDRezkaTool.git
cd HDRezkaTool
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. Follow the interactive prompts:
   - Enter search query
   - Select content from search results
   - Choose download options
   - Select quality (default: 720p)

### Download Options for TV Series

1. Download a single season:
   - Select option 1
   - Enter season number

2. Download specific episodes:
   - Select option 2
   - Enter season number
   - Enter starting episode number

3. Download multiple seasons:
   - Select option 3
   - Enter starting season number
   - Enter ending season number

4. Download complete series:
   - Select option 4

## Project Structure

```
HDRezkaTool/
├── HDRezkaAPI/        # Core API implementation
├── main.py           # Main application script
├── history.json      # Download history
├── LICENSE          # Project license
└── README.md        # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the license included in the LICENSE file.

## Disclaimer

This tool is for educational purposes only. Please respect copyright laws and the terms of service of the source website. The developers are not responsible for any misuse of this tool.
