import fastq as fq
from typing import List
from os import walk, path

class FilterByTile(object):
    def __init__(self, inpdir: str, tiles_to_filter: List[str], outdir: str):
        """Initiate the object
        @params:
            dir - full path to directory containing input fastq files
            tiles_to_filter - a list of tiles to filter
            outdir - full path to a directory where the filtered fastq files will be written
            """
        self.inpdir = inpdir
        self.outdir = outdir
        self.tiles_to_filter = tiles_to_filter
        self.files = self.get_files()[0]
    def read_fastq(self, file: str):
        return fq.read(path.join(self.inpdir, file))
    def get_files(self):
        return [fname for _, _, fname in walk(self.inpdir)]
    @staticmethod
    def get_tile(header: str):
        """Given fastq header, returns tile no of fastq element"""
        header1 = header.split(' ')[0]
        return header1.split(':')[-3]
    def filter(self, fqfile: List):
        """Filter fastq file to only keep reads coming from tiles that are not in tiles_to_filter"""
        filtered_fqfile = []
        for i, fqelement in enumerate(fqfile):
            tile = self.get_tile(fqelement.getHead())
            if not tile in self.tiles_to_filter:
                filtered_fqfile.append(fqelement)
        print("Filtering fastq file..")
        print(f"Keeping {len(filtered_fqfile)} of {i} reads..")
        return filtered_fqfile
    def filter_fastq(self, file_to_filter: str, pref: str):
        """Given file name, read fastq file filter and save it"""
        fqfile = self.read_fastq(file_to_filter)
        filtered_fq = self.filter(fqfile)
        if file_to_filter.endswith('gz'):
            filenm = file_to_filter.replace('.gz', '')
        else:
            filenm = file_to_filter
        outfile = path.join(self.outdir, pref + filenm)
        print(f"Writing {file_to_filter} file as {outfile}")
        fq.write(filtered_fq, outfile)
    def filter_fastqs(self, pref='filtered_'):
        """Main function that filters fastq files in inpdir to remove reads coming from given tiles and writes output into given folder"""
        for file_to_filter in self.files:
            self.filter_fastq(file_to_filter, pref=pref)

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Filter fastq files to remove reads coming from given tiles")
    parser.add_argument('--tiles', dest='tiles', nargs='+', required=True, help='a list of tiles to filter')
    parser.add_argument('--inpdir', dest='inpdir', type=str, required=True, help='full path to directory containing input fastq files')
    parser.add_argument('--outdir', dest='outdir', type=str, required=True, help='full path to a directory where the filtered fastq files will be written')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    fbt = FilterByTile(args.inpdir, args.tiles, args.outdir)
    fbt.filter_fastqs()

