## Creating your own log file

Beastiary reads tsv (tab delimited files) by default. To create your own log file make sure the first column is the `state` (e.g. an integer id). Save your log file in `.tsv` format (or some other kind of whitespace delimited file).

| state | header1 | header2 | etc |
| --- | --- | --- | --- |
| 0   | 123 | 123 | ... |
| 1   | 123 | 123 | ... |
| ... | ... | ... | ... |

## Change the default delimiter

Beastiary can read other delimited text file e.g. csv. To change the default delimiter e.g. to read csv files, use the `--delimiter` option with `","`. Then pass the path to the csv file to beastiary. 

<div class="termy">

```console
$ beastiary --delimiter , data/beast.csv

🐙🐁 <span style="color: #3498db;">STARTING BEASTIARY</span> 🐁🐙

Adding log files:
✅ - data/beast.csv

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>
If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3
```

</div>

!!! note
    
    Any files with non standard delimiters (e.g. csv) must be loaded from the command line.
