# Introduction

Package vcf2circos is a python package based on Plotly which helps generating Circos plot, from a VCF file or a JSON configuration file.

See documentation and code in [GitHub vcf2circos](https://github.com/bioinfo-chru-strasbourg/vcf2circos).

This package is based on [PCircos](https://github.com/CJinnny/PCircos) code


# Examples

Circos plot from VCF file:

[<img src="demo_data/example.vcf.gz.png" width="600"/>](demo_data/example.vcf.gz.png)

Circos plot from JSON file:

[<img src="demo_data/demo_params.json.png" width="600"/>](demo_data/demo_params.json.png)

# Installation

## Git clone

Download package source files.

```
$ mkdir vcf2circos
$ cd vcf2circos
$ git clone https://github.com/bioinfo-chru-strasbourg/vcf2circos.git .
```

## Pip

Compile source using Pip to generate binary "vcf2circos"

```
$ python -m pip install -e .
```

## Docker

Build docker image "vcf2circos:latest"

```
$ docker build -t vcf2circos:latest .
```


# Help

```
usage: python vcf2circos.py [-h] -i INPUT -o OUTPUT [-e EXPORT] [-p OPTIONS]
                         [-n NOTEBOOK_MODE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file.
                        Format will be autodetected from file path.
                        Supported format:
                           'json', 'vcf'
  -o OUTPUT, --output OUTPUT
                        Output file.
                        Format will be autodetected from file path.
                        Supported format:
                           'png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json'
  -e EXPORT, --export EXPORT
                        Export file.
                        Format is 'json'.
                        Generate json file from VCF input file
  -p OPTIONS, --options OPTIONS
                        Options file or string.
                        Format is 'json', either in a file or as a string.
  -n NOTEBOOK_MODE, --notebook_mode NOTEBOOK_MODE
                        Notebook mode.
                        Default False
```

# Usage

## Binary 

```
$ vcf2circos --input=demo_data/example.vcf.gz --output=/data/example.vcf.gz.html --options=demo_data/options.example.json

```

## Docker

```
$ docker run -v $(pwd):/data vcf2circos:latest --input=demo_data/example.vcf.gz --output=/data/example.vcf.gz.html --options=demo_data/options.example.json

```

## Python 

```
$ python vcf2circos/vcf2circos.py --input=demo_data/example.vcf.gz --output=/data/example.vcf.gz.html --options=demo_data/options.example.json

```

# Input

This package allows multiple input formats:
- VCF including SNV/InDel/SV (see [VCF specifications](https://samtools.github.io/hts-specs/VCFv4.2.pdf)). Header needs to contain contigs (in order of appearance). See [VCF example](demo_data/example.vcf.gz).
- JSON configuration file (see [PCircos](https://github.com/CJinnny/PCircos) documentation). See [JSON configuration example](demo_data/demo_params.json).

Format will be autodetected from file path.

# Output

This package generates Circos plot in multiple formats (html, png, jpg, jpeg, webp, svg, pdf, eps, json):
- HTML file (format with customizable hover text). See [HTML example](demo_data/example.vcf.gz.html)
- Image files (i.e. png, jpg, jpeg, webp, svg, pdf, eps). See [PNG example](demo_data/example.vcf.gz.png) and [PDF example](demo_data/example.vcf.gz.pdf)
- JSON Plotly file (see [Plotly documentation](https://plotly.com/)). See [JSON plotly example](demo_data/example.vcf.gz.json)

Format will be autodetected from file path.

Output Circos plot sections from a VCF file:
![Doc Circos](docs/docs.circos.png)

# Export

Circos plot generated from VCF file can be exported as JSON configuration file, for further use. See [JSON configuration export example](demo_data/example.vcf.gz.export.json)

# Options 

Circos plot generated from a VCF file can be configured using a JSON options file. See [JSON options example](demo_data/options.example.json).

Here is an example of a JSON options file:
```
{
	"General": {
		"title": "",
		"width": 1400,
		"height": 1400,
		"plot_bgcolor": "white"
	},
	"Chr_list" : ["chr7", "chr13", "chr12", "chr14", "chr15", "chrX", "chr1"],
	"Annotations": {
		"fields": ["chr", "pos", "ref", "alt", "NOMEN", "*"],
		"show_none": true
	},
	"Cytoband": "options.cytoband.data.path.infos.json",
	"Genes": "options.genes.data.path.json",
	"Gene_list" : ["EGFR", "BRCA1", "BRCA2", "TP53", "BBS1", "BBS2", "BBS4", "BBS5"],
	"Exons": "options.genes_exons.data.path.json",
	"Categories": ["options.category.demo_data.json"]
}
```

## General section

The section "General" is a Plotly General section, which configure main options of the Circos plot (e.g. title, size, back-ground color).

Example:
```
"General": {
  "title": "",
  "width": 1400,
  "height": 1400,
  "plot_bgcolor": "white"
}
```

## Chromosome list section

The section "Chr_list" defines the list of chromosome to show in the Circos plot. Order of chromosome is still defined in the VCF header (in "contigs" section).

Example:
```
"Chr_list" : ["chr7", "chr13", "chr12", "chr14", "chr15", "chrX", "chr1"]
```

## Annotations 

The section "Annotations" defines annotations to show in each variant hover text.

A list of annotations is configured in the subsection "fields". An annotation does not need to exists, and annotation "*" defines all other available annotations. These annotations will be shown by order of appearance. 

The subsection "show_none" defines if a empty annotation (None) need to be shown (true) or not (false).

Example:
```
"Annotations": {
  "fields": ["chr", "pos", "ref", "alt", "NOMEN", "*"],
  "show_none": true
}
```

## Additionnal information

Multiple sections define additionnal information to show in the Circos plot. These sections are in a JSON format, which can be defined directly on tis section, or through a JSON file. Data are either provided in a tab-telimited file, or in a JSON format. The contain of the data (columns) depend on information type (e.g. Cytoband, genes, exons). The following example refers to cytoband information.


Example of a external JSON file:
```
"Cytoband": "options.cytoband.data.path.infos.json"
```

Example of a JSON configuration, with an external data tab-delimited file:
```
"Cytoband": {
    "path": "cytoband_hg19_chr_infos.txt",
    "header": "infer",
    "sep": "\t"
}
```

Example of a JSON configuration, with data in a JSON format through a file:
```
"Cytoband": {
    "path": "",
    "header": "infer",
    "sep": "\t",
    "dataframe": "dataframe.cytoband.json"
}
```

Example of a JSON configuration, with data in a JSON format:
```
"Cytoband": {
  "path": "",
  "header": "infer",
  "sep": "\t",
  "dataframe": {
      "orient": "columns",
      "data": {
          "chr_name": ["chr1", "chr1", "chr1", "chr1", "chr1", "chr1", "chr1", "chr1", "chr1", ...
          "start": [0, 2300000, 5400000, 7200000, 9200000, 12700000, 16200000, 20400000, 239000...
          "end": [2300000, 5400000, 7200000, 9200000, 12700000, 16200000, 20400000, 23900000, 2...
          "band_color": ["gneg", "gpos25", "gneg", "gpos25", "gneg", "gpos50", "gneg", "gpos25"...
      }
  }
}
```

Exemple of a data tab-delimited file:
```
chr_name  start     end       band_color  band
chr1      0         2300000   gneg        p36.33
chr1      2300000   5400000   gpos25      p36.32
chr1      5400000   7200000   gneg        p36.31
chr1      7200000   9200000   gpos25      p36.23
chr1      9200000   12700000  gneg        p36.22
chr1      12700000  16200000  gpos50      p36.21
chr1      16200000  20400000  gneg        p36.13
chr1      20400000  23900000  gpos25      p36.12
chr1      23900000  28000000  gneg        p36.11
```

### Cytoband

The "Cytoband" section add cytoband information on Circos plot. Data contains 4 mandatory columns, and an optional column:
- chr_name: name of the chromosome
- start: start of the band
- end: end of the band
- band_color: color of theband (Recognized stain values: gneg, gpos50, gpos75, gpos25, gpos100, acen, gvar, stalk)
- band: name of the band (optional)

See UCSC databases ("cytoBandIdeo.txt.gz") for [hg38](https://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/) and [hg19](https://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/) to generate the data tab-delimited file. See [Cytoband hg19 data tab-delimited file example](demo_data/cytoband_hg19_chr_infos.txt.txt)

Exemple of a data tab-delimited cytoband file:
```
chr_name  start     end       band_color  band
chr1      0         2300000   gneg        p36.33
chr1      2300000   5400000   gpos25      p36.32
chr1      5400000   7200000   gneg        p36.31
chr1      7200000   9200000   gpos25      p36.23
chr1      9200000   12700000  gneg        p36.22
chr1      12700000  16200000  gpos50      p36.21
chr1      16200000  20400000  gneg        p36.13
chr1      20400000  23900000  gpos25      p36.12
chr1      23900000  28000000  gneg        p36.11
```

### Genes

The "Genes" section add genes information on Circos plot. Data contains 6 mandatory columns:
- chr_name: name of the chromosome
- start: start of the gene
- end: end of the gene
- val: fixed value as 1 (not used)
- color: color of the Circos dot (see [Plotly documentation](https://plotly.com/) for authorized colors)
- gene: name of the gene

Genes' positions can overlap. Genes will be plot on a unique line.

See UCSC databases ("refGene.txt.gz") for [hg38](https://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/) and [hg19](https://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/) to generate the data file. See [refGene Genes hg19 data file example](demo_data/refGene.txt)

Exemple of a data tab-delimited refGenes Genes file:
```
chr_name  start      end        val  color   gene
chrX      110488326  110513711  1    gray    CAPN6
chr5      115368168  115395186  1    gray    ARL14EPL
chr13     72012097   72441342   1    red     DACH1
chr9      21367370   21368056   1    red     IFNA13
chr6      44213902   44221625   1    green   HSP90AB1
chr3      15247752   15294423   1    purple  CAPN7
chrX      85403454   86087605   1    gray    DACH2
chr9      21239000   21240004   1    gray    IFNA14
chr1      223714978  223853403  1    gray    CAPN8
```


### Exons

The "Exons" section add exons information on Circos plot. Data contains 7 mandatory columns:
- chr_name: name of the chromosome
- start: start of the gene
- end: end of the gene
- val: fixed value as 1 (not used)
- color: color of the Circos dot (see [Plotly documentation](https://plotly.com/) for authorized colors)
- gene: name of the gene
- exon: name of the exon

Exons' positions can overlap. Exons will be plot on a unique line.


See UCSC databases ("refGene.txt.gz") for [hg38](https://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/) and [hg19](https://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/) to generate the data file. See [refGene Exons hg19 data file example](demo_data/refGene.exons.txt)

Exemple of a data tab-delimited refGenes Exons file:

```
chr_name  start  end    val  color      gene      exon
chr1      11868  12227  1    lightgray  DDX11L17  exon1
chr1      11873  12227  1    lightgray  DDX11L1   exon1
chr1      12612  12721  1    pink       DDX11L1   exon2
chr1      12612  12721  1    yellow     DDX11L17  exon2
chr1      13220  14362  1    black      DDX11L17  exon3
chr1      13220  14409  1    red        DDX11L1   exon3
chr1      14361  14829  1    lightgray  WASH7P    exon1
chr1      14969  15038  1    lightgray  WASH7P    exon2
chr1      15795  15947  1    lightgray  WASH7P    exon3
```

### Genes list

The section "Gene_list" defines the list of genes to show in the Circos plot. This list refers to the "gene" column in the data tab-delimited refGenes Genes file. Only corresponding exons will be shown in the plot ("gene" column in the data tab-delimited refGenes Exons file).

Example of a genes list:
```
"Gene_list" : ["EGFR", "BRCA1", "BRCA2", "TP53", "BBS1", "BBS2", "BBS4", "BBS5"]
```

## Categories section



