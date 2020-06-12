from datetime import datetime

records = [
    {'source': '48-996355555',
     'destination': '48-666666666',
     'end': 1564610974,
     'start': 1564610674},
    {'source': '41-885633788',
     'destination': '41-886383097',
     'end': 1564506121,
     'start': 1564504821},
    {'source': '48-996383697',
     'destination': '41-886383097',
     'end': 1564630198,
     'start': 1564629838},
    {'source': '48-999999999',
     'destination': '41-885633788',
     'end': 1564697158,
     'start': 1564696258},
    {'source': '41-833333333',
     'destination': '41-885633788',
     'end': 1564707276,
     'start': 1564704317},
    {'source': '41-886383097',
     'destination': '48-996384099',
     'end': 1564505621,
     'start': 1564504821},
    {'source': '48-999999999',
     'destination': '48-996383697',
     'end': 1564505721,
     'start': 1564504821},
    {'source': '41-885633788',
     'destination': '48-996384099',
     'end': 1564505721,
     'start': 1564504821},
    {'source': '48-996355555',
     'destination': '48-996383697',
     'end': 1564505821,
     'start': 1564504821},
    {'source': '48-999999999',
     'destination': '41-886383097',
     'end': 1564610750,
     'start': 1564610150},
    {'source': '48-996383697',
     'destination': '41-885633788',
     'end': 1564505021,
     'start': 1564504821},
    {'source': '48-996383697',
     'destination': '41-885633788',
     'end': 1564627800,
     'start': 1564626000}]
# Constantes
TARIFA_DIURNA_INICIO = 6
TARIFA_DIURNA_FIM = 22
ENCARGO_PERMANENTE = 0.36
TAXA_DIURNA = 0.09


# Funções
def adicionar_duracao():
    """
    Adiciona a coluna "duracao" na lista records contendo o tempo de cada ligação em minutos fechados
    :return: records
    """
    for item in range(len(records)):
        inicio = datetime.fromtimestamp(records[item]['start'])
        final = datetime.fromtimestamp(records[item]['end'])
        duracao = int(round(((final - inicio).total_seconds() / 60), 2))
        records[item]["duracao"] = str(duracao)
    return records


def preco_ligacao():
    """
    Adiciona a coluna "total" contendo o preço de cada ligação
    :return: records
    """
    for item in range(len(records)):
        inicio_diurno = (TARIFA_DIURNA_INICIO < datetime.fromtimestamp(records[item]['start']).hour < TARIFA_DIURNA_FIM)
        fim_diurno = (TARIFA_DIURNA_INICIO < datetime.fromtimestamp(records[item]['end']).hour < TARIFA_DIURNA_FIM)
        fim_noturno = datetime.fromtimestamp(records[item]['end']).hour > TARIFA_DIURNA_FIM
        if inicio_diurno and fim_diurno:
            records[item]['total'] = round((float(records[item]['duracao']) * TAXA_DIURNA + ENCARGO_PERMANENTE), 2)
        elif inicio_diurno and fim_noturno:
            custo_diurno = (TARIFA_DIURNA_FIM - records[item]['start'])
            records[item]['total'] = round(custo_diurno * TAXA_DIURNA + ENCARGO_PERMANENTE, 2)
        else:
            records[item]['total'] = ENCARGO_PERMANENTE
    return records


def pegar_entradas(source):
    return lambda x: x['total'] if x['source'] == source else 0


def classify_by_phone_number(records):
    adicionar_duracao()
    preco = preco_ligacao()
    sources = sorted(set(map(lambda x: x['source'], preco)))
    resultado = [{'source': source, 'total': round(sum(map(pegar_entradas(source), preco)), 2)} for source in sources]
    resultado_ordenado = sorted(resultado, key=lambda k: k['total'], reverse=True)
    return resultado_ordenado
