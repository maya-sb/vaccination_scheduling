import os
import csv

from django.core.management.base import BaseCommand

from vaccination.models import VaccinationCenter


class Command(BaseCommand):
    help = 'Importa arquivo csv com os locais de vacinação'

    def handle(self, *args, **options):

        print('*---------------Importação dos Locais de Vacinação---------------*')
        print('- Digite o caminho do arquivo que deseja importar (sem "")')
        print('- OU 1: Usar "vaccination/data/ubs.csv"')
        print('- OU 2: Sair')

        valid_path = False
        path = ""

        while not valid_path and path != "1" and path != "2":
            path = input('Caminho ou opção: ')

            if path == "1":
                path = os.path.join('vaccination', 'data', 'ubs.csv')
            elif path == "2":
                break
            try:

                with open(path, 'r', encoding="utf-8") as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        cnes = int(row['cod_cnes'])
                        name = row['nom_estab']
                        address = row['dsc_endereco']
                        neighborhood = row['dsc_bairro']
                        city = row['dsc_cidade']

                        VaccinationCenter.objects.update_or_create(cnes=cnes,
                                                                   defaults={'name': name,
                                                                             'address': address,
                                                                             'neighborhood': neighborhood,
                                                                             'city': city})

                    print('Arquivo importado com sucesso!')

            except KeyError:
                print("Arquivo não possui as colunas necessárias. Tente novamente.")

            except FileNotFoundError:
                print("Arquivo não encontrado. Tente novamente.")

            except Exception:
                print("Algo deu errado. Tente novamente.")

            else:
                valid_path = True
