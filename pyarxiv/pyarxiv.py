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

    def query(self, msg, start=0, max_items=10, id_list=[], sync=True):
        path = 'http://export.arxiv.org/api/query?search_query=all:{0}&start={1}&max_results={2}&id_list={3}'.format(msg, start, max_items,\
                id_list)
        if sync is False:
            self.commands.append(asyncio.ensure_future(self._get(path)))
        else:
            r = requests.get(path)
            if r.status_code == 200:
                return r.text

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
