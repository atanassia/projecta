import datetime
import os
from typing import Optional

import pandas as pd
from django.forms import model_to_dict
from project_a.settings import MEDIA_ROOT
from projecta import models
from dataclasses import dataclass


@dataclass()
class Pages:
    pages = [
        'workers', 'clients', 'agreements', 'contacts',
        'tickets', 'acts', 'equipment'
    ]


class CreatorXLSX:

    def __init__(self, company, pages: Optional[list] = None):
        """
        Accepts the user's company and a list of pages to be included in the xlsx file
        * Pages can be empty - in this case all pages will be included
        """
        self.company = company
        self.filename = self.gen_xlsx_name()
        self.writer = pd.ExcelWriter(path=self.filename, engine='xlsxwriter')
        self.pages = pages or Pages.pages

    def gen_xlsx_name(self):
        company_name = str(self.company).replace('\"', '')
        filename = f"{int(datetime.datetime.timestamp(datetime.datetime.utcnow()))}-{company_name}.xlsx"
        filename = os.path.join(MEDIA_ROOT, 'excel', filename)
        return filename

    @staticmethod
    def get_dataframe(dataset, columns=None):
        dataset = map(model_to_dict, dataset)
        dataset = pd.DataFrame(dataset, columns=columns)
        return dataset

    def get_contacts(self, clients):
        result = pd.DataFrame()
        for client in clients:
            result = pd.concat([
                result,
                self.get_dataframe(client.contacts.all(), models.ClientContact.xlsx_columns())
            ])
        return result

    def write(self, df: pd.DataFrame, sheet_name: str):
        df.to_excel(self.writer, sheet_name=sheet_name, index=False)

    def create_file(self):
        for page in self.pages:
            try:
                if page != 'contacts':
                    query_set = getattr(self.company, page).all()
                    df = self.get_dataframe(query_set, query_set[0].xlsx_columns())

                else:
                    clients_qs = self.company.clients.all()
                    df = self.get_contacts(clients_qs)

                self.write(df, page.capitalize())
            except AttributeError:
                pass
            except IndexError:
                pass

        self.writer.close()
