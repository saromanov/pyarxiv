import asyncio
import requests

#Implementation of Arxiv API
#http://arxiv.org/help/api/index


#http://academia.stackexchange.com/questions/38969/getting-a-dump-of-arxiv-metadata

class PyArxiv:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.commands = []

    async def _get(self, path):
        result = requests.get(path)
        print(result.text)

    def _add(self, func):
        self.commands.append(asyncio.ensure_future(func))

    def _req(self, path, sync):
        if sync is False:
            self.commands.append(asyncio.ensure_future(self._get(path)))
        else:
            print(path)
            r = requests.get(path)
            if r.status_code == 200:
                return r.text

    def query(self, msg, start=0, max_items=10, id_list="", sync=True, sort_order='relevance',
            author=''):
        ''' query is for searching papers
            Args:
                msg - target for the query
                start - start page
                max_items - max items for query
                id_list - TODO
                sync - True is getting data sync, False - gettin data as async
                sort_order - sorting results
        '''

        path = 'http://export.arxiv.org/api/query?search_query=all:{0}&start={1}&max_results={2}&id_list={3}&sortBy={4}'.format(msg, start, max_items,\
                id_list, sort_order)
        return self._req(path, sync)

    def queryByAuthor(self, authors, sync=True):
        ''' This method provides finding papers by author
            Args:
                author - Target author
        '''
        if len(author) == 0:
            raise Exception("author parameter is empty")
        authorsq = 'au:{0}'.format(authors[0])
        for i in range(1, len(authors)):
            authorsreq += '+AND+au:{0}'.format(authors[i])
        path = 'http://export.arxiv.org/api/query?search_query={0}'.format(authorsreq)
        return self._req(path)

    def metadata(self, subset, startdate, enddate):
        '''
        Args:
            subset - for example math, cs
            startdate, enddate - must be in the format 2015-07-28
        '''
        path = 'http://export.arxiv.org/oai2?verb=ListRecords&set={0}&from={1}&until=2015-01-31&metadataPrefix=arXiv'
        self.commands.append(asyncio.ensure_future(self._get(path)))

    def run(self):
        self.loop.run_until_complete(asyncio.wait(self.commands))
        self.loop.close()
