# Sales Data Pipeline

Pipeline locale di data engineering che genera dati sintetici di vendita per Italia e Germania, li elabora con PySpark e produce dataset pronti per l'analisi.

## Funzionalità

- Generazione riproducibile di 20.000 vendite sintetiche.
- Lettura di due CSV con intestazioni differenti.
- Standardizzazione di nomi e tipi delle colonne.
- Filtri per righe incomplete o non valide.
- Rimozione dei duplicati.
- Calcolo di vendite, unità e ricavi mensili per Paese.
- Esportazione dei risultati in CSV.

## Tecnologie

- Python 3.14
- PySpark 4.2.0
- Java 17, 21 o 25
- Hadoop 3.5.0 `winutils.exe` per la scrittura locale su Windows

## Struttura

```text
sales-data-pipeline/
├── data/
│   ├── sales_italy.csv
│   └── sales_germany.csv
├── output/                 # Generata dalla pipeline, esclusa da Git
│   ├── sales_clean/
│   └── monthly_sales/
└── src/
    ├── generate_data.py
    └── combine_sales.py
```

## Requisiti

- Windows
- Python 3.14
- Java 17, 21 o 25
- Dipendenze Python definite nell'ambiente virtuale del progetto
- Hadoop `winutils.exe` compatibile con Hadoop 3.5.0

## Esecuzione su Windows

Attiva l'ambiente virtuale del progetto:

```powershell
.\.venv\Scripts\Activate.ps1
```

Imposta `HADOOP_HOME` per la sessione corrente. Nell'esempio, i binari Hadoop sono stati estratti in `C:\hadoop-win`:

```powershell
$env:HADOOP_HOME = "C:\hadoop-win"
$env:PATH = "$env:HADOOP_HOME\bin;$env:PATH"
```

Verifica che Windows trovi `winutils.exe`:

```powershell
Test-Path "$env:HADOOP_HOME\bin\winutils.exe"
```

Il risultato deve essere `True`. Mantieni la stessa sessione PowerShell attiva durante l'esecuzione: le variabili impostate con `$env:` sono temporanee.

## Generare i dati

Per rigenerare i CSV sintetici:

```powershell
python src\generate_data.py
```

Lo script usa un seed fisso, quindi rigenerando i dati si ottiene lo stesso dataset.

## Eseguire la pipeline

```powershell
python src\combine_sales.py
```

La pipeline legge i CSV da `data/`, uniforma le colonne, pulisce i record e calcola il riepilogo mensile.

## Pulizia applicata

Una vendita viene mantenuta se ha:

- una data valida;
- un prodotto e un cliente non vuoti;
- una quantità maggiore di zero;
- un prezzo unitario maggiore di zero.

Le righe duplicate vengono rimosse.

## Output

I risultati vengono scritti in:

- `output/sales_clean/`: vendite validate e standardizzate.
- `output/monthly_sales/`: aggregato mensile per Paese.

Spark scrive ciascun output in una cartella contenente uno o più file `part-*.csv`, oltre ai file di stato e checksum. Non rinominare manualmente i file di partizione mentre Spark sta scrivendo.

## Risultati attesi

Con il seed attuale:

- Righe dopo l'unione: 20.040
- Vendite valide dopo la pulizia: 19.536
- Gruppi mensili: 24 (12 mesi per ciascuno dei 2 Paesi)

## Power BI

1. Genera prima gli output seguendo i passaggi sopra.
2. In Power BI Desktop seleziona **Home → Get data → Text/CSV**.
3. Importa il file `part-*.csv` contenuto in `output/monthly_sales/`.
4. Crea visualizzazioni con `month` sull'asse, `revenue` e `units_sold` come valori e `country` come legenda o filtro.

## Note

I dati sono sintetici e creati esclusivamente per esercitazione. Gli output in `output/` sono rigenerabili e sono esclusi dal controllo di versione.