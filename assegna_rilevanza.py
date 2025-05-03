from pprint import pprint 
import json

file_path='final_relevance.json'

if False:
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    res = { uin:{} for uin in data }


    for uin in data:
        print(uin+'\n\n\n')
        data[uin].pop('type')
        for se in data[uin]:
            for rank_model, titoli_dict in data[uin][se].items():
                titoli_list = data[uin][se][rank_model]
                for t in titoli_list:
                    rilevante = t['rilevante']
                    titolo = t['title']
                    print(titolo)
                    print(rilevante)
                    if titolo not in res[uin]:
                        print(f'aggiungo {titolo} a {uin}')
                        res[uin].update({ titolo : [] })
                    res[uin][titolo].append(rilevante)

    print('\n\n\n')            
    pprint(res)

    for uin, titoli in res.items():
        for titolo, rates in titoli.items():
            print(f'{uin} -> {titolo} \n  {rates}')
            rilevanza = input('Rilevanza : ')
            print('\n')
            if not rilevanza:
                rilevanza = sum(rates)/len(rates)
            titoli[titolo]= rilevanza


    with open('valutazioni_rilevanza.json','w') as file:
        json.dump(res,file)
    
else :
    bmark_path = 'benchmark.json'
    with open('valutazioni_rilevanza.json', 'r') as file:
        valutazioni = json.load(file)

    with open(file_path, 'r') as file:
        dati_corretti = json.load(file)

    

    for uin, val in dati_corretti.items():
        print(uin)
        for se in val:
            print(se)
            if se != 'type':
                for rank_model in dati_corretti[uin][se]:
                    print(rank_model)
                    for movie in dati_corretti[uin][se][rank_model]:
                        print(movie)
                        titolo = movie['title']
                        rilevante = valutazioni[uin][titolo]
                        movie['rilevante'] = rilevante

    with open(bmark_path, 'w') as file:
        json.dump(dati_corretti, file)
