# pensions-database
**Project for UIC's _CS 480: Database Systems_**
**Team Name**: actuary-pension  
**Team Member(s)**: Carmen Thom  
Document Question-Answering System built on OECD's Pension Outlooks and Pension Market in Focus.  

The pension outlooks are an analysis done every 2 years on changes in policy for public and private pensions, as well as trend assesment.  
The pension market in focus is a yearly report that gives data on pension systems to guide policy, global comparisons, and help people in accessing and developing retirement savings plans.  

The VectorDB I used is FAISS. In the function `index_faiss()`, it calls my chunking/embedding function and builds the indices for the DB. It saves the database as `vector_index.faiss` within the projects directory. It only calls `index_faiss()` if `vector_index.faiss` doesn't exist, so if this proccess somehow gets interupted, delete `vector_index.faiss` before running again.

**NOTE:** `get_chunked_text()` has an optional parameter `chunk_size` that defaults to 500, and `search_faiss()` has an optional k parameter for KNN algo.