# starplotter
A  real-time OCR &amp; data visualization tool for Starship flights live stream.

## Project Structure
```bash
starplotter
├── capturer
├── controller
├── ocr
└── plotter

```
Currently, we have four parts. The capturer will continuously capture the screen and store the images in a queue. The controller will take the newest image as possible and send it to the OCR part, then wait for the OCR part returning a result. The result will be written to a file, and the plotter will read the file and visualize the data.

### File Definitions
The ocr module will reture the result as a dictionary, which must contain a timestamp.

The values will be stored in a csv file, with the following format:
```csv
timestamp, value1, value2, value3, ...
```


## Contributing
Welcome! By contributing to this project, you consent to the repository owner's ability to modify the project's license.
