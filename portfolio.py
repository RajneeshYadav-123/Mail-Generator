# import pandas as pd
# import chromadb
# import uuid


# class Portfolio:
#     def __init__(self, file_path="resource/job1.csv"):
#         self.file_path = file_path
#         self.data = pd.read_csv(file_path)
#         self.chroma_client = chromadb.PersistentClient('vectorstore')
#         self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

#     def load_portfolio(self):
#         if not self.collection.count():
#             for _, row in self.data.iterrows():
#                 self.collection.add(documents=row["Techstack"],
#                                     metadatas={"links": row["Links"]},
#                                     ids=[str(uuid.uuid4())])

#     def query_links(self, skills):
#         return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
    
    
import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="resource/job1.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        if not skills:
            return []
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

    def get_all_skills(self):
        skills = []
        for _, row in self.data.iterrows():
            techs = row["Techstack"].split(",")
            skills.extend([t.strip().lower() for t in techs])
        return list(set(skills))

 
    def match_skills(self, job_skills):
        portfolio_skills = set(self.get_all_skills())
        job_skills = set([s.lower() for s in job_skills])

        matched = job_skills.intersection(portfolio_skills)
        missing = job_skills.difference(portfolio_skills)

        score = (len(matched) / len(job_skills)) * 100 if job_skills else 0

        return {
            "matched": list(matched),
            "missing": list(missing),
            "score": round(score, 2)
        }

