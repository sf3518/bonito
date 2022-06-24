# Barker Code for DNA Storage

## Repository Setup
Clone required repository:
```
git clone https://github.com/sf3518/bonito.git
cd bonito
```

## Barker Code Explanation
If not familiar with Barker Code, a jupyter notebook explanation of Barker Code is provided.

Run:
```
jupyter notebook barker_code_illustration.ipynb
```

## Bonito Error Distribution Analysis
### Download Dataset
```
wget  https://s3-eu-west-1.amazonaws.com/ont-research/taiyaki_walkthrough.tar.gz
tar zxvf taiyaki_walkthrough.tar.gz
```
All the FAST5 files are contained in the `taiyaki_walkthrough/reads/` folder.
The reference file containing the ground truth sequence can be found at: `taiyaki_walkthrough/reference.fasta`.

### Setup Bonito
GPU is required to run Bonito.
Create virtual environment and install dependencies:
```
python3 -m venv venv3
source venv3/bin/activate
pip install -r requirements.txt
python setup.py develop
```
Download all pretrained models:
```
bonito download --training
```
Generate FASTQ basecalling result:
```
bonito basecaller bonito/models/choose_your_model/ taiyaki_walkthrough/reads/ > basecalls.fastq
```

To directly generate comparison result against reference:
```
bonito basecaller bonito/models/choose_your_model/ --reference taiyaki_walkthrough/reference.fasta taiyaki_walkthrough/reads/ > basecalls.sam
```


To train your own model or use more advanced features, refer to official [README](https://github.com/sf3518/bonito/blob/master/bonito_README.md).


### Bonito Trouble Shooting
You might encounter those errors when setting up Bonito and here are the solutions:



* Error with protobuf. A recent release of Bonito might have caused the problem. 
If you see `Downgrade the protobuf package to 3.20.x or lower.'`, or `Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`
error messages, you can either downgrade protobuf or set environment variable explicitly for protobuf.
The former solution is preferred, as the latter will slow down training speed significantly.
To downgrade, run:
```
pip install protobuf==3.20.0
```
* gcc must be present to run Bonito. If not installed, run:
```
sudo apt install build-essential
```

* Error related to GPU incompatibility issue (e.g. sm86 incompatible). Run:
```
pip install -f https://download.pytorch.org/whl/torch_stable.html ont-bonito-cuda111
```

### Run Error Distribution Analysis
Download samtools to manipulate SAM file:
```
conda install -c bioconda samtools
```

First extract all CIGAR strings from the SAM file and write to `cigar.txt`:
```
samtools view basecalls.sam | cut -f 6 > cigar.txt
```

Run `parse_cigar.py` to print the insertion, deletion, substitution error rates and the error distribution diagram.
The first argument is the path to the CIGAR string extracted from SAM file. The second argument
is the number of bins when viewing error distribution histogram.

```
python3 parse_cigar.py cigar.txt 100
```

## Error Simulation
First generate the reference FASTA file:
```
python3 error_simulation.py --n 100 --l 500 --std 10 -o references/
```
--n specifies the number of sequences, --l specifies the average length of the sequences,
--std specifies the standard deviation of the sequence lengths, 
-o points to the directory to store reference files.

Next we generate FAST5 file with DeepSimulator. Run the following to set up:

```
git clone https://github.com/lykaust15/DeepSimulator.git
cd ./DeepSimulator/
./install.sh
```
For context-independent pore mode, run:
```
./deep_simulator.sh -i path_to_fasta_file
```
For context-dependent mode, add `-M 0` to the end of the command.

With FAST5 and FASTA reference file, the rest of the simulation process is the same with the last section.
