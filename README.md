# biotools
### Biotools is an integrated toolset for bioinformatics.  

## table of contents  
* [Introduction](#Introduction)
* [Requirements](#Requirement)
* [Installation](#Installation)
* [Usage](#Usage)   

## Introduction
Biotools is an integrated toolset for bioinformatics, it contents tools for formating data, statistic bioinformatics data, handing phylogenetic tree et al.   

## Requirements
* python3
* [ete3](http://etetoolkit.org/)
* [biolib](https://github.com/benjaminfang/biolib)  

## Installation
Install requirements into python3 library path. then biotools can be used directly.

## Usage
`biotools -h`  

> Tools for bioinformatics.  
> The flowing tools/subcommand was supported:  
>
>     * format_fasta_head
>     * format_table_separater
>     * extra_table_raws
>     * statistic_assembly
>     * statistic_phytree
>     * find_updown_elements
>     * phytree_statistic
>     * phytree_cluster
>     * phytree_collapse
>     * phytree_show
>
> usage: biotools [-h] [-V] cmd_name [cmd_args [cmd_args ...]]
>
> positional arguments:
>   cmd_name       subcommand name.
>   cmd_args       subcommand arguments.
>
> optional arguments:
>   -h, --help     show this help message and exit
>   -V, --version  show program's version number and exit
