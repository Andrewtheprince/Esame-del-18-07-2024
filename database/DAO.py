from database.DB_connect import DBConnect
from model.gene import Gene


class DAO():

    @staticmethod
    def getAllGenes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from genes"""

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(a,b):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select DISTINCT g.GeneID , g.Chromosome , c.Localization 
                    from genes g, classification c 
                    WHERE g.Chromosome >= %s
                    and g.Chromosome <= %s
                    and c.GeneID = g.GeneID 
                    order by Chromosome asc
                    """

        cursor.execute(query,(a,b,))

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap,a,b):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCTROW g1.GeneID as g1id, g2.GeneID as g2id, g1.Chromosome as ch1, g2.Chromosome as ch2, c1.Localization, c2.Localization, i.Expression_Corr as peso
                    FROM genes g1, genes g2, classification c1, classification c2, interactions i
                    WHERE g1.GeneID = c1.GeneID 
                    and g2.GeneID = c2.GeneID 
                    and c1.Localization = c2.Localization 
                    and g1.Chromosome >= %s
                    and g1.Chromosome <= %s
                    and g2.Chromosome >= %s
                    and g2.Chromosome <= %s
                    and ((i.GeneID1=g1.GeneID AND i.GeneID2=g2.GeneID)
                         OR (i.GeneID1=g2.GeneID AND i.GeneID2=g1.GeneID)) 
                    and g1.GeneID < g2.GeneID 
                    order by g1id, g2id"""

        cursor.execute(query,(a,b,a,b,))

        for row in cursor:
            result.append((idMap[row["g1id"]],idMap[row["g2id"]],row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getChromosomeVals():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Chromosome  
                    from genes g 
                    order by Chromosome asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Chromosome"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getLocalization():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.Localization
                    from classification c 
                    order by Localization asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Localization"])

        cursor.close()
        conn.close()
        return result