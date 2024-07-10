# filter_by_tile_id

A Python script to filter FASTQ files by removing reads from specified tiles. This script depends on the Python `fastq` library.

## Usage

filter_by_tile_id.py [-h] --tiles TILES [TILES ...] --inpdir INPDIR --outdir OUTDIR

Filter fastq files to remove reads coming from given tiles

options:
  -h, --help            show this help message and exit
  --tiles TILES [TILES ...]
                        a list of tiles to filter
  --inpdir INPDIR       full path to directory containing input fastq files
  --outdir OUTDIR       full path to a directory where the filtered fastq files will be written
