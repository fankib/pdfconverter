# PDF Converter

Replaces parts of a PDF with an image of the PDF (prevents copy and paste)

## RUN

Invoke `python converter.py input.pdf` to convert a PDF with default settings.

### Command Line Arguments

  * input_pdf: the pdf to convert.
  * dpi: the dpi for the replaced images.
  * magic: the string to search and replace pages for.

## Create Alias

Adapt the paths in `converter.sh` and make it executable.

```
chmod u+x bash/converter.sh
```

and add

```
alias pdfconverter="/home/benjamin/git/pdfconverter/bash/converter.sh"
```

to your `~/.bashrc`.

