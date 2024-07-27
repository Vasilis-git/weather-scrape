current_time=$(date "+%Y-%m-%d")
curl https://penteli.meteo.gr/stations/argos/NOAAPRMO.TXT >> measurements/argos_$current_time.txt
curl https://penteli.meteo.gr/stations/aigio/NOAAPRMO.TXT >> measurements/aigio_$current_time.txt
curl https://penteli.meteo.gr/stations/kalamata/NOAAPRMO.TXT >> measurements/kalamata_$current_time.txt
curl https://penteli.meteo.gr/stations/sparti/NOAAPRMO.TXT >> measurements/sparti_$current_time.txt
curl https://penteli.meteo.gr/stations/tripoli/NOAAPRMO.TXT >> measurements/tripoli_$current_time.txt
curl https://penteli.meteo.gr/stations/isthmos/NOAAPRMO.TXT >> measurements/korinthos_$current_time.txt
curl https://penteli.meteo.gr/stations/gytheio/NOAAPRMO.TXT >> measurements/gytheio_$current_time.txt
curl https://penteli.meteo.gr/stations/megalopoli/NOAAPRMO.TXT >> measurements/megalopoli_$current_time.txt
curl https://penteli.meteo.gr/stations/amaliada/NOAAPRMO.TXT >> measurements/amaliada_$current_time.txt

