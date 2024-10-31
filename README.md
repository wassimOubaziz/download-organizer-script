# Download Organizer Script

A Python script to automatically organize your downloads folder by moving files into respective folders based on their types.

## Features

- Automatically detects the Downloads folder on Windows.
- Moves images, videos, documents, and other files into respective folders.
- Runs continuously and monitors the Downloads folder for new files.

## Prerequisites

- Python 3.x
- `watchdog` library

## Installation

1. Clone the repository or download the script.

```sh
git clone https://github.com/yourusername/download-organizer.git
cd download-organizer
```

2. Install the required package.
```sh
pip install watchdog
```

## Usage

1. Run the script.

```sh
python dc.py
```

The script will monitor your Downloads folder and organize the files into the following folders:

  - images
  - videos
  - documents
  - others

## Running the Script Forever with pm2

To run the script continuously even after you log out, you can use pm2:

1. Install pm2.

```sh
npm install -g pm2
```

2. Start the script with pm2.

```sh
pm2 start dc.py --interpreter python
```

3. View the status of your script.

```sh
pm2 list
```

4. Stop the script.

```sh
pm2 stop dc.py
```

5. Ensure pm2 starts on boot (optional).

```sh
pm2 save
pm2 startup
```

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests.

## License

This project is licensed under the MIT License.
