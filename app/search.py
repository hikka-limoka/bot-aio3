from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
from whoosh.qparser import QueryParser, OrGroup
from whoosh.query import FuzzyTerm, Wildcard

import os

class Search:
    def __init__(self, query: str):
        self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
        self.query = query

    def search_module(self, content):
        if not os.path.exists("limoka_search"):
            os.makedirs("limoka_search")
        
        ix = create_in("limoka_search", self.schema)
        writer = ix.writer()
        module_count = 0
        for module_content in content:
            module_count += 1
            writer.add_document(
                title=f"{module_content['id']}", 
                path=f"{module_count}",
                content=module_content["content"]
            )
        writer.commit()

        with ix.searcher() as searcher:

            parser = QueryParser("content", ix.schema, group=OrGroup)
            query = parser.parse(self.query)

            fuzzy_query = FuzzyTerm("content", self.query, maxdist=1, prefixlength=2)

            wildcard_query = Wildcard("content", f"*{self.query}*")

            results = searcher.search(query)

            if not results:
                results = searcher.search(fuzzy_query)
            if not results:
                results = searcher.search(wildcard_query)

            if results:
                best_match = results[0]
                return int(best_match["title"])
            else:
                return 0